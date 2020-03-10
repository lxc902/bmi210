#!/usr/bin/python3
import pickle
import os
import pathlib

def save_obj(obj, name ):
  with open('obj/'+ name + '.pkl', 'wb') as f:
      pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
  # Current file's dir
  dir = str(pathlib.Path(__file__).parent.absolute()) + '/'

  with open(dir + 'obj/' + name + '.pkl', 'rb') as f:
      return pickle.load(f)

