# from datetime import datetime
# import json

# import config_validator

# time_table_open = open('pre_config_files/TimeTable.json')
# site_data_open = open('pre_config_files/SiteData.json')
# period_phase_limit_open = open('pre_config_files/PeriodPhaseLimits.json')
# phase_conflict_open = open('pre_config_files/PhaseConflict.json')
# inter_phase_duration_open = open('pre_config_files/InterPhaseDuration.json')
# smartmicro_open = open('pre_config_files/SmartMicro.json')
# phase_detector_open = open('pre_config_files/ApproachPhaseDetectorMap.json')
# approach_detector_open = open('pre_config_files/ApproachPhaseApproach.json')


# time_table=json.load(time_table_open)
# site_data=json.load(site_data_open)
# period_phase_limit = json.load(period_phase_limit_open)
# phase_conflict = json.load(phase_conflict_open)
# inter_phase_duration = json.load(inter_phase_duration_open)
# smartmicro = json.load(smartmicro_open)
# phase_detector = json.load(phase_detector_open)
# approach_detector = json.load(approach_detector_open)



# def validation_manager() :
#     '''
#     Return the final json file
#     '''
#     zero_period = config_validator.check_0_period(period_phase_limit)
#     offline_mode = config_validator.check_offline_mode(time_table)
#     overlap = config_validator.manager(time_table)
#     period_phase = config_validator.period_phase_consistency(time_table,site_data,period_phase_limit)
#     inter_phase = config_validator.inter_phase_conflict(phase_conflict,inter_phase_duration)
#     detector_scn = config_validator.check_detector_scn(smartmicro,phase_detector)
#     phase_detector_check = config_validator.phase_detector_consistency(phase_detector,approach_detector)
#     radar_ip = config_validator.check_radar_ip(smartmicro)
#     approach_phase_detector_map = config_validator.approach_phase_detector_map(phase_detector)

#     final_msg = json.dumps({
#         'Zero period' : zero_period,
#         'Offline mode' : offline_mode,
#         'Overlapping' : overlap,
#         'Period Phase Consistency' : period_phase,
#         'Interphase consistency' : inter_phase,
#         'Detector SCN' : detector_scn,
#         'Phase Detector consistency' : phase_detector_check,
#         'Radar IP' : radar_ip,
#         'Approach Phase Detector Map' : approach_phase_detector_map
#     }, indent= 4)

#     return final_msg

# print(validation_manager())