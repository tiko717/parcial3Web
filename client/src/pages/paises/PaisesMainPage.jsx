import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const PaisesMainPage = () => {
  const { isLogged, login, getUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isLogged()) {
      navigate("/paises/view");
    }
  }, [isLogged, navigate]);

  const handleLogin = async () => {
    await login("google");
    if (isLogged()) {
      navigate("/paises/view");
    }
  };

  return (
    <div className="container py-5">
      <h1 className="text-center mb-4">MiMapa</h1>
      {!isLogged() && (
        <div className="text-center">
          <button className="btn btn-primary" onClick={handleLogin}>
            Iniciar Sesión
          </button>
        </div>
      )}
    </div>
  );
};

export default PaisesMainPage;
