#!/usr/bin/python3
import gensim
import sys
import os
from itertools import islice
import numpy as np
from saveload import *


# Returns the vocab which is a dict (string => list of floats),
# meaning word => w2v_vector (300-length float value)
def load_cache():
  return load_obj('word2vec_cache')

