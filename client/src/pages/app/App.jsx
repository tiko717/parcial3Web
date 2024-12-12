import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "../app/components/Header";
import Footer from "../app/components/Footer";

import EventsMainPage from "../events/EventsMainPage";

import EventViewPage from "../events/EventViewPage";
import EventCreatePage from "../events/EventCreatePage";
import EventEditPage from "../events/EventEditPage";

// import LoginPage from "../login/LoginPage";
// import LogoutPage from "../login/LogoutPage";
// import Page404 from "../other/Page404";
import LoadingScreen from "./components/Loading";

function App() {
  return (
    <>
      <LoadingScreen />
      
        <Routes>
          <Route
            path="/"
            element={wrap(<EventsMainPage />, { header: false, footer: true })}
          />
          <Route path="/events/create" element={wrap(<EventCreatePage />)} />
          <Route path="/events/:id" element={wrap(<EventViewPage />)} />
          <Route path="/events/:id/edit" element={wrap(<EventEditPage />)} />
          {/* <Route path="/login" element={<LoginPage />} />
          <Route path="/logout" element={<LogoutPage />} />
          <Route path="*" element={<Page404 />} /> */}
        </Routes>      
    </>
  );
}

const wrap = (child, options = { header: false, footer: true }) => (
  <div className="app-container">
    {options.header ? <Header /> : null}
    <div className="content">{child}</div>
    {options.footer ? <Footer /> : null}
  </div>
);

export default App;
