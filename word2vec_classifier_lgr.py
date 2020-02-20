#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from word2vec_cache import load_cache
from tokenizer import *

# word2vec vectors(300-len floats) of words in vocab
w2v = load_cache()

# returns the average vector of a note
def average_vec(note):
  vocab = tokenize(note)
  avg = np.zeros(300)
  size = 0
  #print(avg)
  for w in vocab:
    if w in w2v:
      avg += w2v[w]
      #print(np.linalg.norm(w2v[w]))
      #if size > 10:
      #  break
      size += 1
  avg /= size
  return gensim.matutils.unitvec(avg)

# A model that calculates the average vector of the words in each note
# and uses that to fit in a LogisticRegression.
class WVModel:
  def __init__(self):
    from sklearn.linear_model import LogisticRegression
    self.m = LogisticRegression()
  
  def fit(self, notes, labels):
    avgs = [average_vec(note) for note in notes]
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return 
    self.m.fit(avgs, labels)

  def predict(self, notes):
    avgs = [average_vec(note) for note in notes]
    #print('---------------')
    #for i in range(10):
    #  print(avgs[i][:10])
    #  print(np.linalg.norm(avgs[i]))
    #return 
    return self.m.predict(avgs)

def report(real, pred):
  l = len(real)
  correct = len([i for i in range(l) if real[i]==pred[i]])
  print('accuracy:', correct/l)
  print(real)
  print(pred)

def main():
  allData = read_csv_to_array(data_path)
  allNotes = allData['notelower'].tolist()
  allCodes = allData['label'].to_numpy()

  train_x = allNotes[:600]
  train_y = allCodes[:600]
  test_x = allNotes[600:]
  test_y = allCodes[600:]
  # print(len(test_x)) # 436

  model = WVModel()
  print('start training...')
  model.fit(train_x, train_y)
  print('done training.')
  predicted = model.predict(test_x)
  report(test_y, predicted)

  #allData[] = 
  outf='telephonetriage_predicted.csv'

if __name__ == "__main__":
  main()
  sys.exit(0)

