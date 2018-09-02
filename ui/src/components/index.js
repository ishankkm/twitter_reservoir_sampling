import React from 'react'
import { connect } from 'react-redux';
import Tweets from './containers/Tweets'
import { setAverageLength, setTopHashtags, addTweet, cancelFetching, fetchTweets } from '../actions'

const App = ({socket,
              setAverageLength,
              setTopHashtags,
              addTweet,
              fetchTweets,
              cancelFetching,
              appState}) => {

  const startStream = () => {
    console.log('Creating game...');
    fetchTweets()

    socket.on(socket.io.engine.id, function({topHashTags, averageLength, tweet}){

      if(averageLength) {
        setAverageLength(Math.round(averageLength))
      }

      if(topHashTags) {
        if(topHashTags.length){
          setTopHashtags(topHashTags.map(x => x[0]))
        }
      }

      if(tweet) {
        addTweet(tweet)
      }
    })

    socket.emit(
      socket.io.engine.id, {streaming: true, topics: ['green']}
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
      cancelFetching: () => dispatch(cancelFetching())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
