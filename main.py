
from app import app
from scripts.scrape import fetchPage, parsePage, get_summoner_data
from scripts.get_summoner import *
from scripts.process_data import *
from pprint import pprint
from database.database_setup import *
#can do import * but not recommended bc can lead to errors

def main():
    game_name = "white swan"
    tag_line = "4242"
    account_data = get_puuid_with_riot_id(game_name, tag_line)
    puuid = account_data['puuid']

    #print(puuid)
    print('\n')
    summoner_data = (get_summoner_data_puuid(puuid))
    #print(summoner_data)
    start_time = get_epoch_time(2024, 5, 15)
    end_time = get_epoch_time(2024, 6, 24)
    queue = 440
    match_type = 'ranked'

    match_history = get_match_history(puuid, start_time=start_time, end_time=end_time, queue=queue, match_type=match_type)

    clear_db()
    add_match_history_to_table(match_history)
    #add_match_history_to_table(match_history)

    app.run#(debug=True) #debug mode on will paste in db twice


if __name__ == '__main__':
    #if os.environ.get('WERKZEUG_RUN_MAIN') or os.environ.get('FLASK_RUN_FROM_CLI'):
    main()