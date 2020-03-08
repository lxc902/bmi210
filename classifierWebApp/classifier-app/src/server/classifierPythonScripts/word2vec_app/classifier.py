#!/usr/bin/python3
import sys
import os
import random
import json

from word2vec_classifier_knn import WVModelKNN
from word2vec_classifier_lgr import WVModelLGR
from word2vec_classifier_svm import WVModelSVM
from saveload import *

URGENCY_CLASSES = ["Urgent0", "Urgent1", "NonUrgent2"]

def main():
  transcript = sys.argv[1]
  print("transcript param = ", transcript)

  mod = sys.argv[2]
  m = load_obj('{}_model'.format(mod))

  predicteds, key_scores = m.predict([transcript])
  print(predicteds)

  predicteds = predicteds[0]
  key_scores = key_scores[0]

  key_scores = [x for x in key_scores if x[1]>0.5]
  key_scores = key_scores[:10]

  keys, scores = zip(*key_scores)
  print(keys)

  writeClassificationToJsonFile([URGENCY_CLASSES[predicteds]], keys, scores)


JSON_OUTPUT_PATH = "output.json"

def writeClassificationToJsonFile(classification, keywords, scores):
  # Current file's dir
  fileDir = str(pathlib.Path(__file__).parent.absolute()) + '/'

  #fileDir = os.path.dirname(os.path.realpath('__file__'))
  filename = os.path.join(fileDir, JSON_OUTPUT_PATH)
  #raise ValueError(filename)
  outFile = open(filename, "w")
  outputJSON = json.loads("{}")
  outputJSON["classification"] = classification
  outputJSON["keywords"] = keywords
  outFile.write(json.dumps(outputJSON, indent=2, sort_keys=True, ensure_ascii=True))
  outFile.close()

if __name__ == "__main__":
  main()

