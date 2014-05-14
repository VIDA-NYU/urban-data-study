require("tm");
require("wordcloud");
input <- commandArgs(trailingOnly = TRUE)
print(args)
tags <- Corpus (DirSource(input));
tags <- tm_map(tags, stripWhitespace);
tags <- tm_map(tags, tolower);
tags <- tm_map(tags, removeWords, stopwords("english"));
#par(mfrow=c(3,1))
wordcloud(tags, scale=c(10,0.3), max.words=5000, random.order=FALSE, rot.per=0.35, use.r.layout=TRUE, colors=brewer.pal(8, "Dark2"));
#wordcloud(tags, scale=c(10,1), random.order=FALSE, rot.per=0.35, use.r.layout=TRUE, colors=brewer.pal(8, "Dark2"));
