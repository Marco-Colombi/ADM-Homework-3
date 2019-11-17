# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 22:50:44 2019

@author: marco
"""
from bs4 import BeautifulSoup as soup
import requests
import time
import urllib.request
import urllib.error as uer
import csv
import re
import parser_utils as pu

for i in range(30000):
    infos = []
    #open the i-th html_page 
    file = 'Database/Movies/article_' + str(i) + '.html' 
    #if the i-th html page exists
    try:
        response = open(file, encoding='utf8')
        movie = soup(response, 'html.parser')
        
        #looking for the "disambiguos" wikipedia pages and not creating a TSV file for them
        disambiguos = pu.find_disambiguos(movie)
        if disambiguos is not None:
            continue
        
        #collecting the informations we are looking for        
        infos = pu.scraping_wikipedia(movie)
        
        #creating the i-th TSV file and store it inside a folder called 'TSV', which is inside our folder 'Database'
        with open('Database/TSV/movie_'+ str(i) + '.tsv', 'w', newline = '', encoding = 'utf-8') as tsvFile:
            tsv_output = csv.writer(tsvFile, delimiter = '\t')
            tsv_output.writerow(infos)
            
    #if the i-th html_page doesn't exist, we will continue with the next one    
    except Exception as error:
        pass