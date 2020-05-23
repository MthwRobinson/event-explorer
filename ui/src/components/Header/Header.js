import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Navbar, Nav, NavDropdown } from "react-bootstrap";

import "./Header.css";

class Header extends Component {
  render() {
    return (
      <div className="Header">
        <Navbar className="navbar-default">
          <Navbar.Brand href="#home">
            <a href="/" className="pull-left">
              <img
                src="./fiddler_logo.png"
                className="image-background"
                height="40px"
                alt=""
              />
            </a>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#link">Link</Nav.Link>
              <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  Another action
                </NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">
                  Something
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  Separated link
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>
    );
  }
}

export default withRouter(Header);
