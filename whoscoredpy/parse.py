import requests
import json

url = "http://www.whoscored.com/Matches/959654/Live/England-Premier-League-2015-2016-Newcastle-Man-Utd"

r = requests.get(url)
match_data_matcher = 'var matchCentreData = '
match_data = None
event_types_matcher = 'var matchCentreEventTypeJson = '
event_types = None
formation_types_matcher = 'var formationIdNameMappings = '
formation_types = None

if r.status_code == 200 and r.text != '':
    print r.status_code
    for line in r.text.splitlines():
        if match_data is None and match_data_matcher in line:
            match_data = json.loads(line.strip(match_data_matcher).strip(';'))
        if event_types is None and event_types_matcher in line:
            event_types = json.loads(line.strip(event_types_matcher).strip(';'))
        if formation_types is None and formation_types_matcher in line:
            formation_types = json.loads(line.strip(formation_types_matcher).strip(';'))
        if match_data and event_types and formation_types:
            break
else:
    print 'something bad happened. response: ' + r.text



