import Tweets from '../ui/Tweets'
import { connect } from 'react-redux'

const mapStateToProps = (state, props) => ({
  tweetsReservoir: state.tweetsReservoir
})

export default connect(mapStateToProps)(Tweets)
