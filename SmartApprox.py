#!/usr/bin/env python
__author__ = "João Fabrício Filho"
__version__ = "0.0.1"

import numpy as np
import sys

from random import random
from random import seed
from scipy.spatial import distance
from copy import copy

from metrics_SmartApprox import euclidean_metric
from metrics_SmartApprox import svm_metric
from metrics_SmartApprox import random_metric
from metrics_SmartApprox import nn_regressor, nn_classifier
from metrics_SmartApprox import random_forest_regressor, random_forest_classifier
from metrics_SmartApprox import random_forest_regressor_per_quality
from metrics_SmartApprox import nn_regressor_per_quality

from pickle_utils import *

from configuration_SmartApprox import *

seed(42)

metrics={  
#            "NNA"           : euclidean_metric, 
#            "SVM"           : svm_metric,
#            "RF-r"          : random_forest_regressor,
#            "RF-c"          : random_forest_classifier,
            "RF-mr"         : random_forest_regressor_per_quality,
#            "NN-c"          : nn_classifier,
#            "NN-r"          : nn_regressor,
#            "NN-mr"         : nn_regressor_per_quality,
#            "random"        : random_metric,
        }

quality_requirement=0.9

#error_scenario="best"
error_scenario="median"
#error_scenario="worst"

results_type="axram"

log_activated=True
#log_activated=False

################################################################################
# LOADING FEATURES
################################################################################
#base=info_mem
#base=info_instrs
from common_params import *

def load_base_features(input_type="train"):
    from extract_memory_data import info_mem
    from extract_instrs import info_instrs, norm_instrs
    from extract_dram_energy import dram_energy, dram_cmd
    base={}
    max_features={}
    for app in info_mem.keys():
        for mem_feature in info_mem[app][input_type].keys():
            if mem_feature not in max_features.keys() or max_features[mem_feature] < info_mem[app][input_type][mem_feature]:
                max_features[mem_feature] = info_mem[app][input_type][mem_feature]
        for inst_feature in info_instrs[app][input_type].keys():
            if inst_feature not in max_features.keys() or max_features[inst_feature] < info_instrs[app][input_type][inst_feature]:
                max_features[inst_feature] = info_instrs[app][input_type][inst_feature]

        #for norm_inst_feature in norm_instrs[app][input_type].keys():
        #    if norm_inst_feature not in max_features.keys() or max_features[norm_inst_feature] < norm_instrs[app][input_type][norm_inst_feature]:
        #        max_features[norm_inst_feature] = norm_instrs[app][input_type][norm_inst_feature]

        for dram_energy_feature in dram_energy[app][input_type].keys():
            if dram_energy_feature not in max_features.keys() or max_features[dram_energy_feature] < dram_energy[app][input_type][dram_energy_feature]:
                max_features[dram_energy_feature] = dram_energy[app][input_type][dram_energy_feature]

        for dram_cmd_feature in dram_cmd[app][input_type].keys():
            if dram_cmd_feature not in max_features.keys() or max_features[dram_cmd_feature] < dram_cmd[app][input_type][dram_cmd_feature]:
                max_features[dram_cmd_feature] = dram_cmd[app][input_type][dram_cmd_feature]

    #print max_features

    ################################################################################
    # NORMALIZING FEATURES
    ################################################################################

    for app in info_mem.keys():
        base[app]={}
        for input_type in input_types:
            base[app][input_type]={}
            for mem_feature in info_mem[app][input_type].keys():
                base[app][input_type][mem_feature] = info_mem[app][input_type][mem_feature] / float(max_features[mem_feature])

            for inst_feature in info_instrs[app][input_type].keys():
                base[app][input_type][inst_feature] = info_instrs[app][input_type][inst_feature] / float(max_features[inst_feature])

            #for norm_inst_feature in norm_instrs[app][input_type].keys():
            #    base[app][input_type][norm_inst_feature] = norm_instrs[app][input_type][norm_inst_feature] / float(max_features[norm_inst_feature])

            for dram_energy_feature in dram_energy[app][input_type].keys():
                base[app][input_type][dram_energy_feature] = dram_energy[app][input_type][dram_energy_feature] / float(max_features[dram_energy_feature])

            for dram_cmd_feature in dram_cmd[app][input_type].keys():
                base[app][input_type][dram_cmd_feature] = dram_cmd[app][input_type][dram_cmd_feature] / float(max_features[dram_cmd_feature])
    return base


################################################################################
# ROUTINES 
################################################################################

from common_params import *


from pprint import pprint


from SmartApprox_routines import *



