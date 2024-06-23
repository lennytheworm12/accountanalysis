import requests
from urllib.parse import quote

from bs4 import BeautifulSoup

#get player name and grab data

def fetchPage(playerName, region):
    #grab the html content of an op.gg page for a player
    encodedPlayerName = quote(playerName) #for special characters
    url = f"https://www.op.gg/summoners/{region}/{encodedPlayerName}"

    response = requests.get(url)
    response.raise_for_status() #raise error incase bad statuses
    return response.text


def parsePage(htmlContent):
    #takes the contents of the page and reads it 
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup


def extractWinRates(soup):

    winRates = {}
    try:
        winRates['solo/duo'] = soup.select_one('div.solo-winrate').text.strip()
        winRates['flex'] = soup.select_one('div.flex-winrate').text.strip()
    except AttributeError:
        pass
    return winRates


def extractKDA(soup):
    kdas = {}
    try:
        kdaElements = soup.select('div.kda-champion')

        for el in kdaElements:
            championName = el.select_one('span.champion-name').text.strip()
            kdaValue = el.select_one('span.kda-value').text.strip()
            kdas[championName] = kdaValue
    except AttributeError:
        pass
    return kdas


def get_summoner_data(summoner_name, region):
    encoded_summoner_name = quote(summoner_name)
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encoded_summoner_name}'
    headers = {
        'X-Riot-Token': 'RGAPI-49e481cc-e979-4da6-990a-3de025c3c26c'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an error for bad status codes
    return response.json()