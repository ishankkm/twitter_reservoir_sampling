'''
Created on Jul 29, 2018
@author: ishank
'''

from __future__ import print_function
from __future__ import division
import random

RESERVOIR_SIZE = 10
NUM_TOP_TWEETS = 5

class Reservoir():
    
    def __init__(self):
        self._reservoir = []        # stores tuples (len_tweet, hashtags) for each tweet
        self._hashtags_count = {}   # Each hashtag's count
        self.tweet_count = 0       # Total tweets since start 
        self._sum_tweet_length = 0  # To calculate the average 
    
    # decide whether to keep the tweet or discard it
    def get_add_decision(self):
        
        if self.tweet_count <= RESERVOIR_SIZE:
            return True
        
        thresold_prob = RESERVOIR_SIZE / self.tweet_count
        rand_prob = random.random()
        
        if thresold_prob >= rand_prob:
            return True
        
        return False
    
    # update counts when a tweet is added
    def update_hashtags_dict(self, hashtags):
        for hashtag in hashtags:
            self._hashtags_count[hashtag] = self._hashtags_count.get(hashtag, 0) + 1
    
    # adjust counts if tweet is removed from the reservoir
    def reduce_hashtags_count(self, hashtags):
        for hashtag in hashtags:
            self._hashtags_count[hashtag] -= 1
            if self._hashtags_count[hashtag] == 0:
                del self._hashtags_count[hashtag]
    
    # process each tweet
    def push_tweet(self, len_tweet, hashtags):
        
        if not self.get_add_decision():
            return -1
        
        # For the initial tweets simply add to reservoir
        if len(self._reservoir) < RESERVOIR_SIZE:
            self._reservoir.append(tuple(( len_tweet, hashtags )))
            self.update_hashtags_dict(hashtags)
            self._sum_tweet_length += len_tweet
            return len(self._reservoir) - 1
        
        position = random.randint(0, RESERVOIR_SIZE-1)
        
        self.update_hashtags_dict(hashtags)
        self._sum_tweet_length += len_tweet
        
        self.reduce_hashtags_count(self._reservoir[position][1])
        self._sum_tweet_length -= self._reservoir[position][0]
        
        self._reservoir[position] = tuple(( len_tweet, hashtags ))
        return position
        
    def get_avg_tweet_length(self):
        return self._sum_tweet_length / len(self._reservoir)
    
    def get_top_hashtags(self):
        sorted_dict = sorted(self._hashtags_count.items(), key=lambda x: x[1])
        return sorted_dict[::-1][:NUM_TOP_TWEETS]
        
