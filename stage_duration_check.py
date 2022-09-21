#HELP BY APOORVA
import json

stage_default_open = open('bhel/StageDefault.json')
phase_stage_open = open('bhel/PhaseStage.json')
period_phase_limit_open = open('bhel/PeriodPhaseLimits.json')

period_phase_limit = json.load(period_phase_limit_open)
stage_default = json.load(stage_default_open)
phase_stage = json.load(phase_stage_open)

def stage_duration_check(period_phase_limit, stage_default, phase_stage) :
    '''
    Checking stage duration between Effective min and max
    '''
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
                    
