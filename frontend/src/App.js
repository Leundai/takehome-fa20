import React, { Component } from 'react'
import Instructions from './Instructions'
import Restaurant from './Restaurant'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      restaurants: [
        {id: 1, name: "Golden Harbor", rating: 10},
        {id: 2, name: "Potbelly", rating: 6},
        {id: 3, name: "Noodles and Company", rating: 8},
      ],
      restaurantInput: '',
      restaurantCount: 3
    }
  }

  AddRestaurant = () => {
    // We are calling it back after setState since it is asynchronous
    this.setState((prevState) => ({
      restaurantCount: prevState.restaurantCount + 1
    }), () => {
      let newRestaurant = {id: this.state.restaurantCount, name: this.state.restaurantInput, rating: 0};
      this.setState((prevState) => ({
          restaurants: [...prevState.restaurants, newRestaurant],
          restaurantInput: ''
      }));
    });
  }

  UpdateRestaurantInput = (change) => {
    this.setState({
      restaurantInput: change.target.value 
    });
  }

  render() {
    return (
      <div className="App">
        <Instructions complete={true}/>
        {this.state.restaurants.map(x => (
          <Restaurant id={x.id} name={x.name} rating={x.rating} />
        ))}

        <div>
          <input value={this.state.restaurantInput} onChange={change => this.UpdateRestaurantInput(change)}/>
          <button type="button" onClick={this.AddRestaurant}>Add Restaurant</button>
        </div>

        <div> This is the basic counter </div>
        <Counter count={0}/>
      </div>
    )
  }
}

export default App
