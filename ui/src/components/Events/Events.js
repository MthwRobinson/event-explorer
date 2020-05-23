// Renders the component for the Events screen
import React, { Component } from "react";
import {
  Button,
  Form,
  FormControl,
  FormGroup,
  Row,
  Table,
} from "react-bootstrap";
import { withRouter } from "react-router-dom";
import axios from "axios";
import moment from "moment";
// import FileDownload from 'js-file-download';
import ReactTooltip from "react-tooltip";

import Loading from "./../Loading/Loading";

import "./Events.css";

const LIMIT = 25;

class Events extends Component {
  constructor(props) {
    super(props);
    this.state = {
      events: [],
      pages: 2,
      page: 1,
      count: 0,
      loading: true,
      query: "",
      searchTerms: [],
      sortColumn: "start_datetime",
      sortOrder: "desc",
      defaultEventLocation: null,
      startDate: null,
      endDate: new Date(),
      showFilter: false,
    };
  }

  componentDidMount() {}

  renderTable = () => {
    // Creates the table with event information
    let sortArrow = this.state.sortOrder === "desc" ? "down" : "up";
    const arrowClass = "fa fa-caret-" + sortArrow + " paging-arrows";

    return (
      <div>
        <Table className="table-responsive event-table">
          <thead>
            <tr>
              <th>#</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Username</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Mark</td>
              <td>Otto</td>
              <td>@mdo</td>
            </tr>
            <tr>
              <td>2</td>
              <td>Jacob</td>
              <td>Thornton</td>
              <td>@fat</td>
            </tr>
            <tr>
              <td>3</td>
              <td colSpan="2">Larry the Bird</td>
              <td>@twitter</td>
            </tr>
          </tbody>
        </Table>
      </div>
    );
  };

  renderSearch = () => {
    // Renders the search bar
    return (
      <div>
        <div className="pull-right">
          <Form onSubmit={this.handleSearch} inline>
            <FormGroup>
              <FormControl
                className="search-box"
                value={this.state.query}
                onChange={this.handleQuery}
                type="text"
              />
            </FormGroup>
            <Button
              bsStyle="primary"
              className="search-button"
              type="submit"
              data-tip="Returns searchs fesults for the event name."
            >
              Search
            </Button>
          </Form>
        </div>
      </div>
    );
  };

  renderPageCount = () => {
    // Renders the page count at the top of the table
    let leftCaret = null;
    if (this.state.page > 1) {
      leftCaret = (
        <i
          className="fa fa-caret-left paging-arrows"
          onClick={() => this.incrementPage("down")}
        ></i>
      );
    }
    let rightCaret = null;
    if (this.state.page < this.state.pages) {
      rightCaret = (
        <i
          className="fa fa-caret-right paging-arrows"
          onClick={() => this.incrementPage("up")}
        ></i>
      );
    }
    return (
      <div className="paging pull-left">
        {leftCaret}
        {this.state.page}/{this.state.pages}
        {rightCaret}{" "}
      </div>
    );
  };

  renderSearchTermPills = () => {
    // Renders the pill buttons for the active search terms
    let searchTermPills = [];
    for (let searchTerm of this.state.searchTerms) {
      searchTermPills.push(
        <div className="pull-right search-term-pill">
          <b>{searchTerm}</b>
          <i
            className="fa fa-times pull-right event-icons search-term-times"
            onClick={() => this.handleRemoveTerm(searchTerm)}
          ></i>
        </div>
      );
    }
    return searchTermPills;
  };

  render() {
    let table = this.renderTable();
    let pageCount = this.renderPageCount();
    let search = this.renderSearch();
    let searchTermPills = this.renderSearchTermPills();
    let info = "There are " + String(this.state.count) + " total events. <br/>";
    info += "Click or tap on an event for more information. <br/>";
    info += "On tablet, swipe right or left to switch pages.";
    return (
      <div>
        <div className="Events">
          <div className="events-header">
            <h2>
              Events{" "}
              <sup>
                <i className="fa fa-info-circle" data-tip={info}></i>
              </sup>
              <i
                className="fa fa-times pull-right event-icons"
                onClick={() => this.props.history.push("/")}
              ></i>
              <i
                className="fa fa-download pull-right event-icons"
                data-tip="Download the table of participants"
                onClick={() => this.downloadCSV()}
              ></i>
            </h2>
            <hr />
          </div>
          <div className="event-header">
            {pageCount}
            {search}
          </div>
          <div className="search-term-row pull-right">
            {searchTermPills.length > 0 ? (
              <span id="search-term-list">
                <b>Search Terms:</b>
              </span>
            ) : null}
            {searchTermPills}
          </div>
          {table}
        </div>
        <ReactTooltip html={true} />
      </div>
    );
  }
}

export default withRouter(Events);
