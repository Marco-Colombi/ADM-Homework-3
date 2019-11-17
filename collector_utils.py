# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 02:34:26 2019

@author: marco
"""
#importing libraries
from bs4 import BeautifulSoup as soup
import requests
import time
import urllib.request
import urllib.error as uer

#This functions can be used to download all the 30000 pages in the links without
#considering the fact that we split the downloading part where 
#each one of us downloaded 10000 html pages

#getting the urls from the data folders
def urls_collection(github_url, l):
    response = requests.get(github_url)
    movie = soup(response.text, 'html.parser')
    #Taking all the links
    for movie in movie.find_all('a'):
        for k in (movie.attrs):
            l.append(movie.attrs[k])

#downloading the html pages
def html_downloading(l):
    n = []
    for i in range(30000):
        try:
            file = 'Database/Movies/article_ '+ str(i) + '.html'   
            urllib.request.urlretrieve(l[i], file)
        #if the link does not exist, we pass to the next link 
        except uer.HTTPError:
            pass
        except Exception as error:
            #if an exception occured, we append the number of the link to this list
            n.append(i)
            time.sleep(1200) #60s * 20m = 1200s
        time.sleep(2)
    
    #it will run only if some of the previous html was not downloaded because an exception occured 
    if n != []:
        for i in n:
            try:
                file = 'Database/Movies/article_ '+ str(i) + '.html'
                urllib.request.urlretrieve(l[i], file)
            #if the link does not exist, we pass to the next link  
            except uer.HTTPError:
                pass
            except Exception as error:
                time.sleep(1200) #60s * 20m = 1200s
            time.sleep(2)
            
