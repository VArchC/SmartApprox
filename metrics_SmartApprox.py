from common_params import NOMINAL_VOLTAGE
import numpy as np

QUALITY_REQUIREMENT=0.9

POS_FEATURES=0
POS_QUALITIES_VDD=1
POS_BEST_VDD=2

def get_nearest_vdd(pred_vdd, vdds):
    vdd=pred_vdd
    min_diff=float('inf')
    for v in vdds:
        diff = np.abs(pred_vdd - float(v))
        if diff < min_diff:
            min_diff = diff
            vdd = v

    return vdd


def nn_regressor(data, knowledge_base, features_names):
    from sklearn.neural_network import MLPRegressor
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ float(knowledge_base[app][POS_BEST_VDD]) for app in training_apps ]
    #Y_train = [ knowledge_base[app][POS_QUALITIES_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2),
                        random_state=1, max_iter=5000)
    clf.fit(X_train, Y_train)

    test_Y = clf.predict([ test_X ])

    pred_vdd = test_Y[0]
    vdd = get_nearest_vdd(pred_vdd, vdds)

    return vdd, ''

def nn_regressor_per_quality(data, knowledge_base, features_names):
    from sklearn.neural_network import MLPRegressor
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    #Y_train = [ float(knowledge_base[app][POS_BEST_VDD]) for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_QUALITIES_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2),
                        random_state=1, max_iter=5000)
    clf.fit(X_train, Y_train)

    test_Y = clf.predict([ test_X ])

    pred_vdd = test_Y[0]
    for i in range(len(vdds)):
        if pred_vdd[i] >= QUALITY_REQUIREMENT:
            return vdds[i], ''
    return NOMINAL_VOLTAGE, ''


def nn_classifier(data, knowledge_base, features_names):
    from sklearn.neural_network import MLPClassifier
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_BEST_VDD] for app in training_apps ]
    #Y_train = [ knowledge_base[app][POS_QUALITIES_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1, max_iter=5000)
    clf.fit(X_train, Y_train)

    test_Y = clf.predict([ test_X ])
    vdd = test_Y[0]

    return vdd, ''


def svm_metric(data, knowledge_base, features_names):
    from sklearn import svm

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_BEST_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    clf = svm.SVC(kernel='rbf')
    clf.fit(X_train, Y_train)

    test_Y = clf.predict([ test_X ])

    return test_Y[0], ''


def euclidean_metric(data, knowledge_base, features_names):
    source_vector = [ data[feature_name] for feature_name in features_names ]
    from scipy.spatial import distance
    training_apps = knowledge_base.keys()
    min_distance = float('inf')
    for app in training_apps:
        comp_vector = [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names ]
        dist = distance.euclidean(source_vector, comp_vector)
        if dist < min_distance:
            min_distance = dist
            similar_app  = app
    return knowledge_base[similar_app][POS_BEST_VDD], similar_app

def random_forest_regressor(data, knowledge_base, features_names):
    from sklearn.ensemble import RandomForestRegressor
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_BEST_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(X_train, Y_train)
    
    test_Y = regr.predict([ test_X ])

    pred_vdd = test_Y[0]
    vdd = get_nearest_vdd(pred_vdd, vdds)

    return vdd, ''

def random_forest_classifier(data, knowledge_base, features_names):
    from sklearn.ensemble import RandomForestClassifier
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_BEST_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    regr = RandomForestClassifier(max_depth=2, random_state=0)
    regr.fit(X_train, Y_train)
    
    test_Y = regr.predict([ test_X ])

    vdd = test_Y[0]
    #vdd = get_nearest_vdd(pred_vdd, vdds)

    return vdd, ''


def random_forest_regressor_per_quality(data, knowledge_base, features_names):
    from sklearn.ensemble import RandomForestRegressor
    from common_params import vdds

    training_apps = knowledge_base.keys()
    X_train = [ [ knowledge_base[app][POS_FEATURES][feature_name] for feature_name in features_names] for app in training_apps ]
    Y_train = [ knowledge_base[app][POS_QUALITIES_VDD] for app in training_apps ]
    test_X  = [ data[feature_name] for feature_name in features_names ]

    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(X_train, Y_train)
    
    test_Y = regr.predict([ test_X ])

    pred_vdd = test_Y[0]
    for i in range(len(vdds)):
        if pred_vdd[i] >= QUALITY_REQUIREMENT:
            return vdds[i], ''
    return NOMINAL_VOLTAGE, ''
    #sys.exit(0)
    #vdd = get_nearest_vdd(pred_vdd, vdds)

   # return vdd, ''

def random_metric(data, knowledge_base, features):
    from random import randint
    pos = randint(0, len(knowledge_base)-1)
    #print(len(knowledge_base))
    #print(pos)
    similar_app = list(knowledge_base.keys())[pos]
    return  knowledge_base[similar_app][POS_BEST_VDD], similar_app
