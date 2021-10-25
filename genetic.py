import sys
import random
from datetime import datetime

from copy import copy
from configuration_SmartApprox import features_lists
from SmartApprox import get_smartapprox, load_base_features, load_knowledge_base, calculate_scores
from SmartApprox import training_apps, test_apps
from metrics_SmartApprox import random_forest_regressor_per_quality
from pickle_utils import *
from pprint import pprint

sys.path.append("..")

test_apps=training_apps

learning_model = "rfr-mr"
input_type="train"
metrics={ learning_model : random_forest_regressor_per_quality }
results_type="axram"

if len(sys.argv)>1:
    error_scenario=sys.argv[1]
    print(error_scenario)
else:
    error_scenario="median"

max_generation=5000
max_stagnation=250

initial_mutation_probability = 0.05
mutation_pop_probability=0.5
mutation_probability = initial_mutation_probability
quality_requirement=0.9
growing_mutation_prob=1.2

POPULATION="population"
SCORE="score"
NEW_INDIVIDUALS="new individuals"
SMARTAPPROX="smartapprox"

#########################################################
#           ROUTINES
#########################################################

log_ga_activated=True
def log(string):
    if log_ga_activated:
        print(string)


def is_enough(population, generation, stagnation):
    return generation > max_generation or stagnation > max_stagnation

def mutation_prob(mutation_probability):
    return random.random() < mutation_probability


#population is a dict ( str, list(str) )
def select_individuals(population):
    pos_ind1 = random.randint(0, len(population)-1)
    pos_ind2 = pos_ind1

    #avoiding choosing twice the same individual
    while pos_ind2 == pos_ind1:
        pos_ind2 = random.randint(0, len(population)-1)

    population_keys=list(population.keys())
    return population_keys[pos_ind1], population_keys[pos_ind2]
    
def mutate(individual, features_base):
    list_features_base=list(features_base)
    removed_element=None
    log("\t\tMutation of individual " + str(individual))

    if random.random() < mutation_pop_probability:
        pos_individual = random.randint(0, len(individual)-1)
        removed_element = individual[pos_individual]
        individual.remove(removed_element)
        log("\t\tMutation - removing " + str(removed_element))

    pos_features   = random.randint(0, len(features_base)-1)
    #avoiding the change for a feature that are in the individual
    while list_features_base[pos_features] in individual + [removed_element]:
        pos_features   = random.randint(0, len(features_base)-1)

    log("\t\tMutation - adding " + str(list_features_base[pos_features]))
    individual.append(list_features_base[pos_features])
    return individual

def cross_individuals(indv1, indv2):
    split_indv1 = random.randint(0, len(indv1) - 1)
    split_indv2 = random.randint(0, len(indv2) - 1)

    new_indv1 = list(set(indv1[:split_indv1] + indv2[split_indv2:]))
    new_indv2 = list(set(indv2[:split_indv2] + indv1[split_indv1:]))

    return new_indv1, new_indv2

def initial_population(features_base, size=10):
    #population = features_lists
    population={}
    features = [ "MEB" , "CE", "DS", "MA", "MI", "EI" ]
    for feature_set in features:
        population[feature_set] = features_lists[feature_set]


    for i in range(size - len(population)):
        list_features_base = list(features_base)
        #size of the new individual
        n_features = random.randint(0, len(features_base)-1)

        new_individual=[]
        for f in range(n_features):
            pos_feature = random.randint(0, len(list_features_base)-1)
            #while list_features_base[pos_feature] not in new_individual:
            #    pos_feature = random.randint(0, len(features_base)-1)
            new_individual.append(list_features_base[pos_feature])
            list_features_base.pop(pos_feature)

        population["rand"+str(i)] = new_individual

    return population





#########################################################
#          KERNEL 
#########################################################
log("Starting at " + str(datetime.now()))
log("error scenario>" + error_scenario)


#initialization
genetic=[]
generation=0
stagnation=0
random.seed(42)

base            = load_base_features()

features_base=set()
excluded_features=['D$ writebacks']
for app in base.keys():
    for input_type in base[app].keys():
        for feature in base[app][input_type].keys():
            if feature not in excluded_features:
                features_base.add(feature)

log("Features("+str(len(features_base))+") = " + str(features_base))
log("Training apps("+str(len(training_apps))+") = " + str(training_apps))
log("Test apps("+str(len(test_apps))+") = " + str(test_apps))

population=initial_population(features_base)

knowledge_base  = load_knowledge_base(training_apps, base, quality_requirement, error_scenario, results_type, input_type)

pprint(population)

smartapprox           = get_smartapprox(  test_apps, 
                              knowledge_base, 
                              metrics, 
                              population,
                              results_type, 
                              input_type, 
                              error_scenario,
                              base,
                            )

