from datetime import datetime
from distutils.log import error
import json
import site


site_data_open=open('bhel/SiteData.json')
time_table_open = open('bhel/TimeTable.json')
period_phase_limit_open = open('bhel/PeriodPhaseLimits.json')
phase_conflict_open = open('bhel/PhaseConflict.json')
interphase_duration_open = open('bhel/InterPhaseDuration.json')


time_table = json.load(time_table_open)
site_data = json.load(site_data_open)
period_phase_limit = json.load(period_phase_limit_open)
phase_conflict = json.load(phase_conflict_open)
interphase_duration = json.load(interphase_duration_open)

def period_phase_consistency(time_table,site_data,period_phase_limit,interphase_duration,phase_conflict) :
    '''
    Check for Period consistency
    '''
    # number_of_arms = site_data['number_of_arms']
    error_msg={}
    j=0
    
    phase_map = []
    for i in range(len(site_data['approaches'])) :
        for key in site_data['approaches'][i] :
            if key=='phase_left_turn' or key == 'phase_straight' or key == 'phase_right_turn' or key == 'phase_uturn' or key == 'ped_left_side' or key == 'ped_right_side' :
                if site_data['approaches'][i][key] != "" and site_data['approaches'][i][key] not in phase_map :
                    phase_map.append(site_data['approaches'][i][key])
    
    period_time_table=[]
    for key in time_table:
        for i in range(len(time_table[key])):
            period_time_table.append(int(time_table[key][i]["period_number"]))
    period_time_table.sort()
    
    period_phase_limit_list =[]
    for key in period_phase_limit :
        period_phase_limit_list.append(int(key))
    period_phase_limit_list.sort()
    period_phase_limit_list.remove(0)                                             
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


phase_map = []
for i in range(len(site_data['approaches'])) :
    for key in site_data['approaches'][i] :
        if key=='phase_left_turn' or key == 'phase_straight' or key == 'phase_right_turn' or key == 'phase_uturn' or key == 'ped_left_side' or key == 'ped_right_side' :
            if site_data['approaches'][i][key] != "" and site_data['approaches'][i][key] not in phase_map :
                phase_map.append(site_data['approaches'][i][key])
                                 

phase_map = []
for i in range(len(site_data['approaches'])) :
    for key in site_data['approaches'][i] :
        if key=='phase_left_turn' or key == 'phase_straight' or key == 'phase_right_turn' or key == 'phase_uturn' or key == 'ped_left_side' or key == 'ped_right_side' :
            if site_data['approaches'][i][key] != "" and site_data['approaches'][i][key] not in phase_map :
                phase_map.append(site_data['approaches'][i][key])
''
                                
print(sorted(phase_map))

