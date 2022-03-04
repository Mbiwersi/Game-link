# May have to install this package before using
from urllib.request import urlopen, Request

import requests
import os

headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}
player = dict()
friends = dict()


def connect():
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    #ryan token wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg
    #andrew token k0cwwccokkogcgs0sgkgcgkcwskko0g8s8c
    #michael token wsg8gwgsc48ogwskcwggcswgs840ok04o04

    xuid = get_user()
    player['xuid'] = xuid

    # lookup by id to get data
    response = requests.get('https://xbl.io/api/v2/friends?xuid={}'.format(xuid), headers=headers)
    resp_data = response.json()

    # Parsing out from friends
    for person in resp_data['people']:

        friend_data = dict()

        friend_data['xuid'] = person['xuid']
        friend_data['presenceState'] = person['presenceState']
        friend_data['isFavorite'] = person['isFavorite']
        friend_data['gamerScore'] = person['gamerScore']

        # Stores the gamer pic in ./Gamerpics
        get_gamer_pic(person)

        friend = {person['displayName']: friend_data}
        friends.update(friend)

    # find the games that match with all friends
    # Currently just does all friends
    findMatches(resp_data)

    # TEST WITH FRIENDS AS IF SELECTED IN GUI
    compare_list = ['Yellowacorn101', 'StinkyTurtlShel', 'JettH17', 'PostalBeatle398', 'SEIBERTINSANO81']
    print('Shared games with: {}'.format(compare_list))
    print(compare_selected(compare_list))

    # print out stored friend data
    for friend in friends:
        print()
        print(friend + ': ' + str(friends[friend]))

# prompt for Xbox Gamer tag and return the xuid
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
    for data in resp_data['profileUsers']:
        xuid = data['id']

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
def findMatches(selectedFriends):
    # Gets the current user's games
    ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(player['xuid']), headers=headers)
    myGamesData = ach_resp.json()

    myGames = []
    print('MyGames: ')
    for game in myGamesData['titles']:
        print(game['name'])
        myGames.append(game['name'])
    player['games'] = myGames

    print()
    print()

    # Gets each friends achievements
    for friend in selectedFriends['people']:
        ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(friend['xuid']), headers=headers)
        achieve_data = ach_resp.json()
        print("Friend {} has these games in common:".format(friend['displayName']))
        friendGamesInCommon = []

        # Gets the games of all the friends
        for game in achieve_data['titles']:
            if game['name'] in myGames:
                print(game['name'])
                friendGamesInCommon.append(game['name'])

        # Adding games in common to stored friends data
        friends[friend['displayName']]['gamesInCommon'] = friendGamesInCommon

        print()

# takes a list of the display names of selected friends and returns a list of the games that all friends have in common
def compare_selected(selected):
    in_common = []
    first_selected = True
    for friend in selected:
        if first_selected:
            first_selected = False
            in_common = friends[friend]['gamesInCommon']
        else:
            new_in_common = []
            for games_common in in_common:
                in_both = False
                for games in friends[friend]['gamesInCommon']:
                    if games_common == games:
                        in_both = True
                        new_in_common.append(games_common)
                        break
            in_common = new_in_common

    return in_common




if __name__ == '__main__':
    connect()
    close()
