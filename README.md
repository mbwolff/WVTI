# Word Vector Text Modulator 2
Based on [WVTM](https://github.com/mbwolff/WVTM), a contribution to [2016 NaNoGenMo](https://github.com/NaNoGenMo/2016)

This repository contains the code and data necessary to generate _Enivrez-vous_modulé_, Baudelaire's prose poem modified with word vectors derived from 117 texts written by Honoré de Balzac.

Run the following command to produce a modulated text:

```
./transformText.py bénir maudire Balzac Baudelaire_Enivrez-vous.md
```

You can perform a comparable modulation with a word vector model based on 69 texts written by George Sand:

```
./transformText.py bénir maudire Sand Baudelaire_Enivrez-vous.md
```

(In this repository the only options for word vector models are "Balzac" and "Sand": anything else will produce an error.)

### A quick explanation of what's under the hood

Using [gensim](https://radimrehurek.com/gensim/models/word2vec.html) to build a word2vec model based on a corpus of French texts , the code takes a pair of words (e.g. "homme" and "femme") and a text as parameters to generate a modulated text. Each word in the original text is replaced by a word that is "most similar" to it according to the word pair. For instance, if "roi" is a word in the original text, it would be replaced by analogy:

```
>>> model.most_similar(positive=['femme', 'roi'], negative=['homme'], topn=1)
[(u'reine', 0.8085041046142578)]
```
Handling verb conjugations and adjective agreements computationally in French is tricky but the code produces a mostly readable text needing grammatical polishing (a good exercise for students): the _corrigé_ files are examples. The code can modulate any text against any pair of words.
