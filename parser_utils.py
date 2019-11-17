# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 22:00:07 2019

@author: marco
"""
from bs4 import BeautifulSoup as soup
import requests
import time
import urllib.request
import urllib.error as uer
import csv
import re

#looking for the disambigbox in order to know if it is a disambiguos page
def find_disambiguos(movie):
    disambig = movie.find('table', {'id' : 'disambigbox'})
    return disambig

#scraping the valid wikipedia pages
def scraping_wikipedia(movie):
    Box_info = ['Title', 'Directed by', 'Produced by', 'Written by', 'Starring', 'Music by', 'Release date', 'Running time',
           'Country', 'Language', 'Budget']
    clean_path = re.compile('\[\w+\]')
    infos = []
    #Taking the title
    for title in movie('h1'):
        for t in title('i'):
            if t is not None:
                infos.append(t.get_text(' '))
            else:
                infos.append(title.get_text(' '))
        
    #Taking the first section ('Intro')
    intro = ''
    #looking for the main section of the page
    section = movie.find('div', {'class' : 'mw-parser-output'})
    #finding the first p tag of a real text
    par = section.find_next('p', {'class' : None})
    #Making sure that the first p is not: an empty space;
    if par.text == '\n':
        par = par.find_next('p', {'class' : None})
    #is not inside the infobox;
    while par.find_parent('td') is not None:
        par = par.find_next('p', {'class' : None})
    #is not inside a table or a quote box.
    if par.find_parent('div', {'class':'quotebox pullquote floatleft'}) is not None or par.find_parent('blockquote') is not None:
        par = par.find_next('p')
    #creating the intro
    while par.name == 'p':
        intro += par.text
        if par.find_next_sibling() is not None:
            par = par.find_next_sibling()
            #skip the images and the quote boxes
            while par.name == 'div' or par.name == 'style' or par.name == 'blockquote':
                par = par.find_next_sibling()
        else: 
            break
                
    #Cleaning intro           
    if intro != '':
        #removing eventual "e.g.[3]" links
        clean_intro = re.sub(clean_path, '', intro)
        if clean_intro:
            infos.append((' ').join(clean_intro.split('\n')))
        else:
            infos.append((' ').join(intro.split('\n')))
    else:
        infos.append('NA')
        
    #Taking the second section ('Plot') 
    plot = ''
    #finding the next p tag of a real text after the intro
    p = par.find_next('p', {'class' : None})
    if p is not None:
        #skipping tables and the quote boxes
        if p.find_parent('div', {'class':'quotebox pullquote floatleft'}) is not None or p.find_parent('blockquote') is not None:
            p = p.find_next('p', {'class' : None})
        #creating the plot 
        while p.name == 'p':
            plot += p.text
            if p.find_next_sibling() is not None:
                p = p.find_next_sibling()
                #skip the images and the quote boxes
                while p.name == 'div' or p.name == 'style' or p.name == 'blockquote':
                    p = p.find_next_sibling()
            else:
                break
                    
    #Cleaning plot            
    if plot != '':
        #removing eventual "e.g.[3]" links
        clean_plot = re.sub(clean_path, '', plot)
        if clean_plot:
            infos.append((' ').join(clean_plot.split('\n')))
        else:
            infos.append((' ').join(plot.split('\n')))
    else:
        infos.append('NA')
            
    #Taking the infobox
    infobox = {}
    box = movie.find('table',{'class' : "infobox vevent"})
    if box is not None:
        #taking the title
        titles = box.find('th')
        infobox['Title'] = titles.get_text(' ')
        #taking all the infos inside the infobox with a dictionary like:
        #{'Directed by': 'Quentin Tarantino'}
        for element in box.find_all('tr'):
            for attributes in element.find_all('th'):
                for name in element.find_all('td'):
                    infobox[attributes.get_text(' ')] = name.get_text(' ')
                    
    #looking for the informations that we need inside the infobox                
    for x in Box_info:
        if x in infobox:
            ##removing eventual "e.g.[3]" links
            info_clean = re.sub(clean_path, '', infobox[x])
            if info_clean:
                infos.append((' ').join(info_clean.split('\n')))
            else:
                infos.append((' ').join(infobox[x].split('\n')))
        else:
            infos.append('NA')
    
    return(infos)