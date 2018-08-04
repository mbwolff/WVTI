# Word Vector Text Inventor
Based on [WVTM](https://github.com/mbwolff/WVTM), a contribution to [2016 NaNoGenMo](https://github.com/NaNoGenMo/2016), and formally dubbed WVTG (Word Vector Topic Generator). This is a hack in progress I will present at the [2018 ELO conference](https://sites.grenadine.uqam.ca/sites/nt2/en/elo2018/schedule/444/Algorithmic+Invention).

The repository contains the code and data necessary to invent responses to an assertion from Baudelaire's _Enivrez-vous_. Each word in the invented text is based on an analogy with the word pair _bien_ / _mal_ and on word vectors derived from 30 volumes written by Gustave Flaubert.

The file

```
inventText.ipynb
```

documents and executes a method of algorithmic rhetorical invention.

The code can also produce comparable results in English with the nearly [3,000,000 tweets by Russian trolls.] (https://github.com/mbwolff/russian-troll-tweets) posted by [FiveThirtyEight](https://fivethirtyeight.com).

### A quick explanation of what's under the hood

Using [gensim](https://radimrehurek.com/gensim/models/word2vec.html) to build a word2vec model based on a corpus of French texts , the code takes a pair of words (e.g. "homme" and "femme") and a text as parameters to generate a new text. Each word in the original text is replaced by a word that is "most similar" to it according to the word pair. For instance, if "roi" is a word in the original text, it would be replaced by analogy:

```
>>> model.most_similar(positive=['femme', 'roi'], negative=['homme'], topn=1)
[(u'reine', 0.8085041046142578)]
```
If the word vector model is unable to complete an analogy, the word from the asserted text does not change in the invented text.

Handling verb conjugations and adjective agreements computationally in French is tricky but the code produces a mostly readable text needing grammatical polishing (a good exercise for students). The code can generate a response to any asserted text with any pair of words.
