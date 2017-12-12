#!/usr/bin/env python

import os, treetaggerwrapper, pickle, re, csv

sourcedir = '/Users/mark/Research/2016 DH/FRANTEXT/all-plain-texts'
bibliography = '/Users/mark/Research/2016 DH/FRANTEXT/ARTFLbibDH2014fixed.csv'
# targetdir = r'/Users/mark/Research/LearningPython/FRANTEXT/taggedtexts'
targetdir = '/Users/mark/Research/2018 ELO/processed_sand'
target_author = 'Sand'
pos_dict = '/Users/mark/Research/2018 ELO/Sand_pos_dict.pkl' # dict of lists of pos for lemmatized words

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')

pd = dict()
# for fname in os.listdir(sourcedir):
with open(bibliography, 'rb') as csvfile:
	bibreader = csv.DictReader(csvfile)
	for row in bibreader:
#		if fname.endswith('txt'):
		if row['short_author'] == target_author:
			print(row['title'])
			fname = re.sub('tei$', 'txt', row['filename'])
			nfname = re.sub('tei$', 'pkl', row['filename'])
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
