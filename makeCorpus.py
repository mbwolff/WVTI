#!/usr/bin/env python

import os, treetaggerwrapper, pickle, re

sourcedir = ''
# This should be the path to a directory containing plain text versions
# (in UTF-8) of the corpus documents for the vector space model of words.

targetdir = 'processed_texts'
# This should be a path for pkl files derived from the docs in sourcedir.
# These files will be used to construct the vector space model of words.

pos_dict = 'pos_dict.pkl'
# dict of lists of pos for lemmatized words

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')

pd = dict()
for fname in os.listdir(sourcedir):
	if fname.endswith('txt'):
		print(fname)
		nfname = re.sub('txt$', 'pkl', fname)
		text = open(os.path.join(sourcedir, fname)).read().decode('utf-8')
		parsed = tagger.tag_text(text)
		sentences = []
		sent = []
		for token in parsed:
			tokenparts = token.split('\t')
			if len(tokenparts) == 3:
				pos = tokenparts[1]
				lemma = tokenparts[2]
				if re.search('SENT', pos):
					sentences.append(sent)
					sent = []
				elif not (re.search('PUN', pos) or re.search('@', lemma)):
					sent.append(lemma.lower())
					if pd.get(lemma.lower()): pd[lemma.lower()] = pd.get(lemma.lower()).add(pos)
					else: pd[lemma.lower()] = { pos }

		if len(sent) > 0: sentences.append(sent)
		print(os.path.join(targetdir, nfname))
		pickleFile = open(os.path.join(targetdir, nfname), 'wb')
		pickle.dump(sentences, pickleFile)

pickleFile = open(pos_dict, 'wb')
pickle.dump(pd, pickleFile)
