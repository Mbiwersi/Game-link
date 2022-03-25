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
    gamer_tag = request.args.get('gt')
    # return gamer_tag
    return gl.get_prof(gt)

@app.route('/profile/<gt>/friends')
def get_friends(gt):
    if gl.friends == {} :
        gl.connect(gt)
    return gl.friends



def start():
    app.run(debug=True)

