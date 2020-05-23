// Main app component. Includes routing logic
import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// import Events from './components/Events/Events';
// import EventPage from './components/EventPage/EventPage';
// import Forbidden from './components/ErrorPages/Forbidden';
import Header from './components/Header/Header';
// import Login from './components/Login/Login';
// import Members from './components/Members/Members';
// import MemberPage from './components/MemberPage/MemberPage';
// import NotFound from './components/ErrorPages/NotFound';
// import { getModules } from './utilities/utils';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
// import '../node_modules/font-awesome/css/font-awesome.min.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Switch>
                <Route exact path="/" component={Header} />
                {/* <Route path="/events" component={Events} /> */}
                {/* <Route path="/event" component={EventPage} /> */}
                {/* <Route path="/participant" component={MemberPage} /> */}
                {/* <Route path="/participants" component={Members} /> */}
                {/* <Route path="/server-error" component={ServerError} /> */}
                {/* <Route path="/forbidden" component={Forbidden} /> */}
                {/* <Route path="/login" component={Login} /> */}
                {/* <Route component={NotFound} /> */}
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
