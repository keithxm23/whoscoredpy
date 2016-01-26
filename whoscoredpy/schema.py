import os
import sqlalchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean


engine = create_engine('sqlite:///whoscored.db', echo=True)
Base = declarative_base()

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    league = Column(String)
    attendance = Column(Integer)
    referee = Column(String)
    venue = Column(String)
    start_time = Column(Date)
    weatherCode = Column(Integer)
    ht_score = Column(String)
    ft_score = Column(String)
    et_score = Column(String)
    home_id = Column(Integer, ForeignKey('performances.id')) 
    away_id = Column(Integer, ForeignKey('performances.id')) 

class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id')) 
    team_manager_id = Column(Integer, ForeignKey('team_managers.id')) 

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    ws_id = Column(Integer)
    name = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    shirt = Column(Integer)
    position = Column(String)

class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class TeamManager(Base):
    __tablename__ = "team_managers"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id')) 
    manager_id = Column(Integer, ForeignKey('managers.id')) 


class TeamPlayer(Base):
    __tablename__ = "team_players"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id')) 
    player_id = Column(Integer, ForeignKey('players.id')) 


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    ws_id = Column(Integer)
    name = Column(String)


class PlayerPerformaceMap(Base):
    __tablename__ = "player_performance_map"
    id = Column(Integer, primary_key=True)
    performance_id = Column(Integer, ForeignKey('performances.id')) 
    game_id = Column(Integer, ForeignKey('games.id')) 
    team_player_id = Column(Integer, ForeignKey('team_players.id')) 
    started = Column(Boolean)
    motm = Column(Boolean)

class EventType(Base):
    __tablename__ = "event_types"
    id = Column(Integer, primary_key=True)
    ws_id = Column(Integer)
    name = Column(String)

class FormationType(Base):
    __tablename__ = "formation_types"
    id = Column(Integer, primary_key=True)
    ws_id = Column(Integer)
    name = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id')) 
    team_id = Column(Integer, ForeignKey('teams.id')) 
    team_player_id = Column(Integer, ForeignKey('team_players.id')) 
    ws_id = Column(Integer)
    touch = Column(Boolean)
    outcome = Column(String)
    x = Column(Float)
    y = Column(Float)
    end_x = Column(Float)
    end_y = Column(Float)
    event_type = Column(String)
    satisfied_event_tpes = Column(String)


Base.metadata.create_all(engine)
