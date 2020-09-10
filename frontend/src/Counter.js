import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
      super(props);
      this.state = {
          count: props.count
      };
  }
  
  handleIncrement = () => {
    this.setState((prevState) => ({count: prevState.count + 1}));
  }

  handleDecrement = () => {
    if (this.state.count === 0) {
      return;
    }
    this.setState((prevState) => ({count: prevState.count - 1}));
  }

  render() {
    return (
      <div>
        {this.state.count}
        <div>
        <button onClick={this.handleIncrement}>+</button>
        <button onClick={this.handleDecrement}>-</button>
        </div>
      </div> 
    )
  }
}

export default Counter
