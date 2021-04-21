import React, { Component } from 'react'
import {Video} from './Video.js'
import Home from './Home'
import Wishlist from './Wishlist'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

class App extends Component {
	render() {
		return (
			<div>
				<Router>
					<Switch>
						<Route path="/" exact component={Home} />
						<Route path="/Wishlist" exact component={Wishlist} />
						<Route path="/:url" component={Video} />
					</Switch>
				</Router>
			</div>
		)
	}
}

export default App;