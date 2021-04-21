import React, { Component } from 'react';
import "./Wishlist.css"
import "./bootstrap.min.css"
import {Video, arr} from './Video.js'
import {newarr} from './Video.js'


console.log(newarr);

class Wishlist extends Component {
    constructor (props) {
      super(props)
      this.state = {
          url: '/Wishlist'
      }
  }
  render() {
    return (
          
                <div className="container">
                  <h3 style={{textAlign: 'center', marginTop: '50px'}}>Your Wishlist</h3>
                  <div className="list-group " style={{marginTop: '30px', alignItems: 'center', width: '300px', marginLeft: '410px'}}>
                    <a href="#" className="list-group-item list-group-item-action list-group-item-danger" >Item 1<img src="https://www.thenewsminute.com/sites/default/files/styles/slideshow_image_size/public/Myntra_Logo_1200x800.jpg?itok=QuRN2mnR"style={{maxWidth: '50px', maxHeight: '50px', marginLeft: '60%'}} /></a>
                  </div>
                </div>
    )
}
}

export default Wishlist;