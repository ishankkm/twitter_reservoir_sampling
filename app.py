'''
Created on Aug 24, 2018
@author: ishank
'''

from threading import Lock
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from StreamListener import StreamListener
import tweepy

# create the Flask application
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

thread = {}
thread_lock = Lock()

# app.static_folder = './ui/build/static'
# app.template_folder = './ui/build'

# ROUTING:
@app.route("/api", methods=["GET"])
def list_routes():
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            "methods": list(rt.methods),
            "route": str(rt)
        })
    return jsonify({"routes": result, "total": len(result)})

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

def background_job(uid):

    consumer_token = "XXXXXXXXXXXXXXXXXXXXXXXXX"
    consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"
    access_token = "XXXXXXXXXXXXXXXXXXXXXXXXX"
    access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"


    TWEET_TOPIC = ['#']

    # set up tweepy
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    myStreamListener = StreamListener()
    myStreamListener.initialize(socketio, uid)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(languages=["en"], track=TWEET_TOPIC)

@socketio.on('connect')
def test_connect():

    global thread
    with thread_lock:
        if not request.sid in thread:
            thread[request.sid] = socketio.start_background_task(target=background_job, uid=request.sid)
    emit(request.sid, request.sid)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', thread[request.sid].is_alive())


if __name__ == "__main__":
    socketio.run(app, debug=True)
