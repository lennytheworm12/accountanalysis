
from app import app
from scripts.scrape import fetchPage, parsePage, get_summoner_data
from scripts.get_summoner import *
from pprint import pprint

#can do import * but not recommended bc can lead to errors

def main():
    game_name = "white swan"
    tag_line = "4242"
    account_data = get_puuid_with_riot_id(game_name, tag_line)
    puuid = account_data['puuid']

    #print(puuid)
    print('\n')
    summoner_data = (get_summoner_data_puuid(puuid))
    print(summoner_data)
    print((get_match_history(puuid)))
    #pprint(get_match_data('NA1_5024991435'))
    pprint(get_queue_data(summoner_data['id']))
    app.run(debug=True)


if __name__ == '__main__':
    main()
