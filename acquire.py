#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
############################################################################################################################
# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [ '/truc3651/AnimalCrossing',
 '/ereret2/AnimalCrossing',
 '/Sktthomas/AnimalCrossing',
 '/karatequin/AnimalCrossing',
 '/plgrazon/AnimalCrossing',
 '/StarSovu/AnimalCrossing',
 '/seolyucode/animalCrossing',
 '/Jensoevig/AnimalCrossing',
 '/SonaliZeile/AnimalCrossing',
 '/crossfx96/AnimalCrossing',
 '/longlife0428/AnimalCrossing',
 '/d21581/AnimalCrossing',
 '/CobaltBlast/AnimalCrossing',
 '/custoyang/AnimalCrossing',
 '/Nicolas27300/AnimalCrossing',
 '/hersheyj16/AnimalCrossing',
 '/KLawsonDevelopment/AnimalCrossing',
 '/KristopherKath/AnimalCrossing',
 '/gomip/animalCrossing',
 '/hososugi/AnimalCrossing',
 '/ldw394654116/animalCrossing',
 '/Yulingsong/AnimalCrossing',
 '/MartinPons/AnimalCrossing',
 '/Tsunamus/AnimalCrossing',
 '/farrasdoko/AnimalCrossing',
 '/deeluxe74/AnimalCrossing',
 '/WooseopIM/AnimalCrossing',
 '/Odinwar/AnimalCrossing',
 '/sigon/animalCrossing',
 '/arigallam3/AnimalCrossing',
 '/IdreesInc/NookPhone',
 '/nichaschang/animalCrossing',
 '/jballands/what-can-i-catch-now',
 '/BrunchPunk/wilbot',
 '/YoseptF/acnh-catalog',
 '/Corentints/coco-discord-bot',
 '/nickleee123/AnimalCrossing',
 '/vcinly/animal-crossing-slot',
 '/JanusU/AnimalCrossing',
 '/thomas-desmond/AnimalCrossing',
 '/acplaza/acplaza',
 '/teme-ts/animal-crossing',
 '/lancezeng947/animal-crossing',
 '/teclu/Animals-Crossing',
 '/Overxel/animal-crossing',
 '/rthunder27/animal-crossing',
 '/Gu-ra/Animal-CrossingMatingProgram',
 '/robertdhernandez/touhou-crossing',
 '/UniversalTourist/animal_crossing',
 '/jonpapayon/animal-crossing',
 '/Atndesign/AnimalCrossingSwoosh',
 '/Indigo94/AnimalCrossingTurnipNotifier',
 '/champymarty/animalCrossingAnimalHuntingStat',
 '/HibernantBear/AnimalCrossingTool',
 '/S0r4t4n/AnimalCrossingData',
 '/VGorski/AnimalCrossingDatabase',
 '/Robert-Robotics/animalCrossingAutomaticFisher',
 '/Kameees/Weibo_AnimalCrossing',
 '/karatequin/AnimalCrossing2.0',
 '/williamjlawson/AnimalCrossingApp',
 '/enigodupont/AnimalCrossingPlayer',
 '/ErikaJacobs/AnimalCrossing_PopularityData',
 '/Duke02/AnimalCrossing_CS588',
 '/evillalba1/animalCrossingDb',
 '/Secondbaker/AnimalCrossingTracker',
 '/jj2eun/AnimalCrossing-spring',
 '/HaizhiH/AnimalCrossingQRCodes',
 '/RedishTiger/AnimalCrossingPlugin-----------------------------------------------',
 '/djigoio/AnimalCrossing-NH-Encyclopedia',
 '/scavet64/AnimalCrossingCritters',
 '/victorvermot/AnimalCrossingPrices',
 '/ldw394654116/animalCrossingExpress',
 '/Volvion/Animal-Crossing-Animal-Town',
 '/Coalery/AnimalCrossingBot',
 '/BreannW/AnimalCrossingBulletJournal',
 '/al97/AnimalCrossingCatches',
 '/martinwjwilson/AnimalCrossingDiscord',
 '/strawstack/AnimalCrossingTextBubble',
 '/Chudly63/AnimalCrossingDJ',
 '/racheldosh/AnimalCrossingCalculator',
 '/Cerfio/animalCrossingShare',
 '/chriswebb31/AnimalCrossingReviews',
 '/aislingxmcgrath/AnimalCrossingQ',
 '/zhengbanwansui/09____AnimalCrossingHelper',
 '/ProjectNS/AnimalCrossingExchange',
 '/JanusU/AnimalCrossingPrev',
 '/Hellorocio/AnimalCrossingSerotoninGenerator',
 '/cashutten/AnimalCrossingTools',
 '/JakeCoffey/AnimalCrossingCatalog',
 '/Marlon-Pascual-Marrero-Arancibia/AnimalCrossing-Catchphrase-Generator'
]
############################################################################################################################
headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

############################################################################################################################
def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
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

###################################################################################################################################
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




########################################
def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]

###########################################################################################################################################################################
if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)

###################################################################################################################################