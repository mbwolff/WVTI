#!/usr/bin/env python

# Based on code by Lynn Cherny (and others)
# https://github.com/arnicas/word2vec-pride-vis

# This code generate a file that can be imported to R to create a t-SNE viz.

import os, pickle, re, csv, gensim

datadictfile = '../Trump_pos_dict.pkl'
modelfile = '../Trump_model'

filelabel = re.sub('_model$', '', modelfile)

def make_score_files(model, datadict, filelabel):
    all_pos = set()
    tag = {
        'PRP$': 'ADJ',
        'VBG': 'VERB',
        'FW': 'X',
        'NFP': 'PUNCT',
        'VBN': 'VERB',
        'VBP': 'VERB',
        'WDT': 'ADJ',
        'JJ': 'ADJ',
        'WP': 'NOUN',
        'VBZ': 'VERB',
        'DT': 'DET',
        'RP': 'PART',
        'NN': 'NOUN',
        'VBD': 'VERB',
        'TO': 'PART',
        'PRP': 'PRON',
        'RB': 'ADV',
        'NNS': 'NOUN',
        'NNP': 'PROPN',
        'VB': 'VERB',
        'WRB': 'ADV',
        'CC': 'CONJ',
        'LS': 'PUNCT',
        'PDT': 'ADJ',
        'RBS': 'ADV',
        'RBR': 'ADV',
        'CD': 'NUM',
        'XX': 'X',
        'IN': 'ADP',
        'WP$': 'ADJ',
        'ADD': 'X',
        'MD': 'VERB',
        'NNPS': 'PROPN',
        'JJS': 'ADJ',
        'JJR': 'ADJ',
        'SYM': 'SYM',
        'UH': 'INTJ'
    }
    
    with open(filelabel + '_tsne.tsv', 'w') as tsnefile:
        for word in datadict.keys():
            try:
                score = model[word]
                scores = [str(x) for x in score]
                if re.match('\w', word):
                    pos = next(iter(datadict[word])).split('__')[0]
                    if pos in tag.keys():
                        pos = tag[pos]
                    if pos not in set(['PART']):
                        all_pos.add(pos)
                        tsnefile.write('\t'.join([word, pos] + scores) + '\n')
            except:
                print "Not found:", word, datadict[word]
                continue
    print 'Wrote tsnefile'
    print all_pos

pickleFile = open(datadictfile, 'rb')
datadict = pickle.load(pickleFile)
model = gensim.models.Word2Vec.load(modelfile)

make_score_files(model, datadict, filelabel)
