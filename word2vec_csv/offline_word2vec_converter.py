#!/usr/bin/python3
import gensim
from gensim.models import Word2Vec
import sys
import os
from itertools import islice
import numpy as np

class WVConverter:
  """
  A converter that converts words into vectors using the word2vec model, which is
  trained from 100 billion word Google News corpus.

  NOTE: Please download the word2vec model from here first
  https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit

  Usage Example:
  c = WVConverter()
  print(c.get(["apple", "pear", "dog", "cat"]))
  """

  def __init__(self, wv_model_file='./GoogleNews-vectors-negative300.bin.gz'):
    """ Loads the model. Must be called only once for an object. """

    # This takes about *1 min* to load currently.
    # We can optimize this by pre-filtering and store the words we need only.
    self.wv = gensim.models.KeyedVectors.load_word2vec_format(wv_model_file, binary=True)
    #print("word2vec model loaded :)")
    self.wv.init_sims(replace=True)

  def in_vocab(self, word):
    """ Returns true if the word is in model """
    return word in self.wv.vocab

  def get(self, words):
    """ 
    Input:
      words: a list of words (strings). Each string MUST be in the vocab. 
    Returns:
      A list of unit-normalized vectors, each is a list of float values in length 300.
    """
    # https://stackoverflow.com/a/53333072
    return [self.wv.vectors_norm[self.wv.vocab[word].index] for word in words]

def main():
  c = WVConverter()
  #print("Some words in vocab:", list(islice(c.wv.vocab, 13030, 13040))) 

  words = ["apple", "pear", "dog", "cat"]
  print("Test words:", words)
  print("in_vocab:", [c.in_vocab(w) for w in words])

  vecs = c.get(words)
  print("vector lengths:", [len(v) for v in vecs])
  print("L2 norms:", [np.linalg.norm(v) for v in vecs])

  print("Distances:".format(words))
  l = len(words)
  d = np.zeros((l, l))
  for i in range(l):
    for j in range(i+1, l):
      # L2 norm
      d[i][j] = np.linalg.norm( vecs[i] - vecs[j] )
  print(d)
  # Result:
  # [[0.         0.84253228 1.24924207 1.25897515]
  #  [0.         0.         1.28235996 1.29396939]
  #  [0.         0.         0.         0.69145399]
  #  [0.         0.         0.         0.        ]]

if __name__ == "__main__":
  main()
  sys.exit(0)

