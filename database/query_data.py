import pandas as pd
from sqlalchemy import create_engine

# Connect to the SQLite database
engine = create_engine('sqlite:///league_ranks.db')

# Query the data
def get_champion_win_rates():
    query = """
    SELECT champion, 
           COUNT(*) as games, 
           SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) as wins,
           AVG(win) as win_rate
    FROM matches
    GROUP BY champion
    """
    return pd.read_sql(query, con=engine)


