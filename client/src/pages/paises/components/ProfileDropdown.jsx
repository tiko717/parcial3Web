import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { useAPI } from "../../../context/APIContext";
const ProfileDropdown = ({ id }) => {
  const { users } = useAPI();
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await users.getById(id);
        if (response.status >= 200 && response.status < 300) {
          setUserData(response.data);
        } else {
          console.error(
            "Error al cargar los datos del usuario:",
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error al cargar los datos del usuario:", error);
      }
    };

    if (id) {
      fetchUserData();
    }
  }, [id]);

  if (!userData) {
    return null; // Podrías mostrar un loader aquí mientras se carga la información
  }

  return (
    <div className="dropdown ms-2">
      <button
        className="btn btn-secondary dropdown-toggle"
        type="button"
        id="profileDropdown"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <img
          src={userData.profilePicture}
          alt="Profile"
          className="rounded-circle me-2"
          style={{ width: "32px", height: "32px", objectFit: "cover" }}
        />
        {userData.name}
      </button>
      <ul className="dropdown-menu" aria-labelledby="profileDropdown">
        <li>
          <Link className="dropdown-item" to={`/profile/${id}`}>
            Ver Perfil
          </Link>
        </li>
        <li>
          <Link className="dropdown-item" to="/">
            Mis wikis
          </Link>
        </li>
        <li>
          <hr className="dropdown-divider" />
        </li>
        <li>
          <Link className="dropdown-item text-danger" to="/logout">
            Cerrar Sesión
          </Link>
        </li>
      </ul>
    </div>
  );
};

ProfileDropdown.propTypes = {
  id: PropTypes.string.isRequired, // El ID del usuario es obligatorio
};

export default ProfileDropdown;
