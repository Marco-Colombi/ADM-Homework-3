# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 02:45:24 2019

@author: marco
"""
#importing the libraries
from bs4 import BeautifulSoup as soup
import requests
import time
import urllib.request
import urllib.error as uer
#importing the collector_utils.py
import collector_utils as cu

movies = []
#collecting the links from the three different data folders
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html', movies)
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html', movies)
cu.urls_collection('https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies3.html', movies)

#downloading the html pages
cu.html_downloading(movies)