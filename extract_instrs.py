import sys
sys.path.append("..")
import numpy as np


from pickle_utils import load_pickle
from instructions_classification import classification, LOAD, NORM_PREAMBLE


instructions=load_pickle("reports/smartapprox/instructions.pck")

set_total_instrs=set()

info_instrs={}
norm_instrs={}
executed_instrs = lambda data: np.sum(list(data.values()))
all_instrs = lambda data: executed_instrs(data['All'])

for approx in instructions.keys():
    for app in instructions[approx].keys():
        info_instrs[app]={}
        norm_instrs[app]={}
        for input_type in instructions[approx][app].keys():
            info_instrs[app][input_type]={}
            norm_instrs[app][input_type]={}
            for c in classification.keys():
                info_instrs[app][input_type][c]=0
                norm_instrs[app][input_type][NORM_PREAMBLE + c]=0
                for instruction in instructions[approx][app][input_type].keys():
                    set_total_instrs.add(instruction)
                    if instruction in classification[c]:
                        info_instrs[app][input_type][c] += executed_instrs(instructions[approx][app][input_type][instruction])
                        norm_instrs[app][input_type][NORM_PREAMBLE + c] += executed_instrs(instructions[approx][app][input_type][instruction]) / float(all_instrs(instructions[approx][app][input_type]))

#set_total_instrs.sort()
#import pprint
#pprint.pprint(set_total_instrs)
#pprint.pprint(info_instrs)

