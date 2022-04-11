import json
from functools import reduce

from flask import Flask, render_template ,request

import requests
import GameLink as gl

app = Flask(__name__)

headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}


@app.route('/')
def hello_world():  # put application's code here
    return render_template("Game_link.html")


@app.route('/profile/<gt>')
def get_prof(gt):
    #gamer_tag = request.args.get('gt')
    return gl.connect(gt)

@app.route('/profile/<gt>/friends')
def get_friends(gt):
    if gl.friends == {}:
        print("no friends")
        #gl.connect(gt)
    return gl.friends


@app.route('/profile/friends/incommon',methods=["POST"])
def games_in_common():
    friends= json.loads(request.data)
    games=[]
    if len(friends)!=0 :
        for f in friends:
            games.append(gl.find_matches(f))
        if len(games) != 0:
            res = list(reduce(lambda i, j: i & j, (set(n) for n in games)))
            games = [g for g in gl.player['games'] if g['name'] in res]
        else :
            return {'incommon': games}


    return {'incommon': games}






def start():
    app.run(debug=True)