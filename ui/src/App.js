// Main app component. Includes routing logic
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Header from "./components/Header/Header";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Header />
            <Switch>
              {/* <Route path="/events" component={Events} /> */}
              {/* <Route path="/server-error" component={ServerError} /> */}
              {/* <Route path="/forbidden" component={Forbidden} /> */}
              {/* <Route component={NotFound} /> */}
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
