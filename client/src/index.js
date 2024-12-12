import React from "react";
import ReactDOM from "react-dom";

import 'bootstrap/dist/css/bootstrap.min.css';
import "leaflet/dist/leaflet.css";
import App from "./pages/app/App";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { APIProvider } from "./context/APIContext";
import { DataProvider } from "./context/DataContext";


ReactDOM.render(
      <Router>
          <APIProvider>
              <DataProvider>
                  <App />
              </DataProvider>
          </APIProvider>
      </Router>,
  document.getElementById('root')
);