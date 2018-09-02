import React, { Component } from 'react'
import fetch from 'isomorphic-fetch'

class Tweet extends Component {

  componentWillMount() {
    let {status_id, user_id} = this.props
    let url = 'https://publish.twitter.com/oembed?url=https://twitter.com/'
    console.log(`${url + user_id}/status/${status_id}`)
    fetch(`${url + user_id}/status/${status_id}`, {
      method: "GET",
      mode: "cors",
      headers:{
      'Access-Control-Allow-Origin':'*'
      }
    })
      .then(response => response.json())
      .then(response => {
        console.log(response)
        this.props.html = response.html
      })
      .catch(error => {
        console.log(error.message)
      })
  }

  render() {
    return (
      <div>
        {this.props.html}
      </div>
    )
  }

}

export default Tweet