log(smartapprox.keys())
features_score = calculate_scores(smartapprox, population.keys())

score_population = [ ( features_score[individual_key], individual_key ) for individual_key in population.keys()  ]

genetic.append( {
            POPULATION  : copy(population),
            SCORE       : copy(score_population),
            SMARTAPPROX : copy(smartapprox),
        } )

#log("Initial population("+str(len(population))+") =  "+str(population.keys()))
print("\n\n----------------------------------->INITIAL POPULATION<-----------------------------------")
score_population.sort()
for score, key in score_population:
    print("key="+key+", score="+str(score))
    pprint(population[key])

score_population.sort()

log("Score = "+ str(score_population))

#main loop
while (not is_enough(population, generation, stagnation)):
    generation+=1
    log("\n>>>>>>Generation " + str(generation) + " - mutation_probability: "+("%.2f"%mutation_probability) + " - stagnation: " + str(stagnation)+ " - time: " + str(datetime.now()))

    key_ind1, key_ind2 = select_individuals(population)
    log("\tselected individuals: ")
    log("\t\t"+ str(key_ind1))
    log("\t\t"+ str(key_ind2))

    n_ind1, n_ind2 = cross_individuals(population[key_ind1], population[key_ind2])

    random.shuffle(n_ind1)
    random.shuffle(n_ind2)

    if (mutation_prob(mutation_probability)):
        log("\tMutation on ind1-----")
        mutate(n_ind1, features_base)

    if (mutation_prob(mutation_probability)):
        log("\tMutation on ind2-----")
        mutate(n_ind2, features_base)

    while True:
        n_ind1_repeated = False
        n_ind2_repeated = False
        for individual in population.values():
            if set(individual) == set(n_ind1):
                mutate(n_ind1, features_base)
                n_ind1_repeated = True

            if set(individual) == set(n_ind2):
                mutate(n_ind2, features_base)
                n_ind2_repeated = True
        if not n_ind1_repeated and not n_ind2_repeated:
            break

    new_generation = {}
    if not n_ind1_repeated:
        new_generation["gen"+str(generation)+"-ind1"] = n_ind1
    if not n_ind2_repeated:
        new_generation["gen"+str(generation)+"-ind2"] = n_ind2

    if len(new_generation)==0:
        mutation_probability *= 2
        log("\n\t-- no new individuals in this generation -- ")
        stagnation+=1
        continue

    #elif len(new_generation) == 2:
    #    mutation_probability = initial_mutation_probability

    log("\n\tnew individuals: ")
    for k in new_generation.keys():
        log("\t\t"+ k + ": " + str(list(new_generation[k])))


    smartapprox_new = get_smartapprox(test_apps, 
                          knowledge_base, 
                          metrics, 
                          new_generation,
                          results_type, 
                          input_type, 
                          error_scenario,
                          base
                          )

    features_score = calculate_scores(smartapprox_new, new_generation.keys())


    score_new        = [ ( features_score[individual_key], individual_key ) for individual_key in new_generation.keys()  ]

    score_population.sort()
    score_new.sort(reverse=True)

    #log("\tPopulation Score = "+ str(score_population))
    log("\tNew Generation Score = "+ str(score_new))

    discarded=0
    replace=0
    POS_SCORE=0
    POS_KEY=1
    for sn in score_new:
        if sn[POS_SCORE] > score_population[replace][POS_SCORE]:
            log("\t\t"+sn[POS_KEY]+ " has better score than "+ score_population[replace][POS_KEY])
            population.pop( score_population[replace][POS_KEY] )
            score_population[replace] = ( sn[POS_SCORE], sn[POS_KEY] )
            population[sn[POS_KEY]] = new_generation[sn[POS_KEY]]
            replace+=1
            stagnation=0
            mutation_probability = initial_mutation_probability
        else:
            discarded+=1

    #if both new individuals were discarded
    if discarded==len(new_generation):
        stagnation+=1
        mutation_probability *= growing_mutation_prob

    genetic.append( {
                POPULATION      : copy(population),
                SCORE           : copy(score_population),
                NEW_INDIVIDUALS : new_generation,
                SMARTAPPROX     : smartapprox_new,
            } )

    log("\n\tCurrent Population: ")
    #for k in new_generation.keys()
    log("\t\t"+  str(list(population.keys())))


print("\n\n----------------------------------->FINAL POPULATION<-----------------------------------")
score_population.sort()
for score, key in score_population:
    print("key="+key+", score="+str(score))
    pprint(population[key])

#dump_pickle(genetic, "reports/genetic_"+error_scenario+".pck")

print("Ending at "+ str(datetime.now()))
