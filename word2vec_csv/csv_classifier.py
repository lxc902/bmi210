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
from saveload import *

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'


#enable_train = False
enable_train = True

URGENCY_CLASSES = ["Urgent0", "Urgent1", "NonUrgent2"]
def offline_keywords(true_labels, pred_labels, keylists, mod_name):
  n = len(true_labels)
  fn = 'offline/offline_keywords_{}.txt'.format(mod_name)
  with open(fn, 'w') as f:
    for cls in range(3):
      f.write('-------- class {} ({}) --------\n'.format(cls, URGENCY_CLASSES[cls]))
      keys = []
      for i in range(n):
        if int(true_labels[i]) == cls and pred_labels[i] == cls:
          keys += keylists[i]

      # dedupe
      old_keys = keys
      keys = []
      s = dict() # sum
      cnt = dict()
      for x in old_keys:
        if x[0] not in s:
          s[x[0]] = 0
          cnt[x[0]] = 0
        s[x[0]] += x[1]
        cnt[x[0]] += 1
      for w in s:
        keys += [ (w, s[w]/cnt[w]) ]

      # sort
      if mod_name == 'knn':
        keys.sort(key=lambda x:x[1])
      else:
        keys.sort(key=lambda x:-x[1])

      for x in keys[:100]:
        f.write('{:<20}{:.10f}\n'.format(x[0], x[1]))
      f.write('\n\n')


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
    if enable_train:
      model = mod_cls()
      print('start training...', end='', flush=True)
      model.fit(train_x, train_y)
      print('done')
    else:
      model = load_obj('{}_model'.format(mod_name.lower()))

    predicteds, keylists = model.predict(test_x)
    #report(test_y, predicteds)
    #print(keylists[0])

    offline_keywords(test_y, predicteds, keylists, mod_name.lower())
  
    col_p = [''] * len(allNotes)
    col_k = [''] * len(allNotes)
    for i in range(len(predicteds)):
      col_p[i+600] = predicteds[i]
      col_k[i+600] = str(keylists[i])
  
    allData['predicted'] = col_p
    allData['keywords'] = col_k
    outf='telephonetriage_predicted_{}.csv'.format(mod_name)
    allData.to_csv(outf)
  
    print('---------- Model {} Stats ----------'.format(mod_name))
    evalstats(allData[600:])

if __name__ == "__main__":
  main()
  sys.exit(0)

