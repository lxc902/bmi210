import numpy as np
import os
import csv
import pandas as pd
import re
from collections import defaultdict


'''
This is a program to take in a labeled file and train a unigram classifier to
  triage based on pre-labeled cases

Currently just operates on telephonetriage.csv, which is in the same dir as 
  this program
'''

# Data
training_data = []
dev_data = []
test_data = []
vocab = set([])

# Regular Expressions
phoneREs = [
'\((\d\d\d)\)(\d\d\d)-(\d\d\d\d)',
'\((\d\d\d)\) (\d\d\d)-(\d\d\d\d)',
'(\d\d\d)-(\d\d\d)-(\d\d\d\d)',
'\+1 (\d\d\d) (\d\d\d) (\d\d\d\d)',
'\+1 (\d\d\d) (\d\d\d)-(\d\d\d\d)'
]

dateREs = [
'\d+/\d+/\d+',
'\d+/\d+',
'��\d+/\d+/\d+',
'\d+-\d+-\d+'
]

timeREs = [
'\d\d:\d\d',
'\d\d:\d\d',
'am',
'pm',
'phone',
]

otherREs = [
'crm', 
'\d\d\d\d\d\d\d',
'-----',
'message',
'from',
'�',
'(\w+)@(\w+).(\w+)'
]

REs = [phoneREs, dateREs, timeREs, otherREs]


# Code
def read_csv_to_array(filePath):
  with open(filePath, 'r') as infile:
    df = pd.read_csv(infile)
    # reader = csv.reader(infile)
    # destList = list(reader)
    return df

def trim_notes(notes):
  '''
  Intended to bring some standardization to the notes such as:
    pt --> patient
    remove time stamps
    remove crm codes
    etc.
  Not complete -- Needs more RegExes to get more informative words
  '''
  
  new_notes = []
  for note in notes:
    new_note = note.split()
    for RElist in REs:
      for RE in RElist:
        pattern = re.compile(RE)
        new_note = [i for i in new_note if not re.match(pattern, i)]
    
    for i, word in enumerate(new_note):
      if word == "pt":
        new_note[i] = "patient"
      parens = re.compile(r'\(.*\)$')
      if re.match(parens, word):
        new_note[i] = ''.join(c for c in word if c not in ['(',')'])
    new_notes.append(' '.join(new_note))  
  return new_notes

def trim_word(word):
  r = ''
  for c in word:
    if c>='a' and c<='z':
      r+=c
  return r

# Current file's dir
import pathlib
whitelisted_path = str(pathlib.Path(__file__).parent.absolute()) + '/tokenizer_whitelisted_words.txt'
whitelisted_words = set()
whitelisted_words_loaded = False
def load_whitelisted_words():
  global whitelisted_words
  global whitelisted_words_loaded
  try:
    with open(whitelisted_path) as f:
      for w in f:
        whitelisted_words.add(w.split()[0])
      whitelisted_words_loaded = True
  except e:
    print('skip loading whitelist: ', e)
    whitelisted_words_loaded = False

load_whitelisted_words()
#print(whitelisted_words)

# Returns a set of words in a list of notes
def tokenize_list(notes, weights=False):
  if not weights: # just vocab
    vocab = set()
  else:
    vocab = dict()
  notes = trim_notes(notes)
  for note in notes:
    # build vocab for note
    words = note.split(' ')
    for word in words:
      w = trim_word(word)
      if not w:  # remove ''
        continue
      if whitelisted_words_loaded and w not in whitelisted_words:
        continue # remove skipped
      if not weights:
        if w not in vocab:
          vocab.add(w)
      else:
        if w not in vocab:
          vocab[w] = 1
        else:
          vocab[w] += 1
  return vocab

# Returns a set of words in a note
def tokenize(note, weights=False):
  return tokenize_list([note], weights)


