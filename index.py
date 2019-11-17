# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 00:46:47 2019

@author: marco
"""
#importing the libraries
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
import json
#importing index_utils.py and also collector_utils.py
import index_utils as iu
import collector_utils as cu

#Filtering the intro and the plot and store them in new TSV files
for i in range(30000):
    try:
        #if the i-th TSV file exists
        filtered_infos = []
        with open('Database/TSV/movie_' + str(i) +'.tsv', encoding = 'utf8') as tsvFile:
            reader = csv.reader(tsvFile, delimiter='\t')
            
            #taking all the infos
            filtered_infos = iu.filtering_infos(reader)
        
        #Creating a 'Filtered' TSV file inside the folder FilteredTSV which is inside the Database folder
        with open('Database/FilteredTSV/movie_' + str(i) +'.tsv', 'w', newline = '', encoding = 'utf_8') as tsvFile:
            tsv_output = csv.writer(tsvFile, delimiter='\t')
            tsv_output.writerow(filtered_infos)
            
    #if the i-th TSV file does not exist, pass to the next one        
    except Exception as error:
        pass
    
#Creating the vocabulary and the inverted index  
dic = {} #vocabulary
dic_inverted = defaultdict(list) #inverted index
for i in range(30000):
    try:
        #if the i-th exists
        with open('Database/FilteredTSV/movie_'+str(i)+'.tsv', encoding = 'utf8') as tsvFile:
            reader = csv.reader(tsvFile, delimiter='\t')
            
            #creating both the vocabulary and the inverted index
            iu.vocabulary_index(reader, dic, dic_inverted, i)
            
    #if the i-th TSV file does not exist, pass to the next one        
    except Exception as error:
        pass

#storing both the vocabulary and the inverted index as json files   
with open("Database/vocabulary.json","w") as mj:
    json.dump(dic, mj)
    
with open("Database/dic_inverted.json","w") as mj:
    json.dump(dic_inverted, mj)

import collector_utils as cu
import json

#collecting the urls of all the movies and store them in a json file
movies = []
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html', movies)
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html', movies)
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies3.html', movies)

#creating a dictionary which has as keys the positions and as items the urls
dic_movies = {i: movies[i] for i in range(len(movies))}

with open('Database/urls.json', 'w') as mj:
    json.dump(dic_movies, mj)  

    