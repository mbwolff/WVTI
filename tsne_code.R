# Based on code by Lynn Cherny
# https://github.com/arnicas/word2vec-pride-vis/blob/master/tsne_code.R

# Code borrowed and modified to fit my data and run in RStudio:
# http://www.codeproject.com/Tips/788739/Visualization-of-High-Dimensional-Data-using-t-SNE

data_for_r <- read.delim("NCF_short_author_Balzac_tsne.tsv", header=FALSE)

# a little cleaning, just in case
mydata <- unique(data_for_r)
mydata <- na.omit(mydata)
row.names(mydata) <- mydata$V1

library(Rtsne)

# need to get rid of the word column again
rtsne_out <- Rtsne(
  as.matrix(mydata[,2:101]),
  theta=0.3,
  initial_dims = 100,
  perplexity = 50,
  max_iter = 500,
  verbose=TRUE)

plot(rtsne_out$Y, t='n', main="BarnesHut t-SNE")
text(rtsne_out$Y, labels=rownames(mydata), cex=0.5, col=rgb(0,0,0,0.5))