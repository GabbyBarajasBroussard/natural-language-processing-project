#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import datetime as dt
import requests
from bs4 import BeautifulSoup
import os
import time
import unicodedata
import re
import json
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

from env import github_token, github_username

###########################################################################################################################################################################
def make_soup(url):
    '''
    This function takes in a url and requests and parses HTML
    returning a soup object which holds the html of the site as a text.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    return soup

###########################################################################################################################################################################
def github_ac_urls():
    '''
    This function scrapes all of the Animal Crossing urls from
    the github search page and returns a list of urls.
    '''
    # get the first 100 pages to allow for those that don't have readme or language
    pages = range(1, 101)
    urls = []
    
    for p in pages:
        
        # format string of the base url for the main github search page we are using to update with page number
        url = f'https://github.com/search?p={p}&q=animal+crossing&type=Repositories'

        # Make request and soup object using helper
        soup = make_soup(url)

        # Create a list of the anchor elements that hold the urls on this search page
        page_urls_list = soup.find_all('a', class_='v-align-middle')
        # for each url in the find all list get just the 'href' link
        page_urls = {link.get('href') for link in page_urls_list}
        # make a list of these urls
        page_urls = list(page_urls)
        # append the list from the page to the full list to return
        urls.append(page_urls)
        time.sleep(5)
        
    # flatten the urls list
    urls = [y for x in urls for y in x]
    return urls
###########################################################################################################################################################################

def github_ac_urls():
    '''
    This function scrapes all of the Animal Crossing urls from
    the github search page and returns a list of urls.
    '''
    # get the first 100 pages to allow for those that don't have readme or language
    pages = range(1, 101)
    urls = []
    
    for p in pages:
        
        # format string of the base url for the main github search page we are using to update with page number
        url = f'https://github.com/search?p={p}&q=animal+crossing&type=Repositories'

        # Make request and soup object using helper
        soup = make_soup(url)

        # Create a list of the anchor elements that hold the urls on this search page
        page_urls_list = soup.find_all('a', class_='v-align-middle')
        # for each url in the find all list get just the 'href' link
        page_urls = {link.get('href') for link in page_urls_list}
        # make a list of these urls
        page_urls = list(page_urls)
        # append the list from the page to the full list to return
        urls.append(page_urls)
        time.sleep(5)
        
    # flatten the urls list
    urls = [y for x in urls for y in x]
    return urls




