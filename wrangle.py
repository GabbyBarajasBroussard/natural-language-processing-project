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

"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
import pandas as pd
from requests import get
import requests
from typing import Dict, List, Optional, Union, cast
from bs4 import BeautifulSoup
from env import github_token, github_username
###########################################################################################################################################################################
# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [ 
]
###########################################################################################################################################################################
headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

###########################################################################################################################################################################
def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
            f"url: {url}"
        )
    return response_data
###########################################################################################################################################################################
def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )

###########################################################################################################################################################################
def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )

###########################################################################################################################################################################
def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""
###########################################################################################################################################################################
def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }

###########################################################################################################################################################################
def generate_repo_list():
    """
    Sends requests to the github API based on the given parameters and returns a list of names of repositories that are not empty.
    """
    repos = []
    
    for page in range(1, (_max_pages + 1)):
        response = requests.get(f"{_endpoint}?q={_query}&sort={_sort}&per_page={_per_page}&order={_order}&page={page}",\
                       headers=headers)
        payload = response.json()
        items = payload['items']

        repos += [item['full_name'] for item in items if verify_repo_not_empty(item['full_name'])]
        
    return repos




###########################################################################################################################################################################
def scrape_github_data(repos) -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
   
    
    return [process_repo(repo) for repo in repos]

###########################################################################################################################################################################
if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)

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

