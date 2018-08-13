# Based on code by Lynn Cherny
# https://github.com/arnicas/word2vec-pride-vis/blob/master/tsne_code.R

# Code borrowed and modified to fit my data and run in RStudio:
# http://www.codeproject.com/Tips/788739/Visualization-of-High-Dimensional-Data-using-t-SNE
# Second column contains POS descriptor

data_for_r <- read.delim("NCF_Flaubert_tsne.tsv", header=FALSE, quote="", fill=FALSE)
#data_for_r <- read.delim("RussianTrolls_tsne.tsv", header=FALSE, quote="", fill=FALSE)

color=c("#114477", "#4477AA", "#77AADD", "#117755", "#44AA88", "#99CCBB",
        "#777711", "#AAAA44", "#DDDD77", "#771111", "#AA4444", "#DD7777",
        "#771144", "#AA4477", "#DD77AA")

fr_pos=c("ADV", "NOUN", "ADP", "NUM", "SCONJ", "PROPN", "DET", "INTJ", "PUNCT",
      "VERB", "AUX", "CCONJ", "X", "PRON", "ADJ")
en_pos=c("ADV", "NOUN", "ADP", "PUNCT", "PROPN", "DET", "SYM", "INTJ", "PRON",
         "NUM", "X", "CONJ", "ADJ", "VERB")

# a little cleaning, just in case
mydata <- unique(data_for_r)
mydata <- na.omit(mydata)
#mydata = subset(mydata, !grepl("^[0-9]", V1))
row.names(mydata) <- mydata$V1

library(Rtsne)

rtsne_out <- Rtsne(
  as.matrix(mydata[,3:102]),
  theta=0.3,
  initial_dims = 100,
  perplexity = 50,
  max_iter = 500,
  verbose=TRUE)

plot(rtsne_out$Y, t="n", main="BarnesHut t-SNE")
text(rtsne_out$Y, labels=rownames(mydata), cex=0.5, col=color[match(mydata$V2, fr_pos)])
#text(rtsne_out$Y, labels=rownames(mydata), cex=0.5, col=color[match(mydata$V2, en_pos)])