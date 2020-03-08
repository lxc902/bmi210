#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np
from tokenizer import *
import random
from projectevalstats import evalstats
from word2vec_classifier_knn import WVModelKNN
from word2vec_classifier_lgr import WVModelLGR
from word2vec_classifier_svm import WVModelSVM

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'

def main():
  allData = read_csv_to_array(data_path)
  allNotes = allData['notelower'].tolist()
  #random.Random(4).shuffle(allNotes)
  allCodes = allData['label'].to_numpy()
  #random.Random(4).shuffle(allCodes)

  train_x = allNotes[:600]
  train_y = allCodes[:600]
  test_x = allNotes[600:]
  test_y = allCodes[600:]
  # print(len(test_x)) # 436

  mods = [
      ('KNN', WVModelKNN), 
      ('LGR', WVModelLGR),
      ('SVM', WVModelSVM),
  ]
  for mod_name, mod_cls in mods:
    model = mod_cls()
    print('start training...')
    model.fit(train_x, train_y)
    print('done training.')
    predicteds, keys = model.predict(test_x)
    #report(test_y, predicteds)
    #print(keys[0])
  
    col_p = [''] * len(allNotes)
    col_k = [''] * len(allNotes)
    for i in range(len(predicteds)):
      col_p[i+600] = predicteds[i]
      col_k[i+600] = str(keys[i])
  
    allData['predicted'] = col_p
    allData['keywords'] = col_k
    outf='telephonetriage_predicted_{}.csv'.format(mod_name)
    allData.to_csv(outf)
  
    print('---------- Model {} Stats ----------'.format(mod_name))
    evalstats(allData[600:])

if __name__ == "__main__":
  main()
  sys.exit(0)

