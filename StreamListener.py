'''
Created on Jul 29, 2018
@author: ishank
'''

from __future__ import print_function
from __future__ import division
from ReservoirSampling import Reservoir
import tweepy

class StreamListener(tweepy.StreamListener):

    def initialize(self, socket, uid="broadcast"):
        self._sampler = Reservoir()
        self._socket =  socket
        self._uid = str(uid)
        self._switch = True
#         self.count = 5

    def get_hashtags(self, text):
        hashtags = []
        splitArray = text.split()
        for item in splitArray:
            try:
                item_dec = item.decode('utf-8')
                if item_dec[0] == '#':
                    cand = ''.join(e for e in item_dec.strip() if e.isalnum())
                    if len(cand) > 0:
                        hashtags.append(cand)
            except:
                continue
        return hashtags

    def handle_status(self, status):
        self._sampler.tweet_count += 1
        text = status.text.encode('utf-8')

        position = self._sampler.push_tweet(len(text), self.get_hashtags(text))

        return self.build_output(text, position) if position >= -1 else None

    def on_status(self, status):
        output = self.handle_status(status)
        self._socket.emit(self._uid, output)
#         self.count -=1
#         return True if self.count > 0 else False
        return self._switch

    def stop_listening(self):
        self._switch = False


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

    def build_output(self, tweet, position):
        return {
            "tweet_count": self._sampler.tweet_count,
            "top_hashtags": self._sampler.get_top_hashtags(),
            "avg_length": self._sampler.get_avg_tweet_length(),
            "tweet": {
                "position": position,
                "text": tweet
            }
        }

    def print_output(self):
        print("The number of the twitter from beginning: ", self._sampler.tweet_count)
        print("Top 5 hot hashtags: ")
        for item in self._sampler.get_top_hashtags():
            print(item[0]+": ", item[1])
        print("The average length of the twitter is: ", self._sampler.get_avg_tweet_length())
        print("\n\n")
