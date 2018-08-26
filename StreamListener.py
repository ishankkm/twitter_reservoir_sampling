'''
Created on Jul 29, 2018
@author: ishank
'''

from __future__ import print_function
from __future__ import division
from ReservoirSampling import Reservoir
import tweepy

class StreamListener(tweepy.StreamListener):
    
    def initialize(self):
        self._sampler = Reservoir()   
            
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
         
    def on_status(self, status):        
        self._sampler.tweet_count += 1
        text = status.text.encode('utf-8')
        hashtags = self.get_hashtags(text)
        len_tweet = len(text)
                
        if self._sampler.push_tweet(len_tweet, hashtags):
            self.print_output()
            
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
    def print_output(self):
        print("The number of the twitter from beginning: ", self._sampler.tweet_count)
        print("Top 5 hot hashtags: ")
        for item in self._sampler.get_top_hashtags():
            print(item[0]+": ", item[1])
        print("The average length of the twitter is: ", self._sampler.get_avg_tweet_length())
        print("\n\n")
