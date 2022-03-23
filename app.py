from flask import Flask, render_template ,request

import requests
import GameLink as gl

app = Flask(__name__)

headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}


@app.route('/')
def hello_world():  # put application's code here
    return render_template("Game_link.html")


@app.route('/profile')
def get_prof():
    # gamer_tag = request.args.get('thatginger890')
    return gl.get_prof('thatginger890')


def start():
    app.run(debug=True)

