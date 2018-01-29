import urllib.request as re
import json
import pandas as pd

# "id": 2063 # "name": "Aggramar" # "npcID": 121975
# "id": 2092  # "name": "Argus the Unmaker" # "npcID": 124828

urlBase = 'https://www.warcraftlogs.com/v1/'
apiCode = '815821a51e615e23e86995e9e5696697'
typeString = 'rankings/encounter/'
encounterId = '2063'
# 4 = heroic
difficulty = '5'
# 	The metric to query for. Valid fight metrics are 'speed', 'execution' and 'feats'.
# Valid character metrics are 'dps', 'hps', 'bossdps, 'tankhps', or 'playerspeed'.
# For WoW only, 'krsi' can be used for tank survivability ranks and 'progress' can be used for guild progress info.
metric = 'dps'
urlString = urlBase + typeString + encounterId + '?api_key=' + apiCode + '&difficulty=' + difficulty + '&metric=' + metric + '&region=KR&limit=5000'

jsonUrl = re.urlopen(urlString)
# print(urlString)
data = json.load(jsonUrl)
# print(data)
#data['rankings'][0].keys()
# dict_keys(['name', 'class', 'spec', 'total', 'duration', 'startTime', 'fightID', 'reportID', 'guild', 'server', 'region', 'hidden', 'itemLevel', 'exploit', 'talents', 'gear', 'rankid', 'size'])
# dict_keys(['duration', 'startTime', 'damageTaken', 'deaths', 'fightID', 'reportID', 'guild', 'server', 'region', 'exploit', 'tanks', 'healers', 'melee', 'ranged', 'faction', 'itemLevel', 'verified', 'locked'])

reportList = []

for rows in data['rankings']:
    # print(rows['reportID'])
    reportList.append(rows['reportID'])

df = pd.DataFrame({'reports': reportList})
# print(df)
dfDrop = df.drop_duplicates()
len(df)
len(dfDrop)
dfDrop.head()

dfDict = dfDrop.to_dict('records')

dfDict

for rows in dfDict:
    print(rows['reports'])

reportID = dfDict[1]['reports']

# fight info
# get 2063(Aggramar)'s fight info
# https://www.warcraftlogs.com/v1/report/fights/BA1azbchdM83FWC7?api_key=815821a51e615e23e86995e9e5696697

typeString = 'report/fights/'
urlStringForFight = urlBase + typeString + reportID + '?api_key=' + apiCode

jsonUrl = re.urlopen(urlStringForFight)
dataFight = json.load(jsonUrl)
fightList = []
tmpDict = {}

for rows in dataFight['fights']:
    if rows['boss'] == 2063:
        tmpDict = {'id' : rows['id'] , 'start' : rows['start_time'], 'end': rows['end_time'] }
        fightList.append(tmpDict)

fightList

# event info
# reportID + start + end
# https://www.warcraftlogs.com/v1/report/events/BA1azbchdM83FWC7?api_key=815821a51e615e23e86995e9e5696697&start=2082167&end=2196818
# for rows in fightList:
    #print(rows)

typeString = 'report/events/'
start = '430264'
end = '618944'
urlStringForEvent = urlBase + typeString + reportID + '?api_key=' + apiCode + '&start=' + start + '&end=' + end
urlStringForEvent
jsonUrl = re.urlopen(urlStringForEvent)
dataEvent = json.load(jsonUrl)

#table
#viewtype / reportID / start / end

view = 'healing/'
typeString = 'report/tables/'
urlStringForTable = urlBase + typeString + view + reportID + '?api_key=' + apiCode + '&start=' + start + '&end=' + end
urlStringForTable
jsonUrl = re.urlopen(urlStringForTable)
dataTable = json.load(jsonUrl)


dataTable