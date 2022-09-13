from datetime import datetime
import json

# junction_data_open = open('data.json')
# junction_data = json.load(junction_data_open)

#Check 0 period
async def check_0_period(period_phase_limit) :                             
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
async def check_offline_mode(time_table) :
    '''
    Check weather offline mode is from the allowed list
    '''
    allowed_offline_modes = ['FXTM','LOFF','FBFT','FLSH','LOFLVA','ATATFXFL','ATFXFXNO']       #Add other allowed modes, 'ATFXFXNO'
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
    return error_msg                                                               


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
async def manager(time_table) :
    '''
    Main operator function.
    '''
    # week_data = week_time_table['week_schedule']
    error_msg ={}
    j=0
    for key in time_table :
        day_schedule = create_interval_array(time_table,key)
        n=len(day_schedule)
        overlap_bool = check_overlap(day_schedule,n)            #Not taking first slot of each day as 18:38---
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
async def period_phase_consistency(time_table,site_data,period_phase_limit) :
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
async def inter_phase_conflict(phase_conflict,inter_phase_duration) :
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
async def check_detector_scn(detector,phase_detector) :
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
async def phase_detector_consistency(phase_detector,approach_detector) :
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
async def check_radar_ip(smartmicro) :
    '''
    If detector type = Radar then radar IP should not be null
    '''
    error_msg = {}
    j=0
    for key in smartmicro['details'] :
        if smartmicro['details'][key]['radar_ip'] == "" :
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
async def check_approach_phase_detector_map(approach_detector) :
    '''
    Phase to approach mapping cannot be empty.
    '''
    error_msg={}
    phase_list=[]
    for key in approach_detector :
        for key_1 in approach_detector[key] :
            if approach_detector[key][key_1] != '':
                phase_list.append(approach_detector[key][key_1])
    if phase_list == [] :
        error_msg = {
            'Error' : 'Approach Phase Detector Map is empty'
        }
    if error_msg == {} :
        return None
    return error_msg

async def otu_cpu_map(otu_cpu_mapping) :
    error_msg={}
    j=0
    for key in otu_cpu_mapping :
        for key_1 in otu_cpu_mapping[key] :
            if type(otu_cpu_mapping[key][key_1]) != int :
                add_msg = {
                    'Error' : 'OTU-CPU Map',
                    'Stages' : (key,key_1),
                    'Value' : otu_cpu_mapping[key][key_1]      
                }
                error_msg[j]=add_msg
                j+=1
    if error_msg == {}:
        return None
    return error_msg


async def stage_consistency(otu_cpu_mapping,stage_default,phase_stage,stage_stream):
    '''
    Stage consistency across Config
    OTUCPU map, StageDefault, PhaseStage, StageStream 
    '''
    error_msg={}
    j=0
    stage_default_list = []
    for key in stage_default :
        stage_default_list.append(int(key))
    
    #For Phase stage
    phase_stage_list =[]
    for key in phase_stage :
        phase_stage_list.append(int(key))
    if stage_default_list != phase_stage_list :
        add_msg = {
            "Error" : 'Stages do not match in stage default and phase stage'
        } 
        error_msg[j]=add_msg
        j+=1
    
    #For otu cpu mapping
    otu_stage_list=[]
    error_msg_1={}
    k=0
    for key in otu_cpu_mapping :
        otu_stage_list.append(int(key))    
    if otu_stage_list != stage_default_list :
        add_msg = {
            "Error" : 'Stages do not match in stage default and otu cpu mapping'
        } 
        error_msg_1[k]=add_msg
        k+=1
    if error_msg_1 == {} :
        for key in otu_cpu_mapping :
            cpu_list=[]
            for key_1 in otu_cpu_mapping[key] :
                cpu_list.append(int(key_1))
            if cpu_list != stage_default_list :
                add_msg = {
                "Error" : 'Stages do not match in stage default and otu cpu mapping'
                } 
                error_msg_1[k]=add_msg
                k+=1
    if error_msg_1 != {} :
        error_msg[j] = error_msg_1
        j+=1
    
    #For Stage stream
    for key in stage_stream :
        stream_stage_list = stage_stream[key]
        if stream_stage_list != stage_default_list :
            add_msg={
                'Error' : 'Stages do not match in stage default and stage stream',
                'Stream' : key
            }
            error_msg[j] = add_msg
            j+=1
    if error_msg == {}:
        return None 
    return error_msg

async def check_line_phase(line_phase_map) :    #Can add for PE phase type
    error_msg={}
    j=0
    for key in line_phase_map :
        if line_phase_map[key]['phase_type'] == "FI" :
            red=0
            amber=0
            green=0
            for key_1 in line_phase_map[key]['line_phase_mapping'] :
                if line_phase_map[key]['line_phase_mapping'][key_1] == "R" :
                    red+=1
                if line_phase_map[key]['line_phase_mapping'][key_1] == "A" :
                    amber+=1
                if line_phase_map[key]['line_phase_mapping'][key_1] == "G" :
                    green+=1
            if red == 0 or green ==0 or amber == 0 :
                add_msg = {
                    'Error' : 'Check Line Phase Map for FI Phase type',
                    'Phase' : key,
                    '(Red,Amber,Green)' : (red,amber,green)
                }
                error_msg[j] = add_msg
                j+=1

        if line_phase_map[key]['phase_type'] == "PI" :
            red=0
            amber=0
            for key_1 in line_phase_map[key]['line_phase_mapping'] :
                if line_phase_map[key]['line_phase_mapping'][key_1] == "R" :
                    red+=1
                if line_phase_map[key]['line_phase_mapping'][key_1] == "A" :
                    amber+=1
            if red != 0 or amber != 0 :
                add_msg = {
                    'Error' : 'Check Line Phase Map for PI Phase type',
                    'Phase' : key,
                    '(Red,Amber)' : (red,amber)
                }
                error_msg[j] = add_msg
                j+=1    
    if error_msg == {} :
        return None
    
    return error_msg

