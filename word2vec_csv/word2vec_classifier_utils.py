#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from word2vec_cache import load_cache
from tokenizer import *
import random
from projectevalstats import evalstats

# word2vec vectors(300-len floats) of words in vocab
w2v = load_cache()

# returns the average vector of a vacab;
# vocab is a set of words in a note.
def average_vec(vocab):
  avg = np.zeros(300)
  size = 0
  #print(avg)
  for w in vocab:
    if w in w2v:
      avg += w2v[w]
      #print(avg)
      size += 1
  avg /= size
  return gensim.matutils.unitvec(avg)

def distance(v1, v2):
  return np.linalg.norm(v1-v2)

def report(real, pred):
  l = len(real)
  correct = len([i for i in range(l) if real[i]==pred[i]])
  print('accuracy:', correct/l)
  print(real)
  print(pred)

