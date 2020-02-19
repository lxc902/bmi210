import numpy as np
import os
import csv
import pandas as pd
import re
from collections import defaultdict
from sklearn import svm
from sklearn.exceptions import ConvergenceWarning
import warnings

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
	warnings.filterwarnings('ignore', category=ConvergenceWarning)
	train_size = 800
	
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
	accuracies = []
	for length in range(25,500,25):
		embed_vocab = [i[0] for i in wordorder[:length]]
		note_vecs = tokenize(new_notes, embed_vocab)
		note_mags = np.array([np.linalg.norm(i) for i in note_vecs])
		training_data = note_vecs[:train_size]
		training_labels = allCodes[:train_size]
		test_data = note_vecs[train_size:]
		test_labels = allCodes[train_size:]

		clf = svm.LinearSVC()
		clf.fit(training_data, training_labels)
		test_results = clf.predict(test_data)

		total_test = 0
		total_correct = 0
		for i, result in enumerate(test_results):
			total_test += 1
			# print ("Actual: {}, Predicted: {}".format(test_labels[i], result))
			if test_results[i] == test_labels[i]:
				total_correct += 1
		total_accuracy = float(total_correct/total_test)
		accuracies.append((0, length, total_accuracy))
		# print ("Total Accuracy with top {} words in vocab: {}".format(len(embed_vocab),total_accuracy))

	for start in range(0,375,25):
		for size in range (25, 325, 25):
			embed_vocab = [i[0] for i in wordorder[start:(start+size)]]
			note_vecs = tokenize(new_notes, embed_vocab)
			note_mags = np.array([np.linalg.norm(i) for i in note_vecs])
			training_data = note_vecs[:train_size]
			training_labels = allCodes[:train_size]
			test_data = note_vecs[train_size:]
			test_labels = allCodes[train_size:]

			clf = svm.LinearSVC()
			clf.fit(training_data, training_labels)
			test_results = clf.predict(test_data)

			total_test = 0
			total_correct = 0
			for i, result in enumerate(test_results):
				total_test += 1
				# print ("Actual: {}, Predicted: {}".format(test_labels[i], result))
				if test_results[i] == test_labels[i]:
					total_correct += 1
			total_accuracy = float(total_correct/total_test)
			end = start + size
			accuracies.append((start, end, total_accuracy))
			# print ("Total Accuracy with words from {} to {}: {}".format(start, (start+size),total_accuracy))

	with open('accuracies.csv', 'w') as outfile:
		print ("Writing Accuracies to file...")
		outfile.write('\n'.join('{}, {}, {}'.format(x[0],x[1],x[2]) for x in accuracies))
	print ("Done.")

main()
