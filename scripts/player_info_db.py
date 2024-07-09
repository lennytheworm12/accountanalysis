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


def compute_player_statistics(matches_df):
    total_games = len(matches_df)
    total_wins = matches_df['win'].sum()
    total_losses = total_games - total_wins
    win_rate = total_wins / total_games if total_games > 0 else 0

    champion_stats_df = matches_df.groupby('champion').agg(
        games_played=('champion', 'count'),
        wins=('win', 'sum'),
        avg_kills=('kills', 'mean'),
        avg_deaths=('deaths', 'mean'),
        avg_assists=('assists', 'mean')
    ).reset_index()

    # Round the numerical data to 2 decimal places
    champion_stats_df[['avg_kills', 'avg_deaths', 'avg_assists']] = (
        champion_stats_df[['avg_kills', 'avg_deaths', 'avg_assists']].round(2)
    )

    champion_stats_dict = champion_stats_df.to_dict(orient='records')

    return {
        'total_games': total_games,
        'win_rate': round(win_rate, 2),
        'wins': total_wins,
        'losses': total_losses,
        'champion_stats': champion_stats_dict,
        'avg_kills': round(matches_df['kills'].mean(), 2),
        'avg_deaths': round(matches_df['deaths'].mean(), 2),
        'avg_assists': round(matches_df['assists'].mean(), 2)
    }


def prepare_player_stats(player_id, player_name, stats, queue_type):
    player_stats = {
        'player_id': player_id,
        'player_name': player_name,
        'flex_winrate': 0.0,
        'flex_average_kills': 0.0,
        'flex_average_deaths': 0.0,
        'flex_average_assists': 0.0,
        'flex_champion_stats': json.dumps([]),  # Initialize as empty JSON array
        'solo_duo_winrate': 0.0,
        'solo_duo_average_kills': 0.0,
        'solo_duo_average_deaths': 0.0,
        'solo_duo_average_assists': 0.0,
        'solo_duo_champion_stats': json.dumps([]),  # Initialize as empty JSON array
    }
    #stats taken being the return from compute function taken as a dictionary arg

    if queue_type == 440:
        player_stats.update({
            'flex_winrate': stats['win_rate'],
            'flex_average_kills': stats['avg_kills'],
            'flex_average_deaths': stats['avg_deaths'],
            'flex_average_assists': stats['avg_assists'],
            'flex_champion_stats': json.dumps(stats['champion_stats'])  # Convert to JSON string
        })
    elif queue_type == 420:
        player_stats.update({
            'solo_duo_winrate': stats['win_rate'],
            'solo_duo_average_kills': stats['avg_kills'],
            'solo_duo_average_deaths': stats['avg_deaths'],
            'solo_duo_average_assists': stats['avg_assists'],
            'solo_duo_champion_stats': json.dumps(stats['champion_stats'])  # Convert to JSON string
        })
    #df = pd.DataFrame([player_stats])
    #print(f"Prepared DataFrame:\n{df}")
    return pd.DataFrame([player_stats])


def add_and_update_player_stats(player_stats_df, table_name):
    #take player df and save to the data table
    save_to_database(player_stats_df, table_name)

