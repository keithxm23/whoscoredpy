import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Game, Team, Player, TeamPlayer

match_data = pickle.load(open('pickles/match_data.p', 'rb'))
event_types = pickle.load(open('pickles/event_types.p', 'rb'))
formation_types = pickle.load(open('pickles/formation_types.p', 'rb'))

engine = create_engine('sqlite:///whoscored.db', echo=True)
Session = sessionmaker(bind=engine)
session=Session()

def process_player(player_obj, session):
    pass

def process_team(team_obj, session):
    team = session.query(Team.id).filter(Team.ws_id == team_obj['ws_id']).one_or_none()
    if team is not None:
        return team[0]
    else:
        team = Team(**team_obj)
        session.add(team)
        session.flush()
        session.refresh(team)
        return team.id

def process_manager(manager_obj, session):
    pass


home_team_id = process_team({'ws_id': match_data['home']['teamId'],
    'name': match_data['home']['name']}, session)
away_team_id = process_team({'ws_id': match_data['away']['teamId'],
    'name': match_data['away']['name']}, session)

#manager_id = process_manager({}, session)

session.commit()
