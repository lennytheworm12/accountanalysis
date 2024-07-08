from sqlalchemy import (create_engine, Column, String, Integer, Float,
                         Boolean, MetaData, Table, PrimaryKeyConstraint, JSON)
from sqlalchemy.ext.declarative import declarative_base
import os

if not os.path.exists('database/databases'):
    os.makedirs('database/databases')

Base = declarative_base()



class Match(Base):
    __tablename__ = 'matches'
    match_id = Column(String, primary_key=True)
    participant_id = Column(Integer, primary_key=True)
    game_mode = Column(String)
    game_version = Column(String)
    summoner_name = Column(String)
    summoner_id = Column(String)
    champion = Column(String)
    win = Column(Boolean)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    gold_earned = Column(Integer)
    total_damage_dealt = Column(Integer)
    total_heal = Column(Integer)
    vision_score = Column(Integer)
    queue_id = Column(Integer)  # Add this line

    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'participant_id'),
    )


class PlayerStats(Base):
    __tablename__ = 'player_stats'
    player_id = Column(String, primary_key=True)  # Unique identifier for each player
    #unique player id causes one row per player because can only have 1 player entry
    player_name = Column(String)
    flex_winrate = Column(Float)
    flex_average_kills = Column(Float)
    flex_average_deaths = Column(Float)
    flex_average_assists = Column(Float)
    flex_champion_stats = Column(JSON)  # JSON field to store per-champion stats
    solo_duo_winrate = Column(Float)
    solo_duo_average_kills = Column(Float)
    solo_duo_average_deaths = Column(Float)
    solo_duo_average_assists = Column(Float)
    solo_duo_champion_stats = Column(JSON)  # JSON field to store per-champion stats




def clear_db(table_name):
    # Reflect the table from the database
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    
    # Drop the table if it exists
    table.drop(engine)
    
    # Recreate the table
    Base.metadata.create_all(engine)

# Create an engine and metadata
engine = create_engine('sqlite:///league_ranks.db')
Base.metadata.create_all(engine)
