# May have to install this package before using
from urllib.request import urlopen, Request
from tkinter import *
import requests
import os
from threading import Thread
import app as gui

headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}

#Now a list of objects so that the front end can access game urls
player = dict()

friends = dict()


def connect(gt):
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    # ryan token wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg
    # andrew token k0cwwccokkogcgs0sgkgcgkcwskko0g8s8c
    # michael token wsg8gwgsc48ogwskcwggcswgs840ok04o04

    response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gt), headers=headers)
    resp_data = response.json()

    # Get xuid
    xuid = 0
    for data in resp_data['profileUsers']:
        xuid = data['id']

    # set xuid
    player['xuid'] = xuid

    # lookup by id to get data
    response = requests.get('https://xbl.io/api/v2/friends?xuid={}'.format(xuid), headers=headers)
    resp_friends = response.json()

    threads = list()
    # Parsing out from friends
    for person in resp_friends['people']:
        t1 = Thread(target=get_friend_data, args=[person])
        t1.start()
        threads.append(t1)

    for thread in threads:
        thread.join()

    # get player's games
    get_my_games()

    #find  the games that match with all friends
    #Currently just does all friends
    # threads = list()
    # for friend in friends:
    #     t1 = Thread(target=find_matches, args=[friend])
    #     t1.start()
    #     threads.append(t1)
    #
    # for thread in threads:
    #     thread.join()

    # TEST WITH FRIENDS AS IF SELECTED IN GUI
    # compare_list = ['PostalBeatle398', 'StinkyTurtlShel', 'JettH17', 'Yellowacorn101', 'SEIBERTINSANO81']
    # print('Shared games with: {}'.format(compare_list))
    # print(compare_selected(compare_list))

    # print out stored friend data
    for friend in friends:
        print()
        print(friend + ': ' + str(friends[friend]))

    resp_data['games'] = player['games']
    return resp_data


# NOT BEING USED!!!!
# gets the users profile information and games list
def get_prof(gamer_tag):
    response = requests.get('https://xbl.io/api/v2/friends/search?gt={}'.format(gamer_tag), headers=headers)
    resp_data = response.json()
    # get_my_games()
    resp_data['games'] = player['games']
    return resp_data



# of the selected friends return the games that you have in common with those friends
# currently just finds the games in common with every friend
#   will change later so that all the selected friends have games in common
def find_matches(friend):
    ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(friends[friend]['xuid']),
                            headers=headers)
    achieve_data = ach_resp.json()

    friend_games_in_common = []

    # Gets the games of all the friends
    if 'titles' in achieve_data:
        for game in achieve_data['titles']:
            if game['name'] in [x['name'] for x in player['games']]:
                friend_games_in_common.append(game['name'])


    # Adding games in common to stored friends data
    friends[friend]['games_in_common'] = friend_games_in_common


# takes a list of the display names of selected friends and returns a list of the games that all friends have in common
def compare_selected(selected):
    in_common = []
    first_selected = True
    for friend in selected:
        if first_selected:
            first_selected = False
            in_common = friends[friend]['games_in_common']
        else:
            new_in_common = []
            for games_common in in_common:
                for games in friends[friend]['games_in_common']:
                    if games_common == games:
                        new_in_common.append(games_common)
                        break
            in_common = new_in_common

    return in_common


def start_gui():
    # renders flask project !!!STILL NEEDS BACK END CODE!!!! comment out if working on no gui side
    gui.start()


def get_friend_data(person):
    friend_data = dict()

    friend_data['xuid'] = person['xuid']
    friend_data['presenceState'] = person['presenceState']
    friend_data['isFavorite'] = person['isFavorite']
    friend_data['gamerScore'] = person['gamerScore']
    friend_data['displayPicRaw'] = person['displayPicRaw']

    # Stores the gamer pic in ./static/Gamerpics
    #get_gamer_pic(person)

    friend = {person['displayName']: friend_data}
    friends.update(friend)


def get_my_games():
    # Gets the current user's games
    ach_resp = requests.get('https://xbl.io/api/v2/achievements/player/{}'.format(player['xuid']), headers=headers)
    my_games_data = ach_resp.json()

    my_games = []
    print('MyGames: ')
    # !!!!FILTERS FOR XBOX ONE AND PC GAMES ONLY TO SAVE SPACE
    for game in my_games_data['titles']:
        print(game["name"])
        if "XboxOne" in game["devices"] or "XboxSeries" in game["devices"] or "PC" in game["devices"]:
            my_games.append({'name': game['name'], 'image': game["displayImage"]})
    player['games'] = my_games

    print()
    print()


if __name__ == '__main__':
    #connect()
    start_gui()
    close()
