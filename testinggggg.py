import json


line_phase_open=open('bhel/LinePhase.json')
line_phase_map = json.load(line_phase_open)

if "B" in line_phase_map :
    print("Found B")
if "Z" in line_phase_map :
    print("Found Z")
if "R" in line_phase_map :
    print("Found R")
    
    
#Added new file to check git reset

#New lines to check revert