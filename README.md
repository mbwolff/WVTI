# Word Vector Text Modulator 2
Based on [WVTM](https://github.com/mbwolff/WVTM), a contribution to [2016 NaNoGenMo](https://github.com/NaNoGenMo/2016)

This repository contains the code and data necessary to generate _Balzac_modulé_par_Sand_, an excerpt from Balzac's _Le Père Goriot_  modified with word vectors derived from sixty-nine texts written by George Sand.

Run the following command to produce the modulated text:

```
./transformText.py > Balzac_modulé_par_Sand.txt
```

### A quick explanation of what's under the hood

Using [gensim](https://radimrehurek.com/gensim/models/word2vec.html) to build a word2vec model based on a corpus of French texts , the code takes a pair of words (e.g. "homme" and "femme") and a text as parameters to generate a modulated text. Each word in the original text is replaced by a word that is "most similar" to it according to the word pair. For instance, if "roi" is a word in the original text, it would be replaced by analogy:

```
>>> model.most_similar(positive=['femme', 'roi'], negative=['homme'], topn=1)
[(u'reine', 0.8085041046142578)]
```
Handling verb conjugations and adjective agreements computationally in French is tricky but the code produces a mostly readable text needing grammatical polishing (a good exercise for students). The code can modulate any text against any pair of words.
