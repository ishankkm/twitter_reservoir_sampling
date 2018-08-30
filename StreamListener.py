'''
Created on Jul 29, 2018
@author: ishank
'''

from __future__ import print_function
from __future__ import division
from ReservoirSampling import Reservoir
import tweepy, json

class StreamListener(tweepy.StreamListener):
        
    def initialize(self, socket, emit_at="broadcast"):
        self._sampler = Reservoir()
        self._socket =  socket
        self._emit_at = str(emit_at)
        self._switch = True
#         self.count = 5
            
    def get_hashtags_from_text(self, text):
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
    
    def get_hashtags(self, status):                
        return [hs['text'] for hs in status.entities['hashtags']]
        
    
    def handle_status(self, status):
        self._sampler.tweet_count += 1
        text = status.text.encode('utf-8')
        position = self._sampler.push_tweet(len(text), self.get_hashtags(status))
        
        return self.build_output(status, position) if position >= -1 else None
         
    def on_status(self, status):        
        output = self.handle_status(status)
        self._socket.emit(self._emit_at, output)
        return self._switch
        
    def stop_listening(self):
        self._switch = False
                
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
    def build_output(self, status, position):
        return {
            "tweet_count": self._sampler.tweet_count,
            "topHashTags": self._sampler.get_top_hashtags(),
            "averageLength": self._sampler.get_avg_tweet_length(),
            "tweet": {
                "index": position,
                "status_id": status.id,
                "user_id": status.user.id
            }
        }        

    def print_output(self):
        print("The number of the twitter from beginning: ", self._sampler.tweet_count)
        print("Top 5 hot hashtags: ")
        for item in self._sampler.get_top_hashtags():
            print(item[0]+": ", item[1])
        print("The average length of the twitter is: ", self._sampler.get_avg_tweet_length())
        print("\n\n")
