import React from 'react'
//import {render} from 'react-dom'
import sampleData from './initialState'
import storeFactory from './store'

const initialState = (localStorage["redux-store"]) ?
    JSON.parse(localStorage["redux-store"]) :
    sampleData

const saveState = () =>
    localStorage["redux-store"] = JSON.stringify(store.getState())

const store = storeFactory(initialState)
store.subscribe(saveState)

window.react = React
window.store = store
