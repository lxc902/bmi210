'''
Interpret the pickled models for triaging patient notes
'''
import numpy as np
import os
import csv
import pandas as pd
import pickle
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import ConvergenceWarning
import warnings
import json
import sys
import re

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

# Vocabulary for embeddings
vocab = ['itchy', 'dry', 'allergy', 'ketotifen', 'olapatadine',
 'antibiotic', 'glaucoma', 'steroid', 'surgery', 'pain', 'painful', 'red',
 'flashes', 'float', 'floater', 'flash', 'swelling', 'fax', 'rx', 'contact', 
 'prescription', 'information', 'pharmacy', 'history', 'today', 'nurse', 'self', 
 'seen', 'subject', 'needs', 'vision', 'unresolved', 'scheduled', 'appointment', 
 'appt', 'new', 'informed', 'past', 'eyes', 'wants', 'has', 'do', 'said', 'may', 
 'take', 'questions', 'question', 'about', 'still', 'reasons', 'did', 'ok', 
 'receive', 'order', 'one', 'next', 'back', 'use', 'drop', 'unable', 'come', 
 'complaint', 'doctor', 'urgent', 'not', 'data', 'compliment', 'thank', 'eye']


JSON_OUTPUT_PATH = "output.json"
URGENCY_CLASSES = ["Urgent0", "Urgent1", "NonUrgent2"]

# Unpickle models
gnb_filename = os.getcwd() + "/src/server/classifierPythonScripts/bagOfWords_app/" + "pickled_GNB.pkl"
with open(gnb_filename, 'rb') as file:
	gnb = pickle.load(file)

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


# Get note line

def writeClassificationToJsonFile(classification, keywords):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'src/server/classifierPythonScripts/bagOfWords_app/' + JSON_OUTPUT_PATH)
    outFile = open(filename, "w")
    outputJSON = json.loads("{}")
    outputJSON["classification"] = classification
    outputJSON["keywords"] = keywords
    outFile.write(json.dumps(outputJSON, indent=2, sort_keys=True, ensure_ascii=True))
    outFile.close()

def main():
	transcript = sys.argv[1]
	# print("transcript param = ", transcript)
	trimmed_transcript = trim_notes([transcript])[0]
	transcript_vec = tokenize_note(trimmed_transcript, vocab)
	# print (transcript_vec)
	rating = gnb.predict([transcript_vec])[0]
	print ("Rating is: {}".format(URGENCY_CLASSES[rating]))
	used_words = []
	for i in range(len(transcript_vec)):
		if transcript_vec[i] != 0:
			used_words.append(vocab[i])
	print ("Words used: {}".format(used_words))
	# Write JSON file
	writeClassificationToJsonFile([URGENCY_CLASSES[rating]], used_words)


main()