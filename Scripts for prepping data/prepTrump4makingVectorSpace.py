#!/usr/bin/env python

import os, pickle, spacy, re, json

sourcedir = '../TrumpData'
# The data were downloaded as json files using the python module Twint.
# You may need to edit the json files to ensure they are properly formatted.

targetdir = '../Trump_pickled'
pos_dict = '../Trump_pos_dict.pkl'

nlp = spacy.load('en')

if not os.path.exists(targetdir):
    os.makedirs(targetdir)

pd = dict()
for fname in os.listdir(sourcedir):
	if fname.endswith('json'):
		print(fname)
		nfname = re.sub('json$', 'pkl', fname)
		with open(os.path.join(sourcedir, fname), 'r') as f:
			tweets = json.load(f, encoding='utf-8')
		text = ''
		for tweet in tweets:
			t = tweet['tweet'] # for Twint
			t = re.sub('http\S*', '', t)
			t = re.sub('pic.twitter\S*', '', t)
			if not re.match('\W$', t): t = t + '.'
			text = text + t
		text = re.sub(ur'([\.\?\!])([^\.\?\!])', r'\1 \2', text)
		doc = nlp(unicode(text))
		parsed = [(w.text, w.tag_, w.lemma_) for w in doc]
		sentences = []
		sent = []
		for token in parsed:
			text = token[0]
			pos = token[1]
			lemma = token[2].lower()
			if re.match('PUNCT', pos) and re.match(r'[\.\!\?]', text):
				sent.append(lemma)
				sentences.append(sent)
				sent = []
			else:
				if not re.match('PUNCT', pos):
					lemma = re.sub('^\W+', '', lemma)
					lemma = re.sub('\W+$', '', lemma)
				if re.match('\w', pos):
					sent.append(lemma)
					if pd.get(lemma): pd[lemma] = pd.get(lemma).add(pos)
					else: pd[lemma] = { pos }

		if len(sent) > 0: sentences.append(sent)
		print(os.path.join(targetdir, nfname))
		pickleFile = open(os.path.join(targetdir, nfname), 'wb')
		pickle.dump(sentences, pickleFile)

pickleFile = open(pos_dict, 'wb')
pickle.dump(pd, pickleFile)
