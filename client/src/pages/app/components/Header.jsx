import React, { useEffect, useState, useMemo, useRef } from "react";
import { useAuth } from "../../../context/AuthContext";
import { Link, useLocation, useNavigate } from "react-router-dom";

import ProfileDropdown from "../../events/components/ProfileDropdown";

const Header = () => {
  const { isLogged, getUser } = useAuth();

  const { search } = useLocation();
  const query = React.useMemo(() => new URLSearchParams(search), [search]);
  const navigate = useNavigate();
  const searchInput = useRef();

  const userID = useMemo(
    () => (isLogged() ? getUser().id : null),
    [isLogged, getUser]
  );

  const userName = useMemo(
    () => (isLogged() ? getUser().name : null),
    [isLogged, getUser]
  );

  console.log("uSER ID", userID);

  const searchHandler = () =>
    searchInput.current.value.trim().length > 0 &&
    navigate(`/search?q=${searchInput.current.value.trim()}`);
  const searchKeyHandler = (e) => e.key === "Enter" && searchHandler();

  const searchButton = (
    <button className="btn btn-outline-secondary ms-2" onClick={searchHandler}>
      Buscar
    </button>
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
    () => (
      <div className="d-flex align-items-center">
        {userID && <ProfileDropdown id={userID} />}
      </div>
    ),
    [userID]
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
            La Wiki
          </Link>
          <div className="collapse navbar-collapse" id="collapseDiv">
            <div className="d-flex">
              <input
                ref={searchInput}
                onKeyDown={searchKeyHandler}
                type="search"
                defaultValue={query.get("q") ?? ""}
                name="q"
                className="form-control"
              />
              {searchButton}
            </div>
          </div>
          <div className="d-flex align-items-end">
            {isLogged() ? profileBundle : loginBtn}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;