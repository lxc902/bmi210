#!/usr/bin/python3
import gensim
import sys
import os
from itertools import islice
import numpy as np
from offline_word2vec_converter import WVConverter
from tokenizer import *

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'

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

