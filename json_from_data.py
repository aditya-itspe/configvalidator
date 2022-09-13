import json


junction_data_open = open('bhel.json')
junction_data = json.load(junction_data_open)



time_table = json.loads(junction_data['TimeTable'])
site_data  = json.loads(junction_data['SiteData'])
period_phase_limit = json.loads(junction_data['PeriodPhaseLimits'])
phase_conflict=json.loads(junction_data['PhaseConflict'])
inter_phase_duration = json.loads(junction_data['InterPhaseDuration'])
smartmicro = json.loads(junction_data['DetectorConfig']['SMC'])
phase_detector = json.loads(junction_data['PhaseDetectorMap'])
approach_detector = json.loads(junction_data['ApproachPhaseApproach'])
otu_cpu_mapping = json.loads(junction_data['OtuCpuMap'])
line_phase = json.loads(junction_data['LinePhase'])
phase_stage = json.loads(junction_data['PhaseStage'])
plan = json.loads(junction_data['Plan'])
stage_defaults = json.loads(junction_data['StageDefault'])
stage_streams = json.loads(junction_data['StageStream'])



# with open("bhel/StageStream.json", "w") as outfile:
#     json.dump(stage_streams, outfile)
    