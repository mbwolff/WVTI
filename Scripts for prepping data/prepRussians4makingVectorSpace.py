#!/usr/bin/env python

import os, pickle, spacy, re, csv

sourcedir = '../../russian-troll-tweets-master'
# The data were downloaded from
# https://github.com/fivethirtyeight/russian-troll-tweets.

targetdir = '../Russians_pickled'
pos_dict = '../Russians_pos_dict.pkl'

nlp = spacy.load('en')

if not os.path.exists(targetdir):
    os.makedirs(targetdir)

pd = dict()
for fname in os.listdir(sourcedir):
    if fname.endswith('csv'):
        print(fname)
        nfname = re.sub('csv$', 'pkl', fname)
        tweets = list()
        with open(os.path.join(sourcedir, fname), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: tweets.append(row)
        text = ''
        for tweet in tweets:
            t = tweet['content']
            t = re.sub('http\S*', '', t)
            t = re.sub('pic.twitter\S*', '', t)
            if not re.match('\W$', t): t = t + '.'
            text = text + t
        text = re.sub(ur'([\.\?\!])([^\.\?\!])', r'\1 \2', text)

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
            doc = nlp(unicode(section.decode('utf8')))
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