async def stage_conflicting_phase_check(phase_stage,plan,phase_conflict):
    conflicting_phase_map = {}
    error_msg={}
    j=0
    for key in phase_conflict :
        conflict_list=[]
        for key_1 in phase_conflict[key] :
            if phase_conflict[key][key_1]==1:
                conflict_list.append(key_1)
        conflicting_phase_map[key]=conflict_list
    
    #Check in PhaseStage
    for key in phase_stage :
        stage_phase_map=[]
        for key_1 in phase_stage[key] :
            if phase_stage[key][key_1]=="S" or phase_stage[key][key_1]=='B' :
                stage_phase_map.append(key_1)
        for phase in stage_phase_map :
            for item in conflicting_phase_map[phase] :
                if item in stage_phase_map :
                    add_msg={
                        'Error' : 'Stage contains conflicting phases',
                        'Conflicting Phase' : (phase,item),
                        'Stage' : key
                    }
                    error_msg[j]=add_msg
                    j+=1
                
    #Check in Plan
    for key_1 in plan :
        for key_2 in plan[key_1]:
            for key_3 in plan[key_1][key_2] :
                plan_phase=[]
                for i in range(len(plan[key_1][key_2][key_3]['phase_info'])):
                    plan_phase.append(plan[key_1][key_2][key_3]['phase_info'][i]["phase"])
                for phase in plan_phase :
                    for item in conflicting_phase_map[phase] :
                        if item in plan_phase :
                            add_msg ={
                                'Error' : 'Plan contains conflicting phases',
                                'Conflicting Phases' : (phase,item)
                            }
                            error_msg[j] = add_msg
                            j+=1
    
    if error_msg == {} :
        return None
    return error_msg





async def validation_manager(junction_data) :
    '''
    Return the final json file
    '''
    time_table = json.loads(junction_data['TimeTable'])
    site_data  = json.loads(junction_data['SiteData'])
    period_phase_limit = json.loads(junction_data['PeriodPhaseLimits'])
    phase_conflict=json.loads(junction_data['PhaseConflict'])
    inter_phase_duration = json.loads(junction_data['InterPhaseDuration'])
    smartmicro = json.loads(junction_data['DetectorConfig']['SMC'])
    phase_detector = json.loads(junction_data['PhaseDetectorMap'])
    approach_detector = json.loads(junction_data['ApproachPhaseApproach'])
    otu_cpu_mapping = json.loads(junction_data['OtuCpuMap'])
    stage_default = json.loads(junction_data['StageDefault'])
    phase_stage = json.loads(junction_data['PhaseStage'])
    stage_stream = json.loads(junction_data['StageStream'])
    line_phase_map = json.loads(junction_data['LinePhase'])
    plan = json.loads(junction_data['Plan'])
    #PLAN
    
    
    zero_period = await check_0_period(period_phase_limit)
    offline_mode = await check_offline_mode(time_table)
    overlap = await manager(time_table)
    period_phase = await period_phase_consistency(time_table,site_data,period_phase_limit)
    inter_phase = await inter_phase_conflict(phase_conflict,inter_phase_duration)
    detector_scn = await check_detector_scn(smartmicro,phase_detector)
    phase_detector_check = await phase_detector_consistency(phase_detector,approach_detector)
    radar_ip = await check_radar_ip(smartmicro)
    approach_phase_detector_map = await check_approach_phase_detector_map(approach_detector)
    otu_cpu_check = await otu_cpu_map(otu_cpu_mapping)
    stage_consistency_check = await stage_consistency(otu_cpu_mapping,stage_default,phase_stage,stage_stream)
    line_phase_map = await check_line_phase(line_phase_map)
    conflicting_phase_stage = await stage_conflicting_phase_check(phase_stage,plan,phase_conflict)

    final_msg = json.dumps({
        'Zero period' : zero_period,
        'Offline mode' : offline_mode,
        'Overlapping' : overlap,
        'Period Phase Consistency' : period_phase,
        'Interphase consistency' : inter_phase,
        'Detector SCN' : detector_scn,
        'Phase Detector consistency' : phase_detector_check,
        'Radar IP' : radar_ip,
        'Approach Phase Detector Map' : approach_phase_detector_map,
        'Otu Cpu Map' : otu_cpu_check,
        'Stage Consistency' : stage_consistency_check,
        'Line Phase Map' : line_phase_map,
        'Conflicting Phase in Stage' : conflicting_phase_stage,
    }, indent= 4)

    return final_msg


