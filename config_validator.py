from datetime import datetime
import json

time_table_open = open('pre_config_files/TimeTable.json')
site_data_open = open('pre_config_files/SiteData.json')
period_phase_limit_open = open('pre_config_files/PeriodPhaseLimits.json')
phase_conflict_open = open('pre_config_files/PhaseConflict.json')
inter_phase_duration_open = open('pre_config_files/InterPhaseDuration.json')
smartmicro_open = open('pre_config_files/SmartMicro.json')
phase_detector_open = open('pre_config_files/ApproachPhaseDetectorMap.json')
approach_detector_open = open('pre_config_files/ApproachPhaseApproach.json')


time_table=json.load(time_table_open)
site_data=json.load(site_data_open)
period_phase_limit = json.load(period_phase_limit_open)
phase_conflict = json.load(phase_conflict_open)
inter_phase_duration = json.load(inter_phase_duration_open)
smartmicro = json.load(smartmicro_open)
phase_detector = json.load(phase_detector_open)
approach_detector = json.load(approach_detector_open)


#Check 0 period
def check_0_period(period_phase_limit) :                            #Check : 0 period not defined in the TimeTable only in PeriodPhaseLimit. 
    '''
    Check for 0 period in the time_table
    '''
    error_msg = {}
    if "0" not in period_phase_limit :
        error_msg = {
            "Error" : "0 period not found"
        }
    if error_msg == {} :
        return None
    return error_msg

#Check for Offline modes                                            #Update the list and the correct names
def check_offline_mode(time_table) :
    '''
    Check weather offline mode is from the allowed list
    '''
    allowed_offline_modes = ['FXTM','LOFF','FBFT','FLSH','LOFLVA','ATATFXFL']       #Add other allowed modes
    error_msg ={}
    j=0
    for key in time_table :
        for i in range(len(time_table[key])):
            for key_1 in time_table[key][i]['streams'] :
                offline_mode = time_table[key][i]["streams"][key_1]['offline_mode']
                if offline_mode not in allowed_offline_modes :
                    add_msg={
                        'Error'         : 'Check offline mode',
                        'Current_mode'  : offline_mode,
                        'Day'           : key,
                        'Index'         : str(i),
                    }
                    error_msg[j] = add_msg
                    j+=1
    if error_msg == {} :
        return None
    return error_msg                                                                #Check weather to return empty msg or None in case no error


#Overlapping
class Interval:
	def __init__(self, start, end):
		self.start = start
		self.end = end
def check_overlap(arr, n):
    '''
    Check for overlap in the Interval
    '''
    arr.sort(key=lambda x: x.start)          # Sort intervals in increasing order of start time
    for i in range(1, n):                      
        if (arr[i - 1].end > arr[i].start):
            return True
    
    return False  
def create_interval_array(week_data,key):
    '''
    Create Interval array to send to check_overlap
    '''                        
    #for key in week_data :
    day_schedule=[]
    for i in range(len(week_data[key])):
        start_time_string = week_data[key][i]['start_time']
        end_time_string = week_data[key][i]['end_time']
        start_datetime_obj = datetime.strptime(start_time_string, '%H:%M:%S').time()
        end_datetime_obj = datetime.strptime(end_time_string, '%H:%M:%S').time()
        interval_ = Interval(start_datetime_obj,end_datetime_obj)
        day_schedule.append(interval_)
    return day_schedule
def manager(time_table) :
    '''
    Main operator function.
    '''
    # week_data = week_time_table['week_schedule']
    error_msg ={}
    j=0
    for key in time_table :
        day_schedule = create_interval_array(time_table,key)
        n=len(day_schedule)-1
        overlap_bool = check_overlap(day_schedule[1:],n)            #Not taking first slot of each day as 18:38---
        if overlap_bool :
            error_add ={
                'Error' : 'Overlapping time slot in time table',
                'Day'   :  key
            }
            error_msg[j]=error_add
            j+=1
    if error_msg == {} :
        return None
    return error_msg


#Period consistency         #Check: In the frontend even though period 50 exists it doesn't show in JSON.parse(JunctionData['PeriodPhaseLimits']) but for other it is correct
def period_phase_consistency(time_table,site_data,period_phase_limit) :
    number_of_arms = site_data['number_of_arms']
    error_msg={}
    j=0
    
    period_time_table=[]
    for key in time_table:
        for i in range(len(time_table[key])):
            period_time_table.append(int(time_table[key][i]["period_number"]))
    period_time_table.sort()
    
    period_phase_limit_list =[]
    for key in period_phase_limit :
        period_phase_limit_list.append(int(key))
    period_phase_limit_list.sort()
    period_phase_limit_list.remove(0)                                               #As there is no zero period in Time Table
    if period_time_table != period_phase_limit_list :
        add_msg={
            'Error' : 'Period Inconsistency',
            'In Time Table' : len(period_time_table),
            'In Period Phase Limit' : len(period_phase_limit_list)
        }
        error_msg[j]=add_msg    
        j+=1
    if error_msg == {} :
        return None
    return error_msg


