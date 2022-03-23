import wtf as wtf
from flask import Flask, render_template ,request

import GameLink as gl

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("Game_link.html")

def start():
    app.run(debug=True)

