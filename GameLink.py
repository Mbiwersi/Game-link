# May have to install this package before using
from urllib.request import urlopen, Request

import requests
import json
import os

headers = {"X-Authorization": "wsg8gwgsc48ogwskcwggcswgs840ok04o04"}


def connect():
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    #ryan token wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg
    #andrew token k0cwwccokkogcgs0sgkgcgkcwskko0g8s8c

    # This is what we will be using to gather info from the api, what comes after the v2/ is where you put the
    # command that you want to get (friends, account, group, etc.) from this site: https://xbl.io/console
    #response = requests.get('https://xbl.io/api/v2/friends', headers=headers)

    xuid = get_user()

    # lookup by id to get data
    response = requests.get('https://xbl.io/api/v2/friends?xuid={}'.format(xuid), headers=headers)
    resp_data = response.json()

    # find the games that match with all friends
    # Currently just does all friends
    findMatches(resp_data)


    # Parsing out from friends
    for person in resp_data['people']:
        ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(person['xuid']), headers=headers)
        achieve_data = ach_resp.json()

        print('Player: ' + person['displayName'])
        print('Id: ' + person['xuid'])
        print('Gamerscore: ' + person['gamerScore'])
        print('Presence: ' + person['presenceState'])
        print('Gamerpic: ' + person['displayPicRaw'])

        # Stores the gamer pic in ./Gamerpics
        get_gamer_pic(person)

        # print games list for person
        print('Games: ')
        for achievement in achieve_data['titles']:
            print(achievement['name'])
        print()
        print()

# prompt for Xbox Gamer tage and return the xuid
def get_user():
    gt = input('Type in your Xbox Gamertag: ')
    print()

    # lookup by gamertag to get id
    response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gt), headers=headers)
    resp_data = response.json()

    # Checks validity of gamertag and prompts the user again if it is invalid
    while not ('profileUsers' in resp_data.keys()):
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

    return xuid

def get_gamer_pic(person):
    # Gets and saves gamerpic in "{xuid}.png" format, has a default profile pic if call fails
    try:
        request = Request(person['displayPicRaw'], headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request)
        with open('Gamerpics/gp_' + str(person['displayName'] + '.png'), "wb") as f:
            f.write(response.read())
    except:
        with open('Gamerpics/gp_' + str(person['displayName'] + '.png'), "wb") as f:
            with open('Gamerpics/defaultpic.png', 'rb') as overwrite:
                f.write(overwrite.read())


# Graceful program closing method
def close():
    print("Clearing gamerpic files...")
    pics = os.listdir('Gamerpics')
    for file in pics:
        if file != 'defaultpic.png':
            os.remove("Gamerpics/" + file)

# of the selected friends return the games that you have in common with those friends
# currently just finds the games in common with every friend
#   will change later so that all the selected friends have games in common
# return a dict in the form of {'friend_displayName1': [game1, game2, ...] 'friend_displayName2': [game1, game2, ...}
def findMatches(selectedFriends):
    # Gets the current user's games
    ach_resp = requests.get('https://xbl.io/api/v2/achievements/', headers=headers)
    myGamesData = ach_resp.json()

    myGames = []
    print('MyGames: ')
    for game in myGamesData['titles']:
        print(game['name'])
        myGames.append(game['name'])
    print()
    print()
    print(myGames)

    gamesincommon = {}

    # Gets each friends achievements
    for friend in selectedFriends['people']:
        ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(friend['xuid']), headers=headers)
        achieve_data = ach_resp.json()
        print("Friend {} has these games in common:".format(friend['displayName']))
        friendGamesIncommon = []

        # Gets the games of all the friends
        for game in achieve_data['titles']:
            if game['name'] in myGames:
                print(game['name'])
                friendGamesIncommon.append(game['name'])
        gamesincommon[friend['displayName']] = friendGamesIncommon # can swap for xuid if we want instead of displayName

        print()
    # print(gamesincommon)
    return gamesincommon

if __name__ == '__main__':
    connect()
    close()
