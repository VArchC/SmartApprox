import sys

from instructions_classification import *

training_apps = [
                "2mm",
                "blackscholes",
                "bzip2",
                "correlation",
                "dijkstra",
                "fasta",
                "fft",
                "floyd-warshall",
                "jmeint",
                "k-nucleotide",
                "inversek2j",
                "mandelbrot",
                "qsort",
                "bunzip2",
                "jpeg",
                "nbody",
                "pi",
                "reg_detect",
                "sobel",
                "spectralnorm",
                "reverse-complement",
                "fannkuch-redux",
                "mm",
                "jacobi-2d-imper",
                "atax",
                "covariance"
            ]

test_apps = [
#                #"2mm",
#                #"atax",
                "blackscholes",
#                #"bzip2",
#                #"bunzip2",
#                #"correlation",
#                #"covariance",
                "dijkstra",
#                #"fannkuch-redux",
#                #"fasta",
#                #"fft",
#                #"floyd-warshall",
#                #"jacobi-2d-imper",
#                #"jmeint",
                "k-nucleotide",
#                #"inversek2j",
                "mandelbrot",
#                #"mm",
#                #"qsort",
                "jpeg",
#                #"nbody",
                "pi",
#                #"reg_detect",
#                #"reverse-complement",
                "sobel",
#                #"spectralnorm",
            ]

#test_apps=training_apps


memory_features = [
                'Approximate_DRAM accesses',
                'D$ read_accesses',
                'D$ write_accesses',
                'DRAM accesses',
                'I$ read_accesses',
                'L2$ read_accesses',
                'L2$ write_accesses',
                'L2$ writebacks',
            ]

approx_dram_features =[
                'Approximate_DRAM accesses',
                'Approximate_DRAM fraction',
        ]

fp_instructions = [
            FP,
        ]

all_instr_features = [
            FLOW,
            JUMP_REG,
            LOAD,
            STORE,
            MEMORY,
            BARRIER,
            FP,
            TOTAL,
        ]
norm_all_instr_features = [
            NORM_PREAMBLE + MEMORY,
            NORM_PREAMBLE + FLOW,
            NORM_PREAMBLE + LOAD,
            NORM_PREAMBLE + STORE,
            NORM_PREAMBLE + TOTAL,
            NORM_PREAMBLE + BARRIER,
            NORM_PREAMBLE + FP,
            NORM_PREAMBLE + JUMP_REG,
        ]

mem_instr_features = [
            MEMORY,
            LOAD,
            STORE,
            BARRIER,
        ]

mem_norm_instr_features = [
            NORM_PREAMBLE + MEMORY,
            #NORM_PREAMBLE + ARITHMETIC,
            #NORM_PREAMBLE + FLOW,
            #NORM_PREAMBLE + LOAD,
            #NORM_PREAMBLE + STORE,
            #NORM_PREAMBLE + TOTAL,
            NORM_PREAMBLE + BARRIER,
            #NORM_PREAMBLE + FP,
            #NORM_PREAMBLE + JUMP_REG,
        ]


cache_hit_ratio = [
                'D$ miss_rate',
                'L2$ miss_rate',
                'I$ miss_rate',
        ]

flow_instrs = [
            FLOW,
        ]


datasize_features = [
                'D$ bytes_read',
                'D$ bytes_written',
                'L2$ bytes_read',
                'L2$ bytes_written',
                'I$ bytes_read',
        ]

dram_energy_features =[
    'Average Power',
    'Total Idle Energy (Active + Precharged)',
    'Active Idle Energy',
    'Auto-Refresh Energy',
        ]

dram_cmd_features =[
        '#ACT commands',
        '#RD + #RDA commands',
        '#WR + #WRA commands',
        '#PRE (+ #PREA) commands',
        '#REF commands',
        '#Auto-Refresh Cycles',
        'Total Trace Length (clock cycles)',
        ]
gen_best=['D$ bytes_read',
 'Total Idle Energy (Active + Precharged)',
 'I$ miss_rate',
 'floating-point',
 'D$ miss_rate']

gen_median=['Active Idle Energy',
 'floating-point',
 'Total Idle Energy (Active + Precharged)',
 'Auto-Refresh Energy',
 'D$ bytes_written',
 'Approximate_DRAM accesses']

gen_worst=['Auto-Refresh Energy',
 '#RD + #RDA commands',
 'L2$ read_accesses',
 'floating-point',
 'D$ miss_rate',
 'L2$ bytes_read',
 'Approximate_DRAM accesses',
 'D$ bytes_written',
 'I$ read_accesses']

features_lists = {
                #"AMA"           : approx_dram_features,
                #"CE"            : cache_hit_ratio,
                #"DS"            : datasize_features,
                #"EI"            : all_instr_features, 
                #"MA"            : memory_features, 
                #"MCC"           : dram_cmd_features,
                #"MEB"           : dram_energy_features,
                #"MI"            : mem_instr_features, 
                ##
                #'GA-best'      : gen_best,
                'GA-median'    : gen_median,
                #'GA-worst'     : gen_worst,
            } 
