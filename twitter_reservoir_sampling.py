'''
Created on Jul 29, 2018
@author: ishank
'''

from __future__ import print_function
from __future__ import division
from StreamListener import StreamListener
import sys, tweepy

consumer_token = "XXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"

def main():
        
    TWEET_TOPIC = ['#']
    
    if len(sys.argv) > 1:                
        TWEET_TOPIC = sys.argv[1:]
    
    # set up tweepy
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # create a stream listener 
    myStreamListener = StreamListener()
    myStreamListener.initialize()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=TWEET_TOPIC)
    
if __name__ == "__main__":
    main()
