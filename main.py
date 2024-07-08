import pandas as pd
from app import app
from scripts.get_summoner import get_puuid_with_riot_id, get_match_history, get_queue_data, get_epoch_time,get_summoner_data_puuid
from scripts.process_data import add_match_history_to_table
from pprint import pprint
from database.database_setup import *
from scripts.player_info_db import get_player_matches_df, compute_player_data_general, add_and_update_player_stats

def main():
    game_name = "white swan"
    tag_line = "4242"
    account_data = get_puuid_with_riot_id(game_name, tag_line)
    puuid = account_data['puuid']

    #print(puuid)
    print('\n')
    summoner_data = (get_summoner_data_puuid(puuid))
    print(summoner_data)
    start_time = get_epoch_time(2024, 5, 15)
    end_time = get_epoch_time(2024, 5, 20)
    queue = 440
    #420 for solo q 
    match_type = 'ranked'
    table_name = 'matches'
    match_history = get_match_history(puuid, start_time=start_time, end_time=end_time, queue=queue, match_type=match_type)

    #clear_db(table_name)
    #add_match_history_to_table(match_history)
    #pprint(get_queue_data(summoner_data['id']))

    #compute player stats based on the matches 
    #matches_df = get_player_matches_df(summoner_data['id'], queue_id=queue)
    #player_stats_df = compute_player_data_general(matches_df,queue_id =queue)

    #add_and_update_player_stats(player_stats_df, 'player_stats')

    retrieved_stats = pd.read_sql(f"SELECT * FROM player_stats WHERE player_id = '{summoner_data['id']}'", engine)
    print(retrieved_stats)

    app.run#(debug=True) #debug mode on will paste in db twice


if __name__ == '__main__':
    #if os.environ.get('WERKZEUG_RUN_MAIN') or os.environ.get('FLASK_RUN_FROM_CLI'):
    main()