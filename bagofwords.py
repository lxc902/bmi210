import numpy as np
import os
import csv
import pandas as pd
import re
from collections import defaultdict
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import ConvergenceWarning
import warnings
# import gen_vocab
import pickle


'''
This is a program to take in a labeled file and train a unigram classifier to
	triage based on pre-labeled cases

Currently just operates on telephonetriage.csv, which is in the same dir as 
	this program
'''

# Paths
cur_dir = os.getcwd()
# data_path = cur_dir + '/telephonetriage.csv'
data_path = '/Users/isaacsmith/Documents/Stanford/Winter 2020/CS 270//telephonetriage.csv'


# Data
training_data = []
dev_data = []
test_data = []
vocab_freq = defaultdict()
vocab = set([])

# Test note should give 1
# "patient called clinic and left the following information:     crm # 3400019: pt states that she saw md ta on 04/21. states that he was supposed to submit a prescription to the pharamcy and she has still not received it. states she even called walgreens and they don't have it yet. pt is not sure of the name of the prescription but says it was capsules. please send prescription to the pharmacy attached and call the pt once its done.  nurse called and spoke to patient   explained to patient that per dr. ta note, patient need to get clearance fron pcp before we can send rx for doxycycline to pharmacy (prescription for oral doxycycline 50 mg oral twice a day - need clearance from primary care physician).  nurse provided patient with clinic fax # for pcp to fax in clearance paperwork.   patient verbalized understanding of instructions and will contact her pcp."

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

wordREs = [

]

otherREs = [
'crm', 
'\d\d\d\d\d\d\d',
'[\d+]',
'-----',
'message',
'from',
'�',
'(\w+)@(\w+).(\w+)'
]

REs = [phoneREs, dateREs, timeREs, otherREs, wordREs]


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

def tokenize_word(word, vocab):
	# word is a string, vocab is a list of words
	token = np.zeros(len(vocab))
	if word in vocab:
		index = vocab.index(word)
		token[index] = 1
	return token

def tokenize_note(note, vocab):
	note_vector = np.zeros(len(vocab))
	for word in note.split():
		token = tokenize_word(word, vocab)
		note_vector += token
	return note_vector

def tokenize(notes, vocab):
	tokenized = []
	for note in notes:
		note_arr = tokenize_note(note, vocab)
		tokenized.append(note_arr)
	return np.array(tokenized)

def main():
	warnings.filterwarnings('ignore', category=ConvergenceWarning)
	train_size = 600
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

	get_vocab(new_notes)
	print ("There are {} many 'words' in the notes.".format(len(vocab)))

	wordorder = sorted(vocab_freq.items(), key=lambda k_v: k_v[1], reverse=True)

	results = []

	start = 25
	size = 300
	embed_vocab = [i[0] for i in wordorder[start:(start+size)]]
	test_hand_vocab = ['itchy', 'dry', 'allergy', 'ketotifen', 'olapatadine', 'antibiotic', 'glaucoma', 'steroid', 'surgery', 'pain', 'painful', 'red', 'flashes', 'float', 'floater', 'flash', 'swelling', 'fax', 'rx', 'contact', 'prescription', 'information', 'pharmacy', 'history', 'today', 'nurse', 'self', 'seen', 'subject', 'needs', 'vision', 'unresolved', 'scheduled', 'appointment', 'appt', 'new', 'informed', 'past', 'eyes', 'wants', 'has', 'do', 'said', 'may', 'take', 'questions', 'question', 'about', 'still', 'reasons', 'did', 'ok', 'receive', 'order', 'one', 'next', 'back', 'use', 'drop', 'unable', 'come', 'complaint', 'doctor', 'urgent', 'not', 'data', 'compliment', 'thank', 'eye']

	note_vecs = tokenize(new_notes, test_hand_vocab)
	note_mags = np.array([np.linalg.norm(i) for i in note_vecs])
	training_data = note_vecs[:train_size]
	training_labels = allCodes[:train_size]
	test_data = note_vecs[train_size:]
	test_labels = allCodes[train_size:]


	clf = svm.LinearSVC()
	clf.fit(training_data, training_labels)
	test_results = clf.predict(test_data)

	for i, result in enumerate(test_results):
		results.append((test_labels[i], test_results[i]))

	gnb = GaussianNB()
	gnb_test_results = gnb.fit(training_data, training_labels).predict(test_data)

	gnb_results = []
	for i, result in enumerate(gnb_test_results):
		gnb_results.append((test_labels[i], gnb_test_results[i]))

	# Save to file in the current working directory
	svm_filename = "pickled_SVM.pkl"
	with open(svm_filename, 'wb') as file:
		pickle.dump(clf, file)

	gnb_filename = "pickled_GNB.pkl"
	with open(gnb_filename, 'wb') as file:
		pickle.dump(gnb, file)

main()
