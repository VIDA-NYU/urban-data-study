require("tm");
require("wordcloud");
input <- commandArgs(trailingOnly = TRUE);
min_scale = 1;
max_scale = 10;
max_word = 700;
if (length(input) != 1)
{
  max_word = as.numeric(input[2]);
  min_scale = as.numeric(input[3]);
  max_scale = as.numeric(input[4]);
}
print(min_scale);
print(max_word);
#tags <- Corpus (DirSource(input));
tags <- Corpus(VectorSource(readLines(input[1])));
tags <- tm_map(tags, stripWhitespace);
tags <- tm_map(tags, tolower);
tags <- tm_map(tags, removeWords, stopwords("english"));
skipwords <- as.character(readLines("data/skipwords.txt"));
tags <- tm_map(tags, removeWords, skipwords);
#par(mfrow=c(3,1))
#wordcloud(tags, scale=c(10,0.3), max.words=5000, random.order=FALSE, rot.per=0.35, use.r.layout=TRUE, colors=brewer.pal(8, "Dark2"));
wordcloud(tags, scale=c(max_scale,min_scale), max.words=max_word, random.order=FALSE, rot.per=0.35, use.r.layout=TRUE, colors=brewer.pal(8, "Dark2"));
