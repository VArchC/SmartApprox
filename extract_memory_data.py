
import sys
sys.path.append("..")

from pickle_utils import *


memory_data=load_pickle("reports/smartapprox/memory_accesses.pck")


info_mem={}


for results_type in memory_data.keys():
    for app in memory_data[results_type].keys():
        info_mem[app]={}
        for input_type in memory_data[results_type][app].keys():
            info_mem[app][input_type]={}
            for prob in ['0']:#memory_data[results_type][app][input_type].keys():
                for memory in memory_data[results_type][app][input_type][prob].keys():
                    for data in memory_data[results_type][app][input_type][prob][memory].keys():
                        info_mem[app][input_type][memory.replace(" ","_") + " " + data.replace(" ", "_")] =  memory_data[results_type][app][input_type][prob][memory][data][0]
                        #print(app + memory + data + str(memory_data[results_type][app][input_type][prob][memory][data]))
                info_mem[app][input_type]["Approximate_DRAM fraction"] = info_mem[app][input_type]["Approximate_DRAM accesses"] / float(info_mem[app][input_type]["DRAM accesses"])


