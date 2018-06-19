#!/usr/bin/env python

# Based on code by Lynn Cherny (and others)
# https://github.com/arnicas/word2vec-pride-vis

# This code generate a file that can be imported to R to create a t-SNE viz.

import os, pickle, re, csv, gensim

datadictfile = '../Trump_pos_dict.pkl'
modelfile = '../Trump_model'

filelabel = re.sub('_model$', '', modelfile)

def make_score_files(model, datadict, filelabel):
    with open(filelabel + '_tsne.tsv', 'w') as tsnefile:
        for word in datadict.keys():
            try:
                score = model[word]
                scores = [str(x) for x in score]
                if re.match('\w', word):
                    tsnefile.write('\t'.join([word] + scores) + '\n')
            except:
                print "Not found:", word, datadict[word]
                continue
    print 'Wrote tsnefile'

pickleFile = open(datadictfile, 'rb')
datadict = pickle.load(pickleFile)
model = gensim.models.Word2Vec.load(modelfile)

make_score_files(model, datadict, filelabel)
