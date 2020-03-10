#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from tokenizer import *
from word2vec_classifier_utils import *
import random
from saveload import *


# A model that calculates the average vector of the words in each note
# and uses that to fit in a KNN-model.
class WVModelKNN:
  def __init__(self):
    self.K = 10

  def fit(self, notes, labels):
    vocabs = [tokenize(note) for note in notes]
    avgs = [average_vec(vocab) for vocab in vocabs]
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return
    self.train_x = avgs
    self.train_y = labels

    save_obj(self, 'knn_model')

  def predict(self, notes):
    '''Return tuples of predcated label(string) and words(list of <word,distance> tuple)'''
    vocabs = [tokenize(note) for note in notes]
    avgs = [average_vec(vocab) for vocab in vocabs]
    #print('---------------')
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return
    preds = []
    keys = []
    for i in range(len(avgs)):
      avg = avgs[i]
      t = len(self.train_x)
      top = sorted([(distance(self.train_x[i], avg), self.train_y[i], i) for i in range(t)])
      #print(top)
      topK = [label for (dis,label,ind) in top[:self.K]]
      p = topK[0]
      for label in topK:
        # predict as the most frequent count in the nearest K entries in train
        if topK.count(label) > topK.count(p):
          p = label
      preds.append(p)

      vocab = vocabs[i]
      words = []
      for w in vocab:
        if w in w2v:
          min_d = 1e10
          for (dis,label,ind) in top[:self.K]:
            if label == p:
              d = distance(w2v[w], self.train_x[i])
              if d < min_d:
                min_d = d
          words.append( (w, min_d) )
      words.sort(key=lambda x:x[1])
      words = words
      keys.append(words)
    return preds, keys