#Inter-Phase Conflict
def inter_phase_conflict(phase_conflict,inter_phase_duration) :
    error_msg={}
    j=0
    for key in phase_conflict:
        for key_1 in phase_conflict[key]:
            if phase_conflict[key][key_1]==0 and inter_phase_duration[key][key_1]!=0 :
                add_msg={
                    'Error' : 'Interphase duration non zero for non conflicting phases',
                    'Phase 1' : key,
                    'Phase 2' : key_1
                }
                error_msg[j]=add_msg
                j+=1
            if phase_conflict[key][key_1]!=0 and inter_phase_duration[key][key_1]==0 :
                add_msg={
                    'Error' : 'Interphase duration zero for conflicting phase',
                    'Phase 1' : key,
                    'Phase 2' : key_1
                }
                error_msg[j]=add_msg
                j+=1
    if error_msg == {} :
        return None
    return error_msg


#Detector SCN           #Only checking weather detector scn exists or not. 
def check_detector_scn(detector,phase_detector) :
    radar_list=[]
    error_msg={}
    j=0
    for key in detector['details'] :
        radar_list.append(detector['details'][key]["radar_scn"])
    for key in phase_detector :
        for key_1 in phase_detector[key] :
            if phase_detector[key][key_1]['xdetector_scn'] != '':
                val=phase_detector[key][key_1]['xdetector_scn']
                if val[:8] not in radar_list :
                    add_msg = {
                        'Error' : 'Check Detector SCN',
                        'Phase' : key_1
                    }
                    error_msg[j]=add_msg
                    j+=1
    if error_msg == {} :
        return None
    return error_msg


#ApproachPhaseDetectorMap vs ApproachPhaseApproach          #Check : Only using xdetector_scn and also [0:8] or is there a different source
def phase_detector_consistency(phase_detector,approach_detector) :
    '''
    Checking for Phase-Detector consistency in ApproachPhaseDetectorMap vs ApproachPhaseApproach
    '''
    error_msg = {}
    j=0
    phase_detector_map={}
    for key in approach_detector :
        for key_1 in approach_detector[key]:
            phase_select = approach_detector[key][key_1]
            phase_detector_map[phase_select]=key

    for key in phase_detector :
        for key_1 in phase_detector[key] :
            if key_1 in phase_detector_map :
                val = phase_detector[key][key_1]['xdetector_scn'][:8]
                if val != phase_detector_map[key_1] :
                    add_msg = {
                        'Error' : 'Phase - Detector Inconsistency',
                    }
                    error_msg[j] = add_msg
                    j+=1
    if error_msg == {} :
        return None
    return error_msg


#Radar Detector Smart micro
def check_radar_ip(smartmicro) :
    '''
    If detector type = Radar then radar IP should not be null
    '''
    error_msg = {}
    j=0
    for key in smartmicro['details'] :
        if smartmicro['details'][key]['radar_ip'] == {} :
            add_msg = {
                'Error' : 'IP address missing for radar detector',
                'Radar ID' : smartmicro['details'][key]['radar_id']
            }
            error_msg[j] = add_msg
            j+=1
    if error_msg == {} :
        return None
    return error_msg


#Approach Phase Detector Map
def check_approach_phase_detector_map(phase_detector) :
    '''
    Phase to approach mapping cannot be empty.
    '''
    error_msg={}
    phase_list=[]
    for key in phase_detector :
        for key_1 in phase_detector[key] :
            if phase_detector[key][key_1] != '':
                phase_list.append(phase_detector[key][key_1])
    if phase_list == [] :
        error_msg = {
            'Error' : 'Approach Phase Detector Map is empty'
        }
    if error_msg == {} :
        return None
    return error_msg

def validation_manager() :
    '''
    Return the final json file
    '''
    zero_period = check_0_period(period_phase_limit)
    offline_mode = check_offline_mode(time_table)
    overlap = manager(time_table)
    period_phase = period_phase_consistency(time_table,site_data,period_phase_limit)
    inter_phase = inter_phase_conflict(phase_conflict,inter_phase_duration)
    detector_scn = check_detector_scn(smartmicro,phase_detector)
    phase_detector_check = phase_detector_consistency(phase_detector,approach_detector)
    radar_ip = check_radar_ip(smartmicro)
    approach_phase_detector_map = check_approach_phase_detector_map(phase_detector)

    final_msg = json.dumps({
        'Zero period' : zero_period,
        'Offline mode' : offline_mode,
        'Overlapping' : overlap,
        'Period Phase Consistency' : period_phase,
        'Interphase consistency' : inter_phase,
        'Detector SCN' : detector_scn,
        'Phase Detector consistency' : phase_detector_check,
        'Radar IP' : radar_ip,
        'Approach Phase Detector Map' : approach_phase_detector_map
    }, indent= 4)

    return final_msg

#print(validation_manager())