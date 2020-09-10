import React, { Component } from 'react'
import Counter from './Counter'

class App extends Component {
  // YOUR CODE GOES BELOW
  render() {
    return (
      <div>
        <h3>{this.props.id}. {this.props.name}</h3>
        <Counter count={this.props.rating}/>
      </div>
    )
  }
}

export default App