def log(string):
    if log_activated:
        print(string)

################################################################################
# LOADING KNOWLEDGE BASE 
################################################################################
def load_knowledge_base(training_apps, base, quality_requirement, error_scenario, results_type, input_type):
    knowledge_base={}
    training_apps.sort()
    log("knowledge base for quality requirement "+str(quality_requirement) )
    for ta in training_apps:
        log("\t" + ta)
        oracle_level        = get_best_approx_level(ta, quality_requirement, error_scenario) 
        qualities_app       = get_qualities(results_type, ta, input_type, vdds, error_scenario)
        energies_app        = get_energies(results_type, ta, input_type, vdds, error_scenario)
        knowledge_base[ta]  = ( base[ta][input_type], qualities_app, oracle_level )

        oracle_quality      = get_quality(results_type, ta, input_type, oracle_level, error_scenario)

        log("\t\t vdd: "+str(oracle_level))
        log("\t\t quality: "+ str(oracle_quality))

        out="\t\t qualities> " 
        for q in qualities_app:
            out += "%.2f, " % q
        log(out)
        out="\t\t energies> " 
        for e in energies_app:
            out += "%.2f, " % e
        log(out)
        #log("\t\t qualities> " + str(qualities_app))
        #log("\t\t energies> " + str(energies_app))
    return knowledge_base


################################################################################
# KERNEL
################################################################################
def get_smartapprox(test_apps, knowledge_base, metrics, features_lists, results_type, input_type, error_scenario, base):
    smartapprox={}
    for app in test_apps:
        smartapprox[app]={}
        log(app)

        #for vdd in vdds:
        #    log("\tvdd: ")
        current_kb = copy(knowledge_base)
        current_kb.pop(app)

        for metric_name in metrics.keys():
            smartapprox[app][metric_name]={}
            log("\t"+metric_name)
            metric = metrics[metric_name]

            for fl in features_lists.keys():
                features_list = features_lists[fl]
                if metric_name != "random":
                    log("\t\t features_list> " + fl)
                else:
                    fl = 'random'


                #qualities_app, instance = metric(base[app][input_type], current_kb, features_list)
                approx_level, instance = metric(base[app][input_type], current_kb, features_list)

                log("\t\t similar: "+instance + " - vdd: " + str(approx_level) )

                #log(instance)
                #plog([ knowledge_base[instance][0][f] for f in features_list ] )
                #log(app)
                #plog([ base[app][input_type][f] for f in features_list ])

                #prob=get_prob(approx_level)
                quality = get_quality(results_type, app, input_type, approx_level, error_scenario)
                energy = get_energy(results_type, app, input_type, approx_level, error_scenario)

                #min_energy = 1.0
                #approx_level = NOMINAL_VOLTAGE
                #for i in range(len(qualities_app)):
                #    vdd = vdds[i]
                #    quality = qualities_app[i]

                #    energy = get_energy(results_type, app, input_type, vdd, error_scenario)
                #    if quality >= quality_requirement and energy < min_energy:
                #        min_energy = energy
                #        approx_level = vdd

                smartapprox[app][metric_name][fl]=(approx_level, quality, energy, instance)
                #crashed_executions  = set()
                #for crash_type in crashes[results_type][app][input_type][probability].keys():
                #    crashed_executions  = crashed_executions.union(crashes[results_type][app][input_type][probability][crash_type])
                #perc_crashes = len(crashed_executions) / float(REPETITIONS)

                log("\t\t quality: "+ str(quality))
                #log("\t\t crashed: "+ str(perc_crashes))
                print

                if metric_name == "random":
                    break
            #end for fl in features_list.keys():
        #end for metric_name in metrics.keys():
        oracle_level    = get_best_approx_level(app, quality_requirement, error_scenario) 
        oracle_quality  = get_quality(results_type, app, input_type, oracle_level, error_scenario)
        oracle_energy   = get_energy(results_type, app, input_type, oracle_level, error_scenario)
        #oracle_energy   = float(oracle_level)
        log("\toracle>> vdd: "+str(oracle_level))
        log("\t\t quality: "+ str(oracle_quality))
        smartapprox[app]['oracle']=(oracle_level, oracle_quality, oracle_energy, 'oracle')
    #end for app in test_apps
    return smartapprox


################################################################################
# CALCULATING METRICS AND FEATURES PERFORMANCES
################################################################################

