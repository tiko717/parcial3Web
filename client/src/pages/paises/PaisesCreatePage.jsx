import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAPI } from "../../context/APIContext";
import { useAuth } from "../../context/AuthContext"; // Importa el contexto de autenticación

const PaisesCreatePage = () => {
  const { paises, media } = useAPI();
  const { getUser } = useAuth(); // Obtén la función getUser del contexto de autenticación
  const navigate = useNavigate();
  const [nombre, setNombre] = useState("");  // Nombre del país
  const [imagen, setImagen] = useState(null);  // Imagen del país
  const [imagenURL, setImagenURL] = useState("");  // URL de la imagen subida
  const [error, setError] = useState(null);  // Estado de error
  const [loading, setLoading] = useState(false);  // Estado de carga

  // Función para subir la imagen a Cloudinary
  const handleImageUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "your_preset_name");  // Usa tu preset de Cloudinary

    try {
      const response = await media.create(formData);
      if (response.status >= 200 && response.status < 300) {
        setImagenURL(response.data.result.url);  // Establece la URL de la imagen
      } else {
        setError("Error al subir la imagen");
      }
    } catch (error) {
      setError("Error al subir la imagen");
    }
  };

  // Función para crear un nuevo país
  const handleCreateCountry = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Obtener las coordenadas del país usando OpenStreetMap
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${nombre}`
      );
      const data = await response.json();

      if (data && data.length > 0) {
        const { lat, lon } = data[0];  // Obtener latitud y longitud

        // Verificar si el usuario está logueado y obtener su email
        const usuarioLogueado = getUser(); // Obtener el usuario logueado
        const email = usuarioLogueado ? usuarioLogueado.email : "user"; // Si está logueado, usar su email, sino "user"

        const newCountry = {
          nombre,
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          email,  // Asociar el país con el email del usuario
          imagen: imagenURL,  // Imagen del país
        };

        const countryResponse = await paises.create(newCountry); // Llamada a la API para crear el país
        if (countryResponse.status >= 200 && countryResponse.status < 300) {
          navigate("/paises/view");  // Redirigir a la página de países visitados
        } else {
          setError("Error al crear el país");
        }
      } else {
        setError("País no encontrado");
      }
    } catch (error) {
      setError("Error al crear el país");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <h1>Crear País Visitado</h1>

      <form onSubmit={handleCreateCountry}>
        <div className="mb-3">
          <label className="form-label">Nombre del País</label>
          <input
            type="text"
            className="form-control"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Imagen del País</label>
          <input
            type="file"
            className="form-control"
            onChange={(e) => {
              setImagen(e.target.files[0]);
              handleImageUpload(e.target.files[0]);  // Subir la imagen
            }}
          />
          {imagenURL && (
            <img
              src={imagenURL}
              alt="Previsualización de la Imagen del País"
              className="img-thumbnail mt-3"
              style={{ maxHeight: "200px" }}
            />
          )}
        </div>

        {error && <div className="text-danger mb-3">{error}</div>}

        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? "Creando..." : "Crear País Visitado"}
        </button>
      </form>
    </div>
  );
};

export default PaisesCreatePage;
