import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const LoginPage = () => {
  const navigate = useNavigate();
  const { login, logout, isLogged, getUser } = useAuth();

  const handleLogin = async (provider) => {
    try {
      await login(provider);
      navigate(-1);
    } catch (error) {
      console.error(`Error during ${provider} login:`, error);
    }
  };

  const handleBack = () => {
    navigate(-1);
  };

  return (
    <div className="container-flex vh-100 align-content-center">
      <div
        className="card shadow-lg rounded overflow-hidden mx-lg-auto mx-3"
        style={{ maxWidth: "1020px" }}
      >
        <div className="row g-0">
          <div className="col-12">
            <button
              onClick={handleBack}
              className="btn btn-primary my-3"
              style={{
                position: "absolute",
                top: "10px",
                left: "20px",
                zIndex: 10,
              }}
            >
              Volver
            </button>
          </div>
          <div className="col-lg-4 col-12">
            <img
              src="https://images.pexels.com/photos/2033997/pexels-photo-2033997.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"
              className="img-fluid"
              alt="Login Illustration"
              style={{
                objectFit: "cover",
                width: "100%",
                height: "auto",
                maxHeight: "300px",
              }}
            />
          </div>
          <div className="col-12 col-lg-8">
            <div className="card-body d-flex flex-column justify-content-center">
              <h5 className="card-title mb-3">Iniciar sesión</h5>
              <p className="card-text text-muted mb-4">
                Comparte tus pensamientos con el mundo entero desde hoy.
              </p>
              <div className="d-flex flex-column">
                <p className="text-muted mb-2">Continuar con...</p>
                {isLogged() ? (
                  <div>
                    <p>Bienvenido, {getUser().email}</p>
                    <button
                      onClick={logout}
                      className="btn btn-outline-secondary w-100"
                    >
                      Salir
                    </button>
                  </div>
                ) : (
                  <div className="d-flex flex-column align-items-center">
                    <button
                      onClick={() => handleLogin("google")}
                      className="btn btn-outline-danger d-flex flex-column align-items-center justify-content-center w-100"
                    >
                      <span className="bi bi-google mb-2"></span>
                      Google
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
