
import os.path
import pickle

def dump_pickle(data, filename):
    dbfile = open(filename, "wb")
    pickle.dump(data, dbfile)

def load_pickle(filename):
    if(os.path.exists(filename)):
        dbfile = open(filename, "rb")
        return pickle.load(dbfile)
    else:
        return {}

def append_pickle(data, filename):
    old_data = load_pickle(filename)
    data_to_save = ( data , old_data )
    dump_pickle(data_to_save, filename)

def initialize_pickle(filename):
    dump_pickle([], filename)
    



