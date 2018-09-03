import React from 'react'
import PropTypes from 'prop-types';
import {Tweet} from 'react-twitter-widgets'

const Tweets = ({tweetsReservoir}) => {

  return (
    <div>
      {tweetsReservoir.sort((_x, _y) => _x.index < _y.index).map((tweet) =>
          <Tweet tweetId={tweet.status_id} key={tweet.index} {...tweet}/>
      )}
    </div>
  )
}

Tweets.propTypes = {
  tweetsReservoir: PropTypes.array
}

export default Tweets