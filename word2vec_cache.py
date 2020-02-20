#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from word2vec_converter import WVConverter
from tokenizer import *
import pickle

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'

def save_obj(obj, name ):
  with open('obj/'+ name + '.pkl', 'wb') as f:
      pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Returns the vocab which is a dict (string => list of floats),
# meaning word => w2v_vector (300-length float value)
def load_cache():
  return load_obj('word2vec_cache')

def main():
  c = WVConverter()
  allData = read_csv_to_array(data_path)
  allNotes = allData['notelower'].tolist()
  vocab = set()
  for note in allNotes:
    vocab = vocab.union(tokenize(note))
  #print(len(vocab)) # 6797

  vocab = [w for w in vocab if c.in_vocab(w)]
  # print(len(vocab)) # 5120
  with open('vocab.txt', 'w') as f:
    for w in vocab:
      f.write('{}\n'.format(w))
  print('saved {} words in vocab.txt'.format(len(vocab)))

  # Get the vectors of all words in vocab
  vecs = c.get(vocab)
  d = dict()
  for i in range(len(vocab)):
    d[ vocab[i] ] = vecs[i] 
    #if i % 10 == 0:
    #  print(i)

  # Finally, save the cache to disk
  save_obj(d, 'word2vec_cache')
  print('saved {} vectors in obj/ folder'.format(len(vocab)))

if __name__ == "__main__":
  main()
  sys.exit(0)

