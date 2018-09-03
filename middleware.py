'''
Created on Aug 28, 2018
@author: ishank
'''

import json, tweepy
from StreamListener import StreamListener

class Middleware():
    
    def __init__(self, socketio, emit_at, tweet_topics=['#'], reservoir_size=10):
        self.appJson = json.load(open('app.json'))
        self._socketio = socketio
        self._streamListener = None
        self._tweet_topics = tweet_topics
        self._emit_at = emit_at
        self._reservoir_size = reservoir_size
        
    def start_background_job(self):
    
        consumer_token = self.appJson['twitter']['consumer_token']
        consumer_secret = self.appJson['twitter']['consumer_secret']
        access_token = self.appJson['twitter']['access_token']
        access_token_secret = self.appJson['twitter']['access_token_secret']
                    
        # set up tweepy
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        
        self._streamListener = StreamListener()
        self._streamListener.initialize(self._socketio, self._emit_at, self._reservoir_size)
        myStream = tweepy.Stream(auth = api.auth, listener=self._streamListener)
        myStream.filter(languages=["en"], track=self._tweet_topics)
        
    def stop_backgroung_job(self):
        self._streamListener.stop_listening()