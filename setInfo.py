import requests
import json
import string

api = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
infoApi = 'https://db.ygoprodeck.com/api/v7/cardsetsinfo.php?setcode='

sets = requests.get(api).json()

setDict = {}

def extractInfo(data, find): # extract set name and set code as well as release date
    for i in range(len(data)):
        name = data[i]['set_name'].lower()
        name = name.replace('structure deck:', '')
        name = name.replace('structure deck', '')
        name = name.replace('starter deck', '')
        name = name.replace('starter deck:', '')
        name = name.strip()
        code = data[i]['set_code']
        setDict[name] = code

    if (find in setDict):
        print('Set Code: {0}'.format(setDict[find]))
        #info = requests.get(infoApi + setDict[find]).json()
        #print(info)
    else:
        print('Invalid Set')

while True:
    choose = input('What set do you want to find?: ')
    extractInfo(sets, choose.lower())
    print(len(setDict))