import numpy as np

from common_params import *

def get_static_energy_fraction(results_type, app, input_type, probability, vdd):
    data_app = [ energy_data[results_type][app][input_type][probability][vdd][x] for x in range(REPETITIONS) ]

    idle_energy = np.mean( [ data_app[x]['Total Idle Energy (Active + Precharged)'] for x in range(REPETITIONS) ]) 
    total_energy = np.mean( [ data_app[x]['Total Trace Energy'] for x in range(REPETITIONS) ] )

    return idle_energy / total_energy

def get_approximate_dram_accesses_fraction(results_type, app, input_type):
    approx_accesses  = memory_data[results_type][app][input_type]['0']['Approximate DRAM']['accesses'][0]
    dram_accesses    = memory_data[results_type][app][input_type]['0']['DRAM']['accesses'][0]
    return approx_accesses / float(dram_accesses)

def get_energy(results_type, app, input_type, vdd, error_scenario="median"):
    if app in energies[results_type].keys():
        if vdd == NOMINAL_VOLTAGE:
            return 1.0

        probability = probabilities_rt[error_scenario][float(vdd)]
        non_zero_energies = list(filter(lambda x: x>0, [ energies[results_type][app][input_type][probability][vdd][i][0] for i in range(REPETITIONS) ]))
        avg_energy  = np.mean(non_zero_energies)

        approx_accesses_fraction = get_approximate_dram_accesses_fraction(results_type, app, input_type)
        static_energy_fraction   = get_static_energy_fraction(results_type, app, input_type, probability, vdd)

        return static_energy_fraction * avg_energy + (1.0 - static_energy_fraction) * approx_accesses_fraction * avg_energy

    else:
        return float(vdd)



def get_quality(results_type, app, input_type, vdd, error_scenario="median"):
    if vdd == NOMINAL_VOLTAGE:
        return 1.0
    probability = probabilities_rt[error_scenario][float(vdd)]
    avg_quality = np.mean(qualities[results_type][app][input_type][probability])
    return avg_quality


def get_best_approx_level(app, quality_requirement, error_scenario="median"):
    min_vdd_quality = NOMINAL_VOLTAGE
    min_energy = get_energy(results_type, app, input_type, min_vdd_quality, error_scenario)
    for vdd in vdds:
        quality = get_quality(results_type, app, input_type, vdd, error_scenario)
        if quality >= quality_requirement:
            avg_energy = get_energy(results_type, app, input_type, vdd, error_scenario)
            if avg_energy < min_energy:
                min_energy = avg_energy
                min_vdd_quality = vdd
    return min_vdd_quality


def get_qualities(results_type, app, input_type, vdd, error_scenario="median"):
    qualities_app=[]
    for vdd in vdds:
        quality = get_quality(results_type, app, input_type, vdd, error_scenario)
        qualities_app.append(quality)
    return qualities_app

def get_energies(results_type, app, input_type, vdd, error_scenario="median"):
    energies_app=[]
    for vdd in vdds:
        energy = get_energy(results_type, app, input_type, vdd, error_scenario)
        energies_app.append(energy)
    return energies_app

