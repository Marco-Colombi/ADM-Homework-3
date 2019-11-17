# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 00:41:40 2019

@author: marco
"""
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict

def filtering_infos(reader):
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    filtered_infos = []
    for section in reader:
        for k in range(len(section)):
            line = ''
            #filtering only the intro(1) and the plot(2)
            if k == 1 or k == 2:
                #removing punctuations
                row = tokenizer.tokenize(section[k])
                for j in range(len(row)):
                    #removing stemming
                    w = ps.stem(row[j])
                    #removing stopwords
                    if w not in stop_words and line == '':
                        line += w
                    elif w not in stop_words:
                        line += ' ' + w
            #taking the other sections as they are
            else:
                line = section[k]
            #taking the information
            filtered_infos.append(line)
    return filtered_infos

def vocabulary_index(reader, dic, dic_inverted, i):
    for section in reader:
        #taking the intro and the plot
        row1 = section[1].split()
        row2 = section[2].split()
    list_words = set(row1 + row2)
            
    for word in list_words:
    #if the word is not in the vocabulary we add it
        if word not in dic:
            #appending the document to the inverted_index
            dic_inverted[len(dic)].append(i)
            dic[word] = len(dic)
            
    #if the word is already in the vocabulary we just append the document
    #to the inverted_index          
        else:
            dic_inverted[dic[word]].append(i)
                       