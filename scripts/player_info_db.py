import pandas as pd
from sqlalchemy import create_engine
from database.database_setup import engine
from get_summoner import *
"""create data processing scripts for player stat table"""

def get_player_matches_df(summoner_id, queue_type=None):
    #define our search terms
    query = f"SELECT * FROM matches WHERE summoner_id = '{summoner_id}'"

    #if we want to find the type and it to our search reqs
    if queue_type:
        query += f"AND queue_id = {queue_type}"
    
    #set our df to our search parameters
    df = pd.read_sql(query, engine)
    return df

def compute_player_data_general(matches_df):
    #pass in the df from the other function
    
    total_games = len(matches_df)
    total_wins = matches_df['win'].sum()
    total_losses = total_games - total_wins
    win_rate = total_wins/ total_games if total_games > 0 else 0

    champion_stats = matches_df.groupby('champion').agg(
        games_played=('champion', 'count'),
        wins=('win', 'sum'),
        avg_kills=('kills', 'mean'),
        avg_deaths=('deaths', 'mean'),
        avg_assists=('assists', 'mean')
        ).reset_index()
