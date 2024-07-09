import json
import pandas as pd
from sqlalchemy import create_engine, text,MetaData, Table
from .get_summoner import *
from database.database_setup import engine


def create_dataframe_from_match_data(match_data):
    matches = []
    for match in match_data:
        game_mode = match['info']['gameMode']
        game_version = match['info']['gameVersion']
        queue_id = match['info']['queueId']  # Add this line
        for participant in match['info']['participants']:
            matches.append({
                'match_id': match['metadata']['matchId'],
                'participant_id': participant['participantId'],
                'game_mode': game_mode,
                'game_version': game_version,
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
                'queue_id': queue_id  # Add this line
            })
            #we need things such as queue_id in the append part because the top is just
            #setting the variable to the returned information 
            #but to add to our df we need to append it to our list to using the top part
    df = pd.DataFrame(matches)
    df.drop_duplicates(subset=['match_id', 'participant_id'], inplace=True)
    return df


def add_match_to_table(match_id):
    try:
        # Fetch match data and create DataFrame
        match_data = [get_match_data(match_id)]
        data_frame = create_dataframe_from_match_data(match_data)
        
        # Save to SQL
        save_to_database(data_frame, 'matches')

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


"""create data processing scripts for player stat table"""


def save_to_database(df, table_name):
    try:
        existing_data = pd.read_sql_table(table_name, con=engine)
        
        if table_name == 'player_stats':
            updated_data = pd.concat([existing_data, df]).drop_duplicates(subset=['player_id'], keep='last')
        else:  # assuming it's for matches
            updated_data = pd.concat([existing_data, df]).drop_duplicates(subset=['match_id', 'participant_id'], keep='last')
        
        #update the data to the database by 
        updated_data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully updated {table_name} table.")
    
    except Exception as e:
        print(f"Error saving to database: {e}")

"""
def save_to_database(df, table_name):
    try:
        print("DataFrame to be saved to SQL:")
        print(df)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Error saving to SQL: {e}")

        """


