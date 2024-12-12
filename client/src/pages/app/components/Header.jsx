import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header>
      <nav className="navbar navbar-expand-lg bg-light py-3">
        <div className="container-fluid">
          <Link to="/" className="navbar-brand">
            Eventual
          </Link>
          <div className="d-flex">
            <Link to="/login" className="btn btn-primary">
              Iniciar Sesión
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
