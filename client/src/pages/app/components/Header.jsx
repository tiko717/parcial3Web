import React, { useEffect, useState, useMemo, useRef } from "react";
import { useAuth } from "../../../context/AuthContext";
import { Link, useLocation, useNavigate } from "react-router-dom";
import ProfileDropdown from "../../events/components/ProfileDropdown";

const Header = () => {
  const { isLogged, getUser } = useAuth();

  const userID = useMemo(
    () => (isLogged() ? getUser().id : null),
    [isLogged, getUser]
  );

  const loginBtn = useMemo(
    () => (
      <Link to={"/login"} style={{ textDecoration: "none", color: "gray" }}>
        Iniciar Sesión
      </Link>
    ),
    []
  );

  const profileBundle = useMemo(
    () => userID && <ProfileDropdown id={userID} />, [userID]
  );

  return (
    <header>
      <nav className="navbar navbar-expand-lg bg-secondary-subtle py-3 shadow-sm">
        <div className="container-fluid">
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseDiv"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <Link to={"/"} className="navbar-brand">
            Eventual
          </Link>
          <div className="d-flex align-items-end">
            {isLogged() ? profileBundle : loginBtn}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
