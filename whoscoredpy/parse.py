import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Game, Team, Player, TeamPlayer, Manager

match_data = pickle.load(open('pickles/match_data.p', 'rb'))
event_types = pickle.load(open('pickles/event_types.p', 'rb'))
formation_types = pickle.load(open('pickles/formation_types.p', 'rb'))

engine = create_engine('sqlite:///whoscored.db', echo=True)
Session = sessionmaker(bind=engine)
session=Session()

def process_record(klass, obj, key, session):
    o = session.query(klass.id).filter(getattr(klass, key) == obj[key]).one_or_none()
    if o is not None:
        return o[0]
    else:
        o = klass(**obj)
        session.add(o)
        session.flush()
        session.refresh(o)
        return o.id

def process_team(team_obj, session):
    return process_record(Team, team_obj, 'ws_id', session)

def process_manager(manager_obj, session):
    return process_record(Manager, manager_obj, 'name', session)

def process_player(player_obj, session):
    pass

home = match_data['home']
away = match_data['away']

h_team_id = process_team({'ws_id': home['teamId'], 'name': home['name']}, session)
a_team_id = process_team({'ws_id': away['teamId'], 'name': away['name']}, session)

h_manager_id = process_manager({'name':home['managerName']}, session)
a_manager_id = process_manager({'name':away['managerName']}, session)

session.commit()
