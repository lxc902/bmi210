#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from tokenizer import *
from word2vec_classifier_utils import *
from saveload import *


# A model that calculates the average vector of the words in each note
# and uses that to fit in a SVM.
class WVModelSVM:
  def __init__(self):
    from sklearn.svm import SVC
    self.m = SVC(kernel='linear', gamma='auto', probability=True)
    #LogisticRegression(n_jobs=-1, C=1e2, solver='liblinear')
  
  def fit(self, notes, labels):
    vocabs = [tokenize(note) for note in notes]
    avgs = [average_vec(vocab) for vocab in vocabs]
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return 
    self.m.fit(avgs, labels)

    save_obj(self, 'svm_model')

  def predict(self, notes):
    '''Return tuples of predcated label(string) and words(list of <word,distance> tuple)'''
    vocabs = [tokenize(note) for note in notes]
    avgs = [average_vec(vocab) for vocab in vocabs]
    #print('---------------')
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return 
    preds = self.m.predict(avgs)
    #print(preds)

    keys = []
    for i in range(len(notes)):
      vocab = vocabs[i]
      avg = avgs[i]
      words = []
      for w in vocab:
        if w in w2v:
          prob = self.m.predict_proba( [ w2v[w] ] )
          words.append( (w, prob[0][ preds[i] ] ) )
          # print(prob.shape) # (1, 3)
          # print(prob)
          # sys.exit(0)
      words.sort(key=lambda x:-x[1])
      keys.append(words)

    return preds, keys

