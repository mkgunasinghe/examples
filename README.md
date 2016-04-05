### Introduction  
This is where I maintain working examples of R and Python codes w/ brief descriptions.

**Current Examples:**  
1. LDA  (Latent Dirichlet Allocation)  
2. Phoenix  
3. Article parsing and processing on Python  
4. Map exploration using GADM on R  

LDA: (Latent Dirichlet Allocation)  
>i. Parse newspapers using the newspaper package (http://newspaper.readthedocs.org/en/latest/).   
ii. Save articles in .txt files, apply preprocessing (tokenizing, remove stop words, etc.) and get topic keywords.  
iii. Create document term matrix for text articles and compare through cosine distance.  
iv. Visualize distance (click on points to see what article it refers to).  

Access and visualise Phoenix data on R:  
>i. Access Phoenix dataset (http://phoenixdata.org/description): near real-time  
	risk-event data, scraping +400 news source and coding ~3,000 events per day.  
ii. Fetch yesterday's data or construct a range to view on a customizable    
	interactive map with specifications such as: country/ies, event type, etc.  
	
![alt tag](https://cloud.githubusercontent.com/assets/17466433/13907496/53f545fe-eee7-11e5-9057-be77197f04a1.jpeg)    
Phoenix recorded observations (clustered) for Turkey in the 2 day range 10/03/16 - 11/03/16.  

Article parsing and processing on Python:       
>i. Use newspaper, nltk, xlwt packages to;    
ii. Download and parse articles from Bloomberg, CNN, and the Economist.    
iii. Extract 'title', 'link', and 'keywords' associated with articles.  
iv. Write data on an Excel workbook.  

Map exploration using GADM on R:       
>i. Extract country and province level spatial data on R with the example of Ecuador.   
ii. Function to reduce the virtual memory associated with polygons by GADM is employed.  
iii. Color specific regions/cities and stack variable names on map.  

