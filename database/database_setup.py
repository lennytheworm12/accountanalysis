from sqlalchemy import create_engine, Column, String, Integer, Boolean, MetaData, Table, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = 'matches'
    match_id = Column(String, primary_key=True)
    participant_id = Column(Integer, primary_key=True)
    game_mode = Column(String)
    game_version = Column(String)  # Add this line
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

    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'participant_id'),
    )

def clear_db():
    # Drop the table if it exists
    Match.__table__.drop(engine)
    # Recreate the table
    Base.metadata.create_all(engine)

# Create an engine and metadata
engine = create_engine('sqlite:///league_ranks.db')
Base.metadata.create_all(engine)
