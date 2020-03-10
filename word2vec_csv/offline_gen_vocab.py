import numpy as np
import os
import csv
import pandas as pd
import re
from collections import defaultdict
from tokenizer import read_csv_to_array
from tokenizer import tokenize, tokenize_list

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'

def main():
  allData = read_csv_to_array(data_path)
  
  ## Populate the data arrays
  ''' 
  telephonetriage.csv is formatted with the following columns:
  note_deid, notelower, labeled (1 for all notes), label
  '''
  allNotes = allData['notelower'].tolist()

  print(tokenize(allNotes[0]))

  vocab = tokenize_list(allNotes, weights=True)
  #print(vocab)

  l = sorted(vocab.items(), key=lambda x:-x[1])
  #print(l)

  with open('offline_vocab.txt', 'w') as f:
    for w in l:
      f.write('{}\n'.format(w[0]))
  print('saved {} words in vocab.txt'.format(len(vocab)))
  with open('offline_vocab_weights.txt', 'w') as f:
    for w in l:
      f.write('{} {}\n'.format(w[0], w[1]))
  print('saved {} words in vocab_weights.txt'.format(len(vocab)))

if __name__ == "__main__":
  main()

