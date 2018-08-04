#!/usr/bin/env python

# Based on code by Radim Rehurek
# https://rare-technologies.com/word2vec-tutorial/

import os, re, logging, gensim, re, io, pickle
from six import iteritems

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

### globals
#sourcedir = '../Trump_pickled'
sourcedir = '../Russians_pickled'
saved = re.sub('pickled$', 'model', sourcedir)

### functions and classes
def getTagged(path):
	pickleFile = open(path, 'rb')
	sentences = pickle.load(pickleFile)
	return sentences

class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			if fname.endswith('pkl'):
				for sent in getTagged(os.path.join(self.dirname, fname)):
					yield sent

sentences = MySentences(sourcedir) # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences, workers=4)
model.init_sims(replace=True)
model.save(saved)
