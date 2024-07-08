import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from database.database_setup import engine
from .get_summoner import *
from .process_data import *
"""create data processing scripts for player stat table"""

#get matches from the table
def get_player_matches_df(summoner_id, queue_id=None):
    #define our search terms
    query = f"SELECT * FROM matches WHERE summoner_id = '{summoner_id}'"

    #if we want to find the type and it to our search reqs
    if queue_id:
        query += f"AND queue_id = {queue_id}"
    
    #set our df to our search parameters
    df = pd.read_sql(query, engine)
    return df


def compute_player_data_general(matches_df,queue_id):
    #pass in the df from the other function
    
    total_games = len(matches_df)
    total_wins = matches_df['win'].sum()
    total_losses = total_games - total_wins
    win_rate = total_wins/ total_games if total_games > 0 else 0

    champion_stats_dict = matches_df.groupby('champion').agg(
        games_played=('champion', 'count'),
        wins=('win', 'sum'),
        avg_kills=('kills', 'mean'),
        avg_deaths=('deaths', 'mean'),
        avg_assists=('assists', 'mean')
        ).reset_index().to_dict(orient = 'records')
    # kind of funky but instead of making champion stats df variable and then
    #making new varible to set it to a dict we just jumble the methods in one 

    if queue_id == 440:  # Flex queue
        player_stats = {
            'player_id': matches_df['summoner_id'].iloc[0],
            'player_name': matches_df['summoner_name'].iloc[0],
            'flex_winrate': win_rate,
            'flex_average_kills': matches_df['kills'].mean(),
            'flex_average_deaths': matches_df['deaths'].mean(),
            'flex_average_assists': matches_df['assists'].mean(),
            'flex_champion_stats': json.dumps(champion_stats_dict),
            'solo_duo_winrate': None,  # Placeholder
            'solo_duo_average_kills': None,  # Placeholder
            'solo_duo_average_deaths': None,  # Placeholder
            'solo_duo_average_assists': None,  # Placeholder
            'solo_duo_champion_stats': None  # Placeholder
        }
    elif queue_id == 420:  # Solo/Duo queue
        player_stats = {
            'player_id': matches_df['summoner_id'].iloc[0],
            'player_name': matches_df['summoner_name'].iloc[0],
            'flex_winrate': None,  # Placeholder
            'flex_average_kills': None,  # Placeholder
            'flex_average_deaths': None,  # Placeholder
            'flex_average_assists': None,  # Placeholder
            'flex_champion_stats': None,  # Placeholder
            'solo_duo_winrate': win_rate,
            'solo_duo_average_kills': matches_df['kills'].mean(),
            'solo_duo_average_deaths': matches_df['deaths'].mean(),
            'solo_duo_average_assists': matches_df['assists'].mean(),
            'solo_duo_champion_stats': json.dumps(champion_stats_dict)
        }
    df = pd.DataFrame([player_stats])
    return df #return a df


def add_and_update_player_stats(player_stats_df, table_name):
    #take player df and save to the data table
    save_to_sql(player_stats_df, table_name)

