import React from 'react'
import { connect } from 'react-redux';
import Tweets from './containers/Tweets'
import {  setAverageLength,
          setTopHashtags,
          addTweet,
          fetchTweets,
          cancelFetching,
          setReservoirSize,
          setKeywords,
          setTweetCount,
          clearReservoir,
          clearError,
          addError } from '../actions/actions'

const App = ({socket,
              setAverageLength,
              setTopHashtags,
              addTweet,
              fetchTweets,
              cancelFetching,
              setReservoirSize,
              setKeywords,
              setTweetCount,
              clearReservoir,
              clearError,
              addError,
              appState }) => {

  const changeReservoirSize = (size=10) => {
    setReservoirSize(size)
  }

  const updateTweetCount = (count=10) => {
    setTweetCount(count)
  }

  const changeKeywords = (keywords=[]) => {
    setKeywords(keywords)
  }

  const resetReservoir = () => {
    clearReservoir()
  }

  const logError = (error={}) => {
    addError(error)
  }

  const removeError = (position=0) => {
    clearError(position)
  }

  const startStream = () => {
    console.log('Creating game...');
    fetchTweets()

    socket.on(socket.io.engine.id, function({topHashTags, averageLength, tweet, tweet_count}){

      if(averageLength)  setAverageLength(Math.round(averageLength))
      if(tweet) addTweet(tweet)
      if(tweet_count) updateTweetCount(tweet_count)

      if(topHashTags) {
        if(topHashTags.length){
          setTopHashtags(topHashTags.map(x => x[0]))
        }
      }
    })

    changeReservoirSize(10)
    changeKeywords(['green'])
    resetReservoir()
    removeError(0)
    logError({'type': 'something'})

    socket.emit(
      socket.io.engine.id, {
        streaming: true,
        topics: appState.keywords,
        reservoirSize: appState.reservoirSize
      }
    );
  }

  const stopStream = () => {
      console.log('Stopping...');
      cancelFetching()
      socket.emit(socket.io.engine.id, {streaming: false});
  }

  return (
    <div>
      <p>Average Length- {appState.averageLength}</p>
      <ul>
        Top Hashtags-
        <p>{appState.topHashTags.map((_t, i) => <li key={i}>{_t}</li> )}</p>
      </ul>
      <button onClick={startStream}>Start Stream</button>
      <button onClick={stopStream}>Stop Stream</button>
      <Tweets tweetsReservoir={appState.tweetsReservoir}/>
    </div>
  )
}

const mapStateToProps = (state) => {
  return {
    appState: state
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
      setAverageLength: (length) => dispatch(setAverageLength(length)),
      setTopHashtags: (topHashTags) => dispatch(setTopHashtags(topHashTags)),
      addTweet: (tweet) => dispatch(addTweet(tweet)),
      fetchTweets: () => dispatch(fetchTweets()),
      cancelFetching: () => dispatch(cancelFetching()),
      setReservoirSize: (size) =>  dispatch(setReservoirSize(size)),
      setKeywords: (keywords) =>  dispatch(setKeywords(keywords)),
      clearReservoir: () => dispatch(clearReservoir()),
      clearError: (position) => dispatch(clearError(position)),
      addError: (error) => dispatch(addError(error)),
      setTweetCount: (count) => dispatch(setTweetCount(count))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
