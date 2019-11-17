# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:28:47 2019

@author: marco
"""
#importing libraries
import json
import csv
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
from IPython.display import display
import ipywidgets as widgets
import heapq
import math


#opening the vocabulary, the reversed_index and the movies urls
with open('Database/vocabulary.json') as json_data:
    dic = json.load(json_data)
with open('Database/dic_inverted.json') as json_data:
    dic_inverted = json.load(json_data)
with open('Database/urls.json') as json_data:
    movies = json.load(json_data)

#filtering the queries    
def filtering(info):
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    filtered_info = ''
    #removing punctuations
    row = tokenizer.tokenize(info)
    for j in range(len(row)):
        #removing stemming
        w = ps.stem(row[j])
        #removing stopwords
        if w not in stop_words and filtered_info == '':
            filtered_info += w
        elif w not in stop_words:
            filtered_info += ' ' + w
    return filtered_info

#computing the idf
def idf(term):
    n = 29515  #total filtered documents
    dft = len(dic_inverted.get(str(dic[term])))
    res = math.log(n/dft)
    return(res)
    
#computing the tf
def tf(term,doc):
    file = 'Database/FilteredTSV/movie_'+ str(doc) +'.tsv' 
    data = list(pd.read_csv(file, sep="\t"))
    l = (data[1]+data[2]).split(' ')
    n_term = l.count(term)
    n_doc = len(l)
    return(n_term/n_doc)
    
#computing the tf-idf
def tfidf(term,doc):
    return(round(idf(term)*tf(term,doc),2))

#computing the cosine similarity   
def similarity(query,doc):
    q_list=query.split(' ')
    q_index=[]
    for word in q_list:
        q_index.append(word)
    dot=0
    norm_query=0
    norm_doc=0
    for i in range(len(q_index)):
        dot += (idf(q_index[i])*tfidf(q_index[i],doc))
        norm_query+=tfidf(q_index[i],doc)**2
        norm_doc+=idf(q_index[i])**2
    if norm_query*norm_doc!=0:
        res=round(dot/(math.sqrt(norm_query)*math.sqrt(norm_doc)),2)
    else:
        res=0
    return(res)

#computing the coefficient for search engine 3
def func_coefficient(year, array):
    #taking the release years of all the documents that match the query
    years_data = []
    for x in array:
        file = 'Database/TSV/movie_'+ str(x) +'.tsv'
        data = pd.read_csv(file, sep = "\t")
        release = list(data)[9]
        #if the release date is not None, we take the release year
        if release != 'NA':
            year_release = re.search(r'\d{4}', release)
            if year_release is not None:
                years_data.append(int(year_release.group(0)))
    #taking the maximum difference between the: 
    differences = []
    #year entered by the user - max release year of all the documents that match the query
    differences.append(abs(year - max(years_data)))
    #year entered by the user - min release year of all the documents that match the query
    differences.append(abs(year - min(years_data)))
    max_diff = max(differences)
    if max_diff != 0:
        #computing the coefficient
        coefficient = 1/max_diff
        return coefficient
    else:
        #this means that all the movies are released in the same year of the query
        return 1
    
#computing the score for search engine 3
def new_score(year, data, coefficient):
    release = list(data)[9]
    #if the release date is not None, we take the release year
    if release is not None:
        year_release = re.search(r'\d{4}', release)
        if year_release is not None:
            #computing the score (closeness) of the two years
            score = round(1 - coefficient * abs(year - int(year_release.group(0))), 2)
            return(score)
        else:
            return(0)
    else:
        return(0)

#this function forces the user to input an year in the format 'dddd' for the search engine 3      
def input_year(input):
    print('Enter the year when the film was released: ', end = '')
    year = input() 
    if re.match(r'\d{4}', year) is not None:
        return int(year)
    else:
        print('Please, enter an year', '\n')
        return input_year(input)

#First search engine
def searchengine1(input):
    print('Enter your query: ', end = '')
    query_user=input()
    #filtering the query
    filtered_query = filtering(query_user)
    query_list = filtered_query.split(' ')
    #looking if all the filtered words are in the vocabulary(dic)
    nb = 0
    for word in query_list:
        if word in dic:
            nb += 1
    #if not there is 'no match'
    if nb != len(query_list):
        res = 'No match'
        
    #looking if all the words are in the same documents
    else:
        inter = []
        for word in query_list:
            docs = dic_inverted.get(str(dic[word]))
            inter.append(docs)
        if len(inter)==1:
            final_inter=inter[0]
        else:
            final_inter=list(set(inter[0]).intersection(set(inter[1])))
            for j in range(len(inter)-1):
                final_inter=list(set(final_inter).intersection(set(inter[j+1])))
        #if not there is 'no match'
        if len(final_inter) == 0:
            res = 'No match'
       
        #creating the dataframe of all the matches
        else:
            output_title = []
            output_intro = []
            output_url = []
            for x in final_inter:
                file = 'Database/TSV/movie_'+ str(x) +'.tsv' 
                data = pd.read_csv(file, sep = "\t")
                output_title.append(list(data)[0])
                output_intro.append(list(data)[1])
                output_url.append(movies[str(x)])
            d = pd.DataFrame({'Title': output_title, 'Intro': output_intro,'Wikipedia URL':output_url})
            res = d
    return(res)

#Second search engine    
def searchengine2(input):
    print('Enter your query: ', end = '')
    query_user=input()
    #filtering the query
    filtered_query = filtering(query_user)
    query_list = filtered_query.split(' ')
    #looking if all the filtered words are in the vocabulary(dic)
    nb = 0
    for word in query_list:
        if word in dic:
            nb += 1
    #if not there is 'no match'
    if nb != len(query_list):
        res = 'No match'  
        
    #looking if all the words are in the same documents
    else:
        inter=[]
        for word in query_list:
            docs = dic_inverted.get(str(dic[word]))
            inter.append(docs)
        if len(inter)==1:
            final_inter=inter[0]
        else:
            final_inter=list(set(inter[0]).intersection(set(inter[1])))
            for j in range(len(inter)-1):
                final_inter=list(set(final_inter).intersection(set(inter[j+1])))
        #if not there is 'no match'
        if len(final_inter) == 0:
            res='No match'
        
        else:
            heap_data = []
            for x in final_inter:
                arr = []
                file = 'Database/TSV/movie_'+ str(x) +'.tsv' 
                data = pd.read_csv(file, sep="\t")
                #computing the cosine similarity 
                cos_similarity = similarity(filtered_query, int(x))
                if cos_similarity != 0:
                    arr.append(cos_similarity)
                    arr.append(list(data)[0])
                    arr.append(list(data)[1])
                    arr.append(movies[str(x)])  
                    heap_data.append(arr)
            #mantaining the top k (10) documents using an heap ds method
            top_10 = heapq.nlargest(10, heap_data)
            output_title=[]
            output_intro=[]
            output_url=[]
            output_similarity=[]
            #creating the dataframe of the top k (10) documents
            for data in top_10:
                output_title.append(data[1])
                output_intro.append(data[2])
                output_url.append(data[3])
                output_similarity.append(data[0])   
            d = pd.DataFrame({'Title': output_title, 'Intro': output_intro,'Wikipedia URL':output_url,'Similarity':output_similarity})
            res = d
    return(res)

#with the third search engine we rank the movies by 
#the closeness of their release year to an year entered by the user
#to know the "closeness" we decided to use a coefficient (look at the func_coefficient)
def searchengine3(input):
    print('Enter your query: ', end = '')
    query_user = input()
    #filtering the query 
    filtered_query = filtering(query_user)
    query_list = filtered_query.split(' ')
    #looking if all the filtered words are in the vocabulary(dic)
    nb = 0
    for word in query_list:
        if word in dic:
            nb += 1
    #if not there is 'no match'
    if nb != len(query_list):
        res = 'No match'
    #looking if all the words are in the same documents
    else:
        inter=[]
        for word in query_list:
            docs = dic_inverted.get(str(dic[word]))
            inter.append(docs)
        if len(inter)==1:
            final_inter=inter[0]
        else:
            final_inter=list(set(inter[0]).intersection(set(inter[1])))
            for j in range(len(inter)-1):
                final_inter=list(set(final_inter).intersection(set(inter[j+1])))
                
        #if not there is 'no match'
        if len(final_inter) == 0:
            res='No match'
       
        else:
            heap_data = []
            year_user = input_year(input)
            #computing the coefficient
            coefficient = func_coefficient(year_user, final_inter)
            for x in final_inter:
                arr = []
                file = 'Database/TSV/movie_'+ str(x) +'.tsv' 
                data = pd.read_csv(file, sep="\t")
                #computing the similarity
                arr.append(new_score(year_user, data, coefficient))
                arr.append(list(data)[0])
                arr.append(list(data)[1])
                arr.append(movies[str(x)])  
                heap_data.append(arr)
            #mantaining the top k (10) documents using an heap ds method
            top_10 = heapq.nlargest(10, heap_data)
            output_title=[]
            output_intro=[]
            output_url=[]
            output_similarity=[]
            #creating the dataframe of the top k (10) documents
            for data in top_10:
                output_title.append(data[1])
                output_intro.append(data[2])
                output_url.append(data[3])
                output_similarity.append(data[0])
            d = pd.DataFrame({'Title': output_title, 'Intro': output_intro,'Wikipedia URL':output_url,'Similarity':output_similarity})
            res = d
    return(res)

#Choosing which search engine you want to use
def searchengine_choice(input):
    print("Choose the Search Engine. Enter: \n -'1' to use the First Search Engine \n -'2' to use the Second Search Engine, \n -'3' to use the Third Search Engine. \n Enter 'esc' to exit.", end = "")
    search_engine = input()
    if search_engine == '1':
        return searchengine1(input)
    elif search_engine == '2':
        return searchengine2(input)
    elif search_engine == '3':
        return searchengine3(input)
    elif search_engine == 'esc':
        return
    else:
        print("Please, enter '1', '2', '3' or 'esc'.", '\n')
        return searchengine_choice(input)

output = searchengine_choice(input)
if type(output) != str:
    widget = widgets.Output()
    with widget:
        display(output)
        hbox = widgets.HBox([widget])
    hbox
else:
    print(output)