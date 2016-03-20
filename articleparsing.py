#### START ###

# Code to parse newspapers using the newspaper package (http://newspaper.readthedocs.org/en/latest/). 
# Acquire 'title', 'link', and 'keywords' from 'Bloomberg', 'CNN', and 'The Economist'.
# Write them in a seperate Excel workbook (with sheets for each newspaper source).

#Load packages

import newspaper
from newspaper import Article, ArticleException, news_pool
import tldextract
import pkg_resources
import parser
import nltk
import re
import xlwt
from datetime import datetime

# Creating Excel Workbook for Data
wb = xlwt.Workbook(encoding="utf-8")
sheet1 = wb.add_sheet("Bloomberg", cell_overwrite_ok=True)
sheet2 = wb.add_sheet("CNN", cell_overwrite_ok=True)
sheet3 = wb.add_sheet("Economist", cell_overwrite_ok=True)

# Change width of first column in all sheets
sheet1.col(0).width = 5000 
sheet2.col(0).width = 5000
sheet3.col(0).width = 5000

# Put Headings on each Excel Sheet
headings = ('Title', 'URL', 'Keywords')
for idx, s in enumerate(headings):
	sheet1.write(0,idx,s)
	sheet2.write(0,idx,s)
	sheet3.write(0,idx,s)

# Replace unwanted characters in 'keywords' for better Excel input
replacements= {"u'":"",
			  "'":"",
			  "[":"",
			  "]":""}	

# Creating News Sources
bloomberg_paper = newspaper.build('http://www.bloomberg.com/', memoize_articles=False) # remove memoize if no cache
cnn_paper = newspaper.build('http://www.cnn.com/', memoize_articles=False)
economist_paper = newspaper.build('http://www.economist.com/', memoize_articles=False)

# Check # of articles
bloomberg_size = bloomberg_paper.size() 
cnn_size = cnn_paper.size()
economist_size = economist_paper.size()
size = [bloomberg_size, cnn_size, economist_size]
print size

# Multi-threading to download papers faster (can run w/out this as it takes a lot of time)

tstart = datetime.now()
papers = [bloomberg_paper, cnn_paper, economist_paper]
news_pool.set(papers, threads_per_source=5) 
news_pool.join()
tend = datetime.now()
print "Time taken to Multi-thread:" ,tend - tstart

# Create Loop for each news source to acquire title, url, keywords within a range
# and then save the output to an Excel sheet

tstart = datetime.now()
# BLOOMBERG
for x in range(1, 50): 				      	  # current range = 50
	article = bloomberg_paper.articles[x] 
	article.download() 			       	  # downloading article
	article.parse()					  # parsing article ~ must download first
	article.nlp() 					  # accessing natural language properties ~ must download & parse first
	t1 = (article.title) 				  # title
	l1 = (article.url) 				  # url
	k1 = str(article.keywords) 			  # keywords
	for k, v in replacements.iteritems()	 	  # replacing "[, ], u'" characters
		k1 = k1.replace(k,v) 			  # with whitespace
	bloomberg = [t1, l1, k1] 			  # creating dict with title, url, keywords
	for idx, s in enumerate(bloomberg):    		  # input data into excel sheet
		sheet1.write(x, idx, s)			  # x=row (got from range), idx=t1,l1,k1, s=string

# CNN
for x in range(1, 50):
	article2 = cnn_paper.articles[x] 
	article2.download() 
	article2.parse() 
	article2.nlp() 
	t2 = (article2.title) 
	l2 = (article2.url)
	k2 = str(article2.keywords)
	for k, v in replacements.iteritems():
		k2 = k2.replace(k,v)	
	cnn = [t2, l2, k2]
	for idx, s in enumerate(cnn):
		sheet2.write(x, idx, s)	

# ECONOMIST
for x in range(1, 50):
	article3 = economist_paper.articles[x]
	article3.download()
	article3.parse()
	article3.nlp()	
	t3 = (article3.title)
	l3 = (article3.url)
	k3 = str(article3.keywords)
	for k, v in replacements.iteritems():
		k3 = k3.replace(k,v)	
	economist = [t3, l3, k3]
	for idx, s in enumerate(economist):
		sheet3.write(x, idx, s)

tend = datetime.now()
print "Time taken to parse articles:" ,tend - tstart
wb.save('news.xls') 					  # save XLS file on directory 

# Additionally, if you want to print/save only articles with keyword 'risk'
# insert following code in the loop of the article:
	#if any("risk" in s for s in k):
		# print "The title of the article is:" ,m
		# print "The link for it is:" ,u
		# print "The keywords are:" ,n
		
### END ###
