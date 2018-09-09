import React from 'react'
import PropTypes from 'prop-types';
import {Tweet} from 'react-twitter-widgets'
import './Tweets.css'

const Tweets = ({tweetsReservoir}) => {

  return (
    <div className="container">
      <div className="card-columns">
          {tweetsReservoir.map((tweet) =>
            <div className="card border-0" key={tweet.index} >
              <Tweet tweetId={tweet.status_id} {...tweet}/>
            </div>
          )}
      </div>
    </div>
  )
}

Tweets.propTypes = {
  tweetsReservoir: PropTypes.array
}

export default Tweets