def calculate_scores(smartapprox, features_lists):
    scores={}
    all_avgs={}
    all_avgs['oracle']=[]
    for app in smartapprox.keys():
        oracle_level, oracle_quality, oracle_energy, oracle_similar = smartapprox[app]['oracle']
        all_avgs['oracle'].append( (oracle_quality, oracle_energy) )
        for metric in smartapprox[app].keys():
            if metric == 'oracle':
                continue
            if metric not in scores.keys():
                scores[metric]=[]
            if metric not in all_avgs.keys():
                all_avgs[metric]=[]
            for features_list in smartapprox[app][metric].keys():

                if features_list not in scores.keys():
                    scores[features_list]=[]
                if features_list not in all_avgs.keys():
                    all_avgs[features_list]=[]

                level, quality, energy, similar = smartapprox[app][metric][features_list]

                score_quality   = (quality / oracle_quality) if quality < oracle_quality else 1.0
                score_energy    = (oracle_energy / energy) if energy > oracle_energy else 1.0
                #score_qe        = score_quality * score_energy])
                score = score_quality * score_energy

                scores[features_list].append(score)
                scores[metric].append(score)

                all_avgs[features_list].append( ( quality, energy ))
                all_avgs[metric].append( ( quality, energy ))

    log("--SCORE FOR LEARNING MODELS--")
    for k in metrics:
        log(k+": "+str(np.mean(scores[k])))

    log("\n--SCORE FOR FEATURE SETS--")
    score_features={}
    for k in features_lists:
        log(k+": "+str(np.mean(scores[k])))
        score_features[k] = np.mean(scores[k])

    log("")
    #log("random: "+str(np.mean(scores['random'])))

    #plog(scores)

    #sys.exit(0)
    #return score_features
    return all_avgs, scores


if __name__ == "__main__":
    log("-----------------> SmartApprox <---------------------------")
    log("Results built upon " + results_type)
    log("Error Scenario:" + error_scenario)
    log("\n\n-----------------> TRAINING PHASE <---------------------------")
    base=load_base_features()
   
    knowledge_base=load_knowledge_base(training_apps, base, quality_requirement, error_scenario, results_type, input_type)

    log("\n\n-----------------> RUNTIME EVALUATION <---------------------------")

    smartapprox=get_smartapprox(test_apps, knowledge_base, metrics, features_lists, results_type, input_type, error_scenario, base)

    log("\n\n-----------------> CALCULATING SCORES <---------------------------")


    all_avgs, scores = calculate_scores(smartapprox, features_lists)

    oracle_qualities=[]
    oracle_energies=[]
    all_qualities=[]
    all_energies=[]
    all_qs=[]
    all_es=[]
    all_scores=[]

    log("app,features_set,Q_{score},E_{score},Score")
    for app in smartapprox.keys():
        oracle_level, oracle_quality, oracle_energy, oracle_similar = smartapprox[app]['oracle']
        oracle_qualities.append(oracle_quality)
        oracle_energies.append(oracle_energy)

        for metric in smartapprox[app].keys():
            if metric == 'oracle':
                continue
            features_lists= list(smartapprox[app][metric].keys())
            features_lists.sort(key=str.casefold)
            for features_list in features_lists:

                if metric == 'random':
                    ##
                    features_list="random"
                    continue

                level, quality, energy, similar = smartapprox[app][metric][features_list]

                all_qualities.append(quality)
                all_energies.append(energy)

                score_quality   = (quality / oracle_quality) if quality < oracle_quality else 1.0
                score_energy    = (oracle_energy / energy) if energy > oracle_energy else 1.0
                #score_qe        = score_quality * score_energy])
                score = score_quality * score_energy

                all_qs.append(score_quality)
                all_es.append(score_energy)
                all_scores.append(score)

                log(app+"|"+features_list+"|"+str(quality)+"|"+str(energy)+"|"+str(oracle_quality)+"|"+str(oracle_energy)+"|"+str(score))

    log("\n\n\n###############################")
    log("oracle:")
    log("\tavg quality:" + str(np.mean(oracle_qualities)))
    log("\tavg energy:" + str(np.mean(oracle_energies)))

    log("\nSmartApprox:")
    log("\tavg quality:" + str(np.mean(all_qualities)))
    log("\tavg energy:" + str(np.mean(all_energies)))
    log("\tavg score quality:" + str(np.mean(all_qs)))
    log("\tavg score energy:" + str(np.mean(all_es)))
    log("\tavg score:" + str(np.mean(all_scores)))

    dump_pickle(smartapprox, 'reports/smartapprox_'+error_scenario+'.pck')
    dump_pickle(all_avgs, 'reports/all_avgs_'+error_scenario+'.pck')
    #dump_pickle(scores, 'reports/score_'+error_scenario+'.pck')
