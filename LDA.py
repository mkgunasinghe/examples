### START ###

"""
Parse newspapers using the newspaper package (http://newspaper.readthedocs.org/en/latest/). 
Save articles in .txt files, apply preprocessing (tokenizing, remove stop words, etc.) and get topic keywords.
Create document term matrix for text articles and compare through cosine distance.
Visualize distance (click on points to see what article it refers to).
"""

# Load packages
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from time import time
from matplotlib.pyplot import figure, show
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS
from newspaper import Article, ArticleException, news_pool
import tldextract
import pkg_resources
import parser
import re
import gensim
import os
import glob
import scipy
import numpy as np
import pandas as pd 
import newspaper
import matplotlib.pyplot as plt

os.chdir('/Users/milo/Documents/Python') # change 'milo'

# Creating News Sources
bloomberg_paper = newspaper.build('http://www.bloomberg.com/', memoize_articles=False) # remove memoize if no cache
economist_paper = newspaper.build('http://www.economist.com/', memoize_articles=False)
print ("There are", bloomberg_paper.size() ,"Bloomberg articles and", economist_paper.size() , "Economist articles.")

# Multithreading ~ This takes time (can run without it but make sure 'papers' is assigned)
t0 = time()
papers = [bloomberg_paper, economist_paper]
news_pool.set(papers, threads_per_source=2) 
news_pool.join()
print ("%0.2f Seconds to Multi-thread." % (time() - t0))

# Download articles in txt format w/ heading as title
t0 = time()
for npapers in papers:	
	path = ("/Users/milo/Documents/Python/text/" + npapers.brand + "/")
	if not os.path.exists(path):
		os.makedirs(path)
	os.chdir(path)	
	for x in range(1, 51): 					# download 50 articles      
		article = npapers.articles[x] 
		article.download() 					  
		article.parse()						
		article.nlp() 						 
		tl1 = (article.title) 				  	 
		t1 = (article.text)		
		t1 = str(t1.replace("\n\n", " ")) 	# format to delete \n tags		
		k1 = str(article.keywords)  		# need to article.nlp() for this	
		if len(t1) > 500: 					# heurestic to remove 'update' articles
			with open(tl1 + ".txt", 'w') as txt:
				txt.write(t1)
				txt.write("\n \n Keywords:")
				txt.write(k1)
	print ("Downloaded", x,"articles from", npapers.brand,"in %0.2f seconds." % (time() - t0))
	print ("They can be found here:" ,path)

# Latent Dirichlet Allocation
# Preprocessing
en_stop = get_stop_words('en') 
tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()

# Apply stopwords/stemmers and get tokens to convert into BoW
# Print topic keywords for each article
t1 = time()
for nwsp in papers:
	path = (r"/Users/milo/Documents/Python/text/" + nwsp.brand + "/*.txt")
	for file in glob.glob(path):
		texts = []
		with open(file, 'r') as infile:	
				for line in infile:
					line = line.lower()
					tokens = tokenizer.tokenize(line)
					stopped_tokens = [i for i in tokens if not i in en_stop]
					stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
					texts.append(stemmed_tokens)
					texts = [x for x in texts if x] # remove empty texts
		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]
		ldamodel = (gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=50)) # increase passes for higher accuracy (expense of time)
		lda = str(ldamodel.print_topics(num_topics=3, num_words=3))
		lda = re.sub("[^a-z\s(),+]", "", lda) 	# clean the output
		print (lda) 							# Print out main topic words
	print ("Completed Tokenizing in %0.2fs." % (time() - t1))

# Visualise LDA
# Convert txt articles to vectors
filenames = [] 
for nwsp in papers:
	path = (r"/Users/milo/Documents/Python/text/" + nwsp.brand + "/*.txt")
	for file in glob.glob(path):
		filenames.append(file)

vectorizer = CountVectorizer(input='filename')
dtm = vectorizer.fit_transform(filenames)
vocab = vectorizer.get_feature_names()
dtm = dtm.toarray() 
vocab = np.array(vocab)

# Reverse of cosine to get distance between articles
dist = 1 - cosine_similarity(dtm)

mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)

x, y = pos[:, 0], pos[:, 1]
names = [os.path.basename(fn).replace('.txt', '') for fn in filenames] # clean names
fig = plt.figure()

# A picker to show name of article when clicked on plot
def onpick(event):
    ind = event.ind
    print ('The point refers to this article:', np.take(names, ind))

plt.scatter(x, y, picker=True)
fig.canvas.mpl_connect('pick_event', onpick)
plt.title('LDA on Bloomberg and Economist articles')
show()

### END ###






