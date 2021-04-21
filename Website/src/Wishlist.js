import React, { Component } from 'react';
import "./Wishlist.css"
import Arr from './Video'

console.log(Arr.arr);

class Wishlist extends Component {
    constructor (props) {
      super(props)
      this.state = {
          url: '/Wishlist'
      }
  }
  render() {
    return (
        <div className="container2">            
            <div>
                <h1 style={{ fontSize: "45px", margin:0, padding:0 }}>V-SHOP</h1>
                <p style={{ margin:0, }}><i>..together we shop, in a Virtual-Shop!</i> </p>
            </div>
        </div>
    )
}
}

export default Wishlist;