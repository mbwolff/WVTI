#!/usr/bin/env python
from __future__ import division
import os, pickle, re, csv

bibliography = '../NCFbibliography.csv'
corpus = 'NCF'
target_att = 'short_author'
target_value = 'Balzac'
sourcedir = '../NCF_pickled'

targetdir = '../' + corpus + '_' + target_att + '_' + target_value + '_selected'

if not os.path.exists(targetdir):
    os.makedirs(targetdir)

with open(bibliography, 'rb') as csvfile:
    bibreader = csv.DictReader(csvfile)
    for row in bibreader:
        if row[target_att] == target_value:
            fname = re.sub('tei$', '', row['filename'])
            for file in os.listdir(sourcedir):
                string = re.escape(fname)
                if re.match(string, file):
                    try:
                        os.symlink(os.path.join(sourcedir, file), os.path.join(targetdir, file))
                    except:
                        print file + 'has probably already been symlinked.'
                        continue
