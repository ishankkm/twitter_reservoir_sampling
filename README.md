## Twitter Reservoir Sampling

The objective of the project is to implement the concept of [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling) for a stream of data. The idea is to sample a certain amount of data from a large dataset of unknown size which cannot fit into the main memory. 

Here, the dataset is tweets from twitter corresponding to a given topic. The tweets arrive when a person tweets and the tweet contains a keyword that matches the topic that is being tracked. Since it is impossible to know the size of the dataset, reservoir sampling proves to be a good algorithm here. 

The project uses the [tweepy](http://docs.tweepy.org/en/v3.5.0/) library of python.
