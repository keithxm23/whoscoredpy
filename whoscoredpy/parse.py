import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Game, Team, Player, TeamPlayer, Manager, TeamManager

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

def process_map_record(klass, obj, key1, key2, session):
    o = session.query(klass.id).filter(
            getattr(klass, key1) == obj[key1],
            getattr(klass, key2) == obj[key2]).one_or_none()
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

def process_team_manager(tm_mgr_obj, session):
    return process_map_record(TeamManager, tm_mgr_obj, 'team_id', 'manager_id', session)

def process_player(player_obj, session):
    return process_record(Player, player_obj, 'ws_id', session)

def process_team_player(tm_plyr_obj, session):
    return process_map_record(TeamPlayer, tm_plyr_obj, 'team_id', 'player_id', session)


home = match_data['home']
away = match_data['away']

h_team_id = process_team({'ws_id': home['teamId'], 'name': home['name']}, session)
a_team_id = process_team({'ws_id': away['teamId'], 'name': away['name']}, session)

h_manager_id = process_manager({'name':home['managerName']}, session)
a_manager_id = process_manager({'name':away['managerName']}, session)

h_team_mgr_id = process_team_manager({'team_id': h_team_id,
                                      'manager_id' : h_manager_id}, session)
a_team_mgr_id = process_team_manager({'team_id': a_team_id, 
                                      'manager_id' : a_manager_id}, session)

h_team_plyrs = []
a_team_plyrs = []
for p in home['players'] + away['players']:
    plyr_obj = {}
    plyr_obj['ws_id'] = p['playerId']
    plyr_obj['name'] = p['name']
    plyr_obj['age'] = p['age']
    plyr_obj['height'] = p['height']
    plyr_obj['weight'] = p['weight']
    plyr_obj['shirt'] = p['shirtNo']
    plyr_id = process_player(plyr_obj, session)
    if p['field'] == 'home':
        h_team_plyrs.append(process_team_player({'team_id':h_team_id, 
            'player_id': plyr_id}, session))
        h_team_plyrs.append(plyr_id)
    else:
        a_team_plyrs.append(process_team_player({'team_id': a_team_id, 
            'player_id': plyr_id}, session))
        a_team_plyrs.append(plyr_id)


session.commit()
