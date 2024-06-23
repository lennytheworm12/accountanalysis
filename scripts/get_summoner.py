import requests
from urllib.parse import quote
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('RIOT_API_KEY')

def make_api_request(url):
    headers = {
        'X-Riot-Token': API_KEY
    }
    response = requests.get(url, headers=headers)
    
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


def get_match_history(puuid, start_time=None, end_time=None, queue=None, match_type=None, start=0, count=20):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}'
    
    if start_time:
        url += f'&startTime={start_time}'
    if end_time:
        url += f'&endTime={end_time}'
    if queue:
        url += f'&queue={queue}'
    if match_type:
        url += f'&type={match_type}'
    
    return make_api_request(url)


def get_match_data(match_id):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

    return make_api_request(url)


def get_match_timeline(match_id):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline'
    
    return make_api_request(url)


def get_queue_data(summoner_id):
    url = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'

    return make_api_request(url)


def get_league_leagueid(league_id):

    url = f'https://na1.api.riotgames.com/lol/league/v4/leagues/{league_id}'

    return make_api_request(url)