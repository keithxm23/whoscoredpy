import pickle
from sqlalchemy.orm import sessionmaker
from schema import Game, Team, Player, TeamPlayer

match_data = pickle.load(open('match_data.p', 'rb'))
event_types = pickle.load(open('event_types.p', 'rb'))
formation_types = pickle.load(open('formation_types.p', 'rb'))

Session = sessionmaker(bind=engine)
session=Session()


