#!/usr/bin/env python
from __future__ import division
import os, spacy, pickle, re, csv

sourcedir = '/dir/for/text/files' # source data is restricted
bibliography = '../NCFbibliography.csv'
corpus = 'NCF'

targetdir = '../' + corpus + '_pickled'
pos_dict = '../' + corpus + '_pos_dict.pkl'
# dict of lists of pos for lemmatized words

if not os.path.exists(targetdir):
    os.makedirs(targetdir)

nlp = spacy.load('fr')

pd = dict()
with open(bibliography, 'rb') as csvfile:
	bibreader = csv.DictReader(csvfile)
	for row in bibreader:
		print(row['title'])
		fname = re.sub('tei$', 'txt', row['filename'])
		nfname = re.sub('tei$', 'pkl', row['filename'])
		text = open(os.path.join(sourcedir, fname)).read().decode('utf8')
		chunks = text.split('.')
		sections = []
		current_section = ''
		last_chunk = chunks.pop()
		for chunk in chunks:
			if len(current_section) + len(chunk) + 1 < 1000000:
			# Spacy requires texts of length no more than 1000000
				current_section = current_section + chunk + '.'
			else:
				sections.append(current_section)
				current_section = chunk + '.'

		current_section = current_section + last_chunk
		sections.append(current_section)

		section_counter = 0
		for section in sections:
			doc = nlp(unicode(section))
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
			fn = nfname
			if len(sections) > 1:
				fn = re.sub('pkl$', str(section_counter) + '.pkl', fn)
				section_counter = section_counter + 1
			print(os.path.join(targetdir, fn))
			pickleFile = open(os.path.join(targetdir, fn), 'wb')
			pickle.dump(sentences, pickleFile)

pickleFile = open(pos_dict, 'wb')
pickle.dump(pd, pickleFile)
