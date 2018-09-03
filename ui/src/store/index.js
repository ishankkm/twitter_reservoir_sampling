import appReducer from './reducers'
import { createStore, applyMiddleware} from 'redux'

const logMessages = store => next => action => {

  let result
  console.clear()
  console.groupCollapsed(`Dispatching action: ${action.type}`)
  console.log('Tweets', store.getState().tweetsReservoir.length)
  result = next(action)

  console.log(store.getState())
  console.groupEnd()

  return result
}

export default (initialState={}) => {
  return applyMiddleware(logMessages)(createStore)(appReducer, initialState)
}
