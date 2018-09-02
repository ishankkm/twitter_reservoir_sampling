import C from '../constants'
import {combineReducers} from 'redux'

const keywords = (state=[], action) =>
  (action.type === C.SET_KEYWORDS) ?
    action.payload :
    state

const reservoirSize = (state=100, action) =>
  (action.type === C.SET_RESERVOIR_SIZE) ?
    action.payload :
    state

const tweet = (state=null, action) =>
  (action.type === C.ADD_TWEET) ?
    action.payload :
    state

const tweetsReservoir = (state=[], action) => {
  switch (action.type) {
    case C.ADD_TWEET:
      return [
        ...state.filter(t => t.index !== action.payload.index),
        tweet(null, action)
      ]
    case C.CLEAR_RESERVOIR:
      return []
    default:
      return state
  }
}

const averageLength = (state=0, action) =>
  (action.type === C.SET_AVG_LENGTH) ?
    action.payload :
    state

const topHashTags = (state=[], action) =>
  (action.type === C.SET_TOP_HASHTAGS) ?
    action.payload :
    state

const fetchingTweets = (state=false, action) =>
  (action.type === C.FETCH_TWEETS) ?
    true :
    (action.type === C.CANCEL_FETCHING) ?
      false :
      state

const appErrors = (state=[], action) => {
  switch (action.type) {
    case C.ADD_ERROR:
        return [
            ...state,
            action.payload
        ]
    case C.CLEAR_ERROR:
      return state.filter((_m, i) => i !== action.payload)
    default:
        return state
  }
}

export default combineReducers({
  keywords,
  reservoirSize,
  tweetsReservoir,
  averageLength,
  topHashTags,
  fetchingTweets,
  appErrors
})
