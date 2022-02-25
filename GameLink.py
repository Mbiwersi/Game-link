# May have to install this package before using
import requests
import json

def connect():
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}

    # This is what we will be using to gather info from the api, what comes after the v2/ is where you put the
    # command that you want to get (friends, account, group, etc.) from this site: https://xbl.io/console
    #response = requests.get('https://xbl.io/api/v2/friends', headers=headers)

    # Use this to print header info if needed
    # print(response.headers)

    gt = input('Type in your Xbox Gamertag: ')
    # lookup by gamertag to get id
    response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gt), headers=headers)
    resp_data = response.json()
    for data in resp_data['profileUsers']:
        xuid = data['id']

    # lookup by id to get data
    response = requests.get('https://xbl.io/api/v2/friends?xuid={}'.format(xuid), headers=headers)
    resp_data = response.json()

    # Parsing out from friends
    for person in resp_data['people']:
        ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(person['xuid']), headers=headers)
        achieve_data = ach_resp.json()

        print('Player: ' + person['displayName'])
        print('Id: ' + person['xuid'])
        print('Gamerscore: ' + person['gamerScore'])
        print('Presence: ' + person['presenceState'])
        print()
        # print games list for person
        print('Games: ')
        for achievement in achieve_data['titles']:
            print(achievement['name'])
        print()
        print()


if __name__ == '__main__':
    connect()
