import json
import pandas as pd
from sqlalchemy import create_engine, text,MetaData, Table
from scripts.get_summoner import *
from database.database_setup import *

engine = create_engine('sqlite:///league_ranks.db')

def create_dataframe_from_match_data(match_data):
    matches = []
    for match in match_data:
        game_mode = match['info']['gameMode']
        game_version = match['info']['gameVersion']
        for participant in match['info']['participants']:
            matches.append({
                'match_id': match['metadata']['matchId'],
                'participant_id': participant['participantId'],
                'game_mode': game_mode,
                'game_version': game_version,  # Add this line
                'summoner_name': participant['summonerName'],
                'summoner_id': participant['summonerId'],
                'champion': participant['championName'],
                'win': participant['win'],
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists'],
                'gold_earned': participant['goldEarned'],
                'total_damage_dealt': participant['totalDamageDealt'],
                'total_heal': participant['totalHeal'],
                'vision_score': participant['visionScore'],
            })
    df = pd.DataFrame(matches)
    # Ensure no duplicates
    df.drop_duplicates(subset=['match_id', 'participant_id'], inplace=True)
    return df



def add_match_to_table(match_id):
    try:
        # Check if the match_id already exists
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT 1 FROM matches WHERE match_id = :match_id LIMIT 1"), {'match_id': match_id}).fetchone()
        
        # If the match_id exists, skip processing
        if result is not None:
            print(f"Match {match_id} already exists. Skipping.")
            return

        # Fetch match data and create DataFrame
        match_data = [get_match_data(match_id)]
        data_frame = create_dataframe_from_match_data(match_data)
        
        # Save to SQL
        save_to_sql(data_frame)

    except Exception as e:
        print(f"Error processing match {match_id}: {e}")


def add_match_history_to_table(match_history):

    for match_id in match_history:
        try:
            add_match_to_table(match_id)
        except Exception as e:
            #log error and continue
            print(f"Skipping match {match_id} due to error: {e}")
    return 0



# Function to save DataFrame to SQL database

def save_to_sql(df, table_name='matches'):
    try:
        print("DataFrame to be saved to SQL:")
        print(df)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Error saving to SQL: {e}")
"""
def clear_db():
    metadata = MetaData()
    metadata.reflect(bind=engine)
    matches = metadata.tables['matches']
    with engine.connect() as connection:
        connection.execute(matches.delete())
        """