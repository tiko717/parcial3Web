import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "../app/components/Header";
import Footer from "../app/components/Footer";

import PaisesMainPage from "../paises/PaisesMainPage";

import PaisesViewPage from "../paises/PaisesViewPage";
import PaisesCreatePage from "../paises/PaisesCreatePage";

import LoginPage from "../login/LoginPage";
import LogoutPage from "../login/LogoutPage";
// import Page404 from "../other/Page404";
import LoadingScreen from "./components/Loading";

function App() {
  return (
    <>
      <LoadingScreen />
      
        <Routes>
          <Route
            path="/"
            element={wrap(<PaisesMainPage />, { header: false, footer: true })}
          />
          <Route path="/paises/create" element={wrap(<PaisesCreatePage />, { header: false, footer: true })} />
          <Route path="/paises/view/" element={wrap(<PaisesViewPage />, { header: false, footer: true })} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/logout" element={<LogoutPage />} />
          {/* <Route path="*" element={<Page404 />} /> */}
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
