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

def union2(dict1, dict2):
  from collections import Counter 
  return Counter(dict1) + Counter(dict2)

def main():
  allData = read_csv_to_array(data_path)
  allNotes = allData['notelower'].tolist()
  vocab = set()
  #vocab = dict() # for Print3 below
  for note in allNotes:
    vocab = vocab.union(tokenize(note))
    #vocab = dict(union2(vocab, tokenize(note, weights=True))) # for Print3 below
  #print(len(vocab)) # 6797

  c = WVConverter()

  ## Print3 out non-vocab words
  #x = []
  #for w in vocab:
  #  if not c.in_vocab(w):
  #    x += [(w, vocab[w])]
  #x.sort(key=lambda y: -y[1])
  #[print(y) for y in x]
  #sys.exit(0) # Print3

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

