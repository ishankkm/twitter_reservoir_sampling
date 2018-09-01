import React, {Component} from 'react'
import { connect } from 'react-redux';
import { setAverageLength } from '../actions'

class App extends Component {

  constructor(props) {
    super(props)
    this.createGame = this.createGame.bind(this)
    this.stopStream = this.stopStream.bind(this)
  }

  componentDidMount() {
    console.log(this.props.appState)
  }

  createGame() {
    console.log('Creating game...');
    let setAverageLength = this.props.setAverageLength
    this.props.socket.on(this.props.socket.io.engine.id, function(msg){
      if(msg.averageLength) {
        setAverageLength(Math.round( msg.averageLength))
      }
    })

    this.props.socket.emit(
      this.props.socket.io.engine.id, {streaming: true, teams: 2, topics: ['india']}
    );
  }

  stopStream() {
      console.log('Stopping...');
      this.props.socket.emit(this.props.socket.io.engine.id, {streaming: false});
  }

  render() {
    return (
      <div>App- {this.props.appState.averageLength}
        <button onClick={this.createGame}>Start Stream</button>
        <button onClick={this.stopStream}>Stop Stream</button>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    appState: state
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
      setAverageLength: (length) => dispatch(setAverageLength(length))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
