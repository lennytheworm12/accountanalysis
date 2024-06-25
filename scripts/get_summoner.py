import requests
from urllib.parse import quote
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('RIOT_API_KEY')

def get_epoch_time(year, month, day):
    dt = datetime(year, month, day)
    return int(dt.timestamp())


#time our requests so we dont get errors
def rate_limited_request(url, headers, params=None):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 429:  # Too Many Requests
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limit hit, retrying after {retry_after} seconds...")
        time.sleep(retry_after)
        return rate_limited_request(url, headers, params)
    return response


def make_api_request(url, params=None):
    headers = {
        'X-Riot-Token': API_KEY
    }
    response = rate_limited_request(url, headers, params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json()}")
        response.raise_for_status()
    
    return response.json()

def get_puuid_with_riot_id(game_name, riot_id):
    url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{quote(game_name)}/{quote(riot_id)}'

    return make_api_request(url)


def get_summoner_data_puuid(puuid):
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'

    return make_api_request(url)


#440 for flex type ranked
def get_match_history(puuid, start_time=None, end_time=None, queue=None, match_type=None, start=0, count=100):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'

    
    params = {
        'start': start,
        'count': count,
        'startTime': start_time,
        'endTime': end_time,
        'queue': queue,
        'type': match_type
    }
    
    params = {k: v for k, v in params.items() if v is not None}
    #k being key and v being value 
    # for each key and value in params if the value is not none
    # then add to this new dict
    
    return make_api_request(url, params = params)
#return a list of match ids


def get_match_data(match_id):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

    return make_api_request(url)


def get_match_timeline(match_id):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline'
    
    return make_api_request(url)


#summoner id is id from get summoner data
def get_queue_data(summoner_id):
    url = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'

    return make_api_request(url)


def get_league_leagueid(league_id):

    url = f'https://na1.api.riotgames.com/lol/league/v4/leagues/{league_id}'

    return make_api_request(url)