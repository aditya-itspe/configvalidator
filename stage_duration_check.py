#HELP BY APOORVA
import json

stage_default_open = open('configvalidator/bhel/StageDefault.json')
phase_stage_open = open('configvalidator/bhel/PhaseStage.json')
period_phase_limit_open = open('configvalidator/bhel/PeriodPhaseLimits.json')
plan_open = open('configvalidator/bhel/Plan.json')

period_phase_limit = json.load(period_phase_limit_open)
stage_default = json.load(stage_default_open)
phase_stage = json.load(phase_stage_open)
plan = json.load(plan_open)

def stage_duration_check(period_phase_limit, stage_default, phase_stage,plan) :
    '''
    Checking stage duration between Effective min and max
    '''
    error_msg = {}
    j=0
    for key in stage_default :
        effective_stage_min = int(stage_default[key]['min'])
        effective_stage_max = int(stage_default[key]['max'])
        
        stage_phase_map=[]
        for key_1 in phase_stage[key] :
            if phase_stage[key][key_1] == 'S' or phase_stage[key][key_1] == 'B' :
                stage_phase_map.append(key_1)
        
        for i in range(len(period_phase_limit[key])) :
            if period_phase_limit[key][i]['phase'] in stage_phase_map :
                if period_phase_limit[key][i]['min'] > effective_stage_min :
                    effective_stage_min = period_phase_limit[key][i]['min']
                if period_phase_limit[key][i]['max'] < effective_stage_max :
                    effective_stage_max = period_phase_limit[key][i]['max']
        
        for key_1 in plan :
            for key_2 in plan[key_1] :
                for key_3 in plan[key_1][key_2] :
                    if plan[key][key_1][key_3]['duration'] < effective_stage_min or plan[key][key_1][key_2]['duration'] > effective_stage_max :
                        add_msg={
                            'Error' : 'Stage duration not in allowed limit',
                            'Stream' : key_1,
                            'Plan number' : key_2,
                            'Stage order' : plan[key_1][key_2][key_3]['stage_order']
                        }
                        error_msg[j] = add_msg
                        j+=1
    if error_msg=={} :
        return None
    return error_msg

#Can't do like this as we need the same key to compare. need to make 2 functions or multiple which
#send the required values for a particular stage (eg. it's min max and phase_Stage_map)
print(stage_duration_check(period_phase_limit, stage_default, phase_stage,plan))