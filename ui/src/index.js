import React from 'react'
import {render} from 'react-dom'
import sampleData from './initialState'
import storeFactory from './store'
import { Provider } from 'react-redux'
import App from './components'
import io from 'socket.io-client'

const initialState = (localStorage["redux-store"]) ?
    JSON.parse(localStorage["redux-store"]) :
    sampleData

const saveState = () =>
    localStorage["redux-store"] = JSON.stringify(store.getState())

const store = storeFactory(initialState)
store.subscribe(saveState)

window.react = React
window.store = store

var socket = io.connect(`http://${document.domain}:5000`);

socket.on('connect', function() {
    console.log('Websocket connected!');
});


render(
  <Provider store={store}>
    <App socket={socket}/>
  </Provider>,
  document.getElementById('root')
)
