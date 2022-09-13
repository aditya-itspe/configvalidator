from datetime import datetime
from distutils.log import error
import json


phase_stage_open=open('bhel/PhaseStage.json')
plan_open = open('bhel/Plan.json')
phase_conflict_open=open('bhel/PhaseConflict.json')

phase_stage = json.load(phase_stage_open)
plan = json.load(plan_open)
phase_conflict=json.load(phase_conflict_open)

def stage_conflicting_phase_check(phase_stage,plan,phase_conflict):
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
    
    return error_msg      
            
print(stage_conflicting_phase_check(phase_stage,plan,phase_conflict))
#Stage should not contain conflicting phases(PhaseStage, Plan)

