import C from './constants'

export const setKeywords = keywords => ({
  type: C.SET_KEYWORDS,
  payload: keywords
})

export const setReservoirSize = size => ({
  type: C.SET_RESERVOIR_SIZE,
  payload: size
})

export const setTweetCount = count => ({
  type: C.SET_TWEET_COUNT,
  payload: count
})

export const addTweet = tweet => ({
  type: C.ADD_TWEET,
  payload: tweet
})

export const clearReservoir = () => ({
  type: C.CLEAR_RESERVOIR,
  payload: null
})

export const setAverageLength = length => ({
  type: C.SET_AVG_LENGTH,
  payload: length
})

export const setTopHashtags = hashtags => ({
  type: C.SET_TOP_HASHTAGS,
  payload: hashtags
})

export const fetchTweets = () => ({
  type: C.FETCH_TWEETS,
  payload: null
})

export const cancelFetching = () => ({
  type: C.CANCEL_FETCHING,
  payload: null
})

export const addError = error => ({
  type: C.ADD_ERROR,
  payload: error
})

export const clearError = position => ({
  type: C.CLEAR_ERROR,
  payload: position
})
