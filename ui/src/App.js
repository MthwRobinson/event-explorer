// Main app component. Includes routing logic
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Events from "./components/Events/Events";
import Forbidden from "./components/ErrorPages/Forbidden";
import Header from "./components/Header/Header";
import NotFound from "./components/ErrorPages/NotFound";
import ServerError from "./components/ErrorPages/ServerError";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/font-awesome/css/font-awesome.min.css";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Header />
            <Switch>
              <Route path="/" component={Events} />
              <Route path="/server-error" component={ServerError} />
              <Route path="/forbidden" component={Forbidden} />
              <Route component={NotFound} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
