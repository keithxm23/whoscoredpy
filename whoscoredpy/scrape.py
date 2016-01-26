import requests
import json
import pickle

url = "http://www.whoscored.com/Matches/959654/Live/England-Premier-League-2015-2016-Newcastle-Man-Utd"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(url, headers=headers)
match_data_matcher = 'var matchCentreData = '
match_data = None
event_types_matcher = 'var matchCentreEventTypeJson = '
event_types = None
formation_types_matcher = 'var formationIdNameMappings = '
formation_types = None

if r.status_code == 200 and r.text != '':
    print(r.status_code)
    for line in r.text.splitlines():
        if match_data is None and match_data_matcher in line:
            match_data = json.loads(line.strip(match_data_matcher).strip(';'))
        if event_types is None and event_types_matcher in line:
            event_types = json.loads(line.strip(event_types_matcher).strip(';'))
        if formation_types is None and formation_types_matcher in line:
            formation_types = json.loads(line.strip(formation_types_matcher).strip(';'))
        if match_data and event_types and formation_types:
            break

    pickle.dump(match_data, open('pickles/match_data.p', 'wb'))
    pickle.dump(event_types, open('pickles/event_types.p', 'wb'))
    pickle.dump(formation_types, open('pickles/formation_types.p', 'wb'))
else:
    print('something bad happened. response: ' + r.text)



