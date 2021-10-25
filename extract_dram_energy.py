from common_params import energy_data, NOMINAL_VOLTAGE

ZERO='0'

ENERGY_FEATURES=[
    'Average Power',
    'Total Idle Energy (Active + Precharged)',
    #'ACT Stdby Energy',
    #'WR Stdby Energy', 
    #'PRE Stdby Energy',
    #'Precharge Idle Energy',
    #'ACT Cmd Energy',
    #'PRE Cmd Energy',
    #'WR Cmd Energy',
    #'RD Cmd Energy',
    'Active Idle Energy',
    'Auto-Refresh Energy',
        ]

CMD_FEATURES=[
        '#ACT commands',
        '#RD + #RDA commands',
        '#WR + #WRA commands',
        '#PRE (+ #PREA) commands',
        '#REF commands',
        '#Auto-Refresh Cycles',
        'Total Trace Length (clock cycles)',
        ]


dram_energy={}
dram_cmd={}
for approx in energy_data.keys():
    for app in energy_data[approx].keys():
        dram_energy[app]={}
        dram_cmd[app]={}
        for input_type in energy_data[approx][app].keys():
            dram_energy[app][input_type]={}
            dram_cmd[app][input_type]={}

            accur_data = energy_data[approx][app][input_type][ZERO][NOMINAL_VOLTAGE][0]
            total_trace_energy = accur_data['Total Trace Energy']

            for energy_features in ENERGY_FEATURES:
                dram_energy[app][input_type][energy_features] = accur_data[energy_features] / total_trace_energy

            for cmd_features in CMD_FEATURES:
                dram_cmd[app][input_type][cmd_features] = accur_data[cmd_features]
