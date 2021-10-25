import sys

from pickle_utils import load_pickle

energies    = load_pickle("reports/smartapprox/energies.pck")
crashes     = load_pickle("reports/smartapprox/crashes.pck")
qualities   = load_pickle("reports/smartapprox/qualities.pck")
memory_data = load_pickle("reports/smartapprox/memory_accesses.pck")
energy_data = load_pickle("reports/smartapprox/data_energies.pck")


REPETITIONS         = 100
KEY_CRASH           = "invalid"
KEY_ZERO_QUALITY    = "zero_quality"
APPROXIMATE         = "approximate"
ACCURATE            = "accurate"
NONE                = "none"
NOMINAL_VOLTAGE     = '1.35'
rt                  = "median"
input_type          = "train"
input_types         = [ "train" ]

results_type="axram"
results_types = [
            "axram"
        ]

probabilities_rt={}

probabilities_rt["best"] = {
            1.02 : "2.32675381652E-04",
            1.03 : "5.58854784011E-05",
            1.04 : "1.34229357397E-05",
            1.05 : "3.22400754232E-06",
            1.06 : "7.74362988434E-07",
            1.07 : "1.85991512112E-07",
            1.08 : "4.46726446052E-08",
            1.09 : "1.07297647799E-08",
            1.10 : "2.57714431840E-09",
            1.11 : "6.18995194592E-10",
        }

probabilities_rt["median"] = {
            1.02: "1.61853785504E-01",
            1.03: "3.40572283643E-02",
            1.04: "7.16631248534E-03",
            1.05: "1.50793347269E-03",
            1.06: "3.17298940384E-04",
            1.07: "6.67659544616E-05",
            1.08: "1.40488735001E-05",
            1.09: "2.95616004015E-06",
            1.10: "6.22034370436E-07",
            1.11: "1.30888298586E-07",
        }

probabilities_rt["worst"] = {
            1.02 : "1", 
            1.03 : "1", 
            1.04 : "2.87476835195E-01", 
            1.05 : "4.97220508602E-02", 
            1.06 : "8.59993585245E-03", 
            1.07 : "1.48744662351E-03", 
            1.08 : "2.57269065231E-04", 
            1.09 : "4.44973089309E-05", 
            1.10 : "7.69626344433E-06", 
            1.11 : "1.33114726323E-06",
        }

results_types_labels= {
            "axram"    : "AxRAM",
         }



vdds=[  "%.2f"%v for v in probabilities_rt[rt].keys() ]
vdds.sort()

label_methodologies={
        "best"      : "best",
        "median"    : "median",
        "worst"     : "worst"
                    }
methodologies=list(label_methodologies.keys())


label_classifiers = {
        "euclidean" : "NNA",
        "nn"        : "NN",
        "rfr"       : "RFR",
        "svm"       : "SVM",
        "random"    : "random",
        "nn-c"        : "NN-c",
        "rfr-c"       : "RFR-c",
        "nn-r"        : "NN-r",
        "rfr-r"       : "RFR-r",
        "nn-rq"        : "NN-mr",
        "rfr-rq"       : "RFR-mr",
        }

label_features_lists ={

        }

input_type = "train"

