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

# Paths
cur_dir = os.getcwd()
data_path = cur_dir + '/telephonetriage.csv'

# Data
training_data = []
dev_data = []
test_data = []
vocab_freq = defaultdict()
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

def get_vocab(notes):
	# build vocab from notes
	for note in notes:
		words = note.split(' ')
		for word in words:
			if word in vocab_freq:
				vocab_freq[word] += 1
			else:
				vocab_freq[word] = 1
			if word not in vocab:
				vocab.add(word)


def main():
	allData = read_csv_to_array(data_path)
  
	## Populate the data arrays
	''' 
	telephonetriage.csv is formatted with the following columns:
	note_deid, notelower, labeled (1 for all notes), label
	'''
	allNotes = allData['notelower'].tolist()
	allCodes = allData['label'].to_numpy()

	print ("Number of notes is: {} ".format(len(allNotes))) # 1036
	new_notes = trim_notes(allNotes)
	print (new_notes[:5])
	get_vocab(new_notes)
	print ("There are {} many 'words' in the notes.".format(len(vocab)))
	wordorder = sorted(vocab_freq.items(), key=lambda k_v: k_v[1], reverse=True)
	print (wordorder)

main()
