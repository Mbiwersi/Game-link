# May have to install this package before using
from urllib.request import urlopen, Request

import requests
import json
import os

def connect():
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    #ryan token wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg
    #andrew token k0cwwccokkogcgs0sgkgcgkcwskko0g8s8c

    headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}

    # This is what we will be using to gather info from the api, what comes after the v2/ is where you put the
    # command that you want to get (friends, account, group, etc.) from this site: https://xbl.io/console
    #response = requests.get('https://xbl.io/api/v2/friends', headers=headers)
    gt = input('Type in your Xbox Gamertag: ')
    print()

    # lookup by gamertag to get id
    response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gt), headers=headers)
    resp_data = response.json()

    #Checks validity of gamertag and prompts the user again if it is invalid
    while not( 'profileUsers' in resp_data.keys()):
        print("!!Invalid Gamertag try again!!")
        gt = input('Type in your Xbox Gamertag: ')
        response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gt), headers=headers)
        resp_data = response.json()

    # Use this to print header info if needed
    # print(response.headers)

    try:
        for data in resp_data['profileUsers']:
            xuid = data['id']
    except:
        print('Gamertag not found!')
        quit()

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
        print('Gamerpic: ' + person['displayPicRaw'])

        # Gets and saves gamerpic in "gp{xuid}.png" format, has a default profile pic if call fails
        try:
            request = Request(person['displayPicRaw'], headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(request)
            with open('Gamerpics/gp' + str(person['xuid'] + '.png'), "wb") as f:
                f.write(response.read())
        except:
            with open('Gamerpics/gp' + str(person['xuid'] + '.png'), "wb") as f:
                with open('Gamerpics/defaultpic.png', 'rb') as overwrite:
                    f.write(overwrite.read())

        # print games list for person
        print('Games: ')
        for achievement in achieve_data['titles']:
            print(achievement['name'])
        print()
        print()

# Graceful program closing method
def close():
    print("Clearing gamerpic files...")
    pics = os.listdir('Gamerpics')
    for file in pics:
        if file != 'defaultpic.png':
            os.remove("Gamerpics/" + file)

if __name__ == '__main__':
    connect()
    close()
