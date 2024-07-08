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
        save_to_sql(data_frame, 'matches')

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



# Function to check if the data already exists 
def data_exists(record_id, table_name, id_column, participant_id=None):
    with engine.connect() as connection:
        if participant_id is not None:
            query = text(f"SELECT 1 FROM {table_name} WHERE {id_column} = :record_id AND participant_id = :participant_id LIMIT 1")
            result = connection.execute(query, {'record_id': record_id, 'participant_id': participant_id}).fetchone()
        else:
            query = text(f"SELECT 1 FROM {table_name} WHERE {id_column} = :record_id LIMIT 1")
            result = connection.execute(query, {'record_id': record_id}).fetchone()
        return result is not None
#function append stats in for cases like adding
def append_record(row, table_name):
    row_df = pd.DataFrame([row])
    row_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def update_player_stats(row, table_name):
    with engine.connect() as connection:
        query = text(f"""
            UPDATE {table_name}
            SET player_name = :player_name,
                flex_winrate = :flex_winrate,
                flex_average_kills = :flex_average_kills,
                flex_average_deaths = :flex_average_deaths,
                flex_average_assists = :flex_average_assists,
                flex_champion_stats = :flex_champion_stats,
                solo_duo_winrate = :solo_duo_winrate,
                solo_duo_average_kills = :solo_duo_average_kills,
                solo_duo_average_deaths = :solo_duo_average_deaths,
                solo_duo_average_assists = :solo_duo_average_assists,
                solo_duo_champion_stats = :solo_duo_champion_stats
            WHERE player_id = :player_id
        """)
        connection.execute(query, **row.to_dict())


# Function to save DataFrame to SQL database
def save_to_sql(df, table_name):
    for _, row in df.iterrows():
        if table_name == 'player_stats':
            #state variables just to make things cleaner
            record_id = row['player_id']
            id_column = 'player_id'
            update_function = update_player_stats

            # Check if the record already exists in the table
            if data_exists(record_id, table_name, id_column):
                # Update existing record
                update_function(row, table_name)
            else:
                # Append new record
                append_record(row, table_name)
        else:
            #this else logic is used for match data appending
            #we still have to check for dupes 
            record_id = row['match_id']
            id_column = 'match_id'
            participant_id = row['participant_id']

            if not data_exists(record_id, table_name, id_column, participant_id):
                append_record(row, table_name)
"""
def save_to_sql(df, table_name):
    try:
        print("DataFrame to be saved to SQL:")
        print(df)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Error saving to SQL: {e}")

        """


