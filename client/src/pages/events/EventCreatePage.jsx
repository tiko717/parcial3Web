import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAPI } from "../../context/APIContext";

const EventCreatePage = () => {
  const { eventos, media } = useAPI();
  const navigate = useNavigate();
  const [nombre, setNombre] = useState("");
  const [timestamp, setTimestamp] = useState("");
  const [lugar, setLugar] = useState("");
  const [imagen, setImagen] = useState(null);
  const [imagenURL, setImagenURL] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await media.create(formData);
      if (response.status >= 200 && response.status < 300) {
        setImagenURL(response.data.result.url);
      } else {
        setError("Error al subir la imagen");
      }
    } catch (error) {
      setError("Error al subir la imagen");
    }
  };

  const handleCreateEvent = async () => {
    setLoading(true);
    setError(null);

    try {
      // Obtener lat y lon de OpenStreetMap
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${lugar}`
      );
      const data = await response.json();

      if (data && data.length > 0) {
        const { lat, lon } = data[0];

        const newEvent = {
          nombre,
          timestamp,
          lugar,
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          organizador: "user",
          imagen: imagenURL,
        };

        const eventResponse = await eventos.create(newEvent);
        if (eventResponse.status >= 200 && eventResponse.status < 300) {
          navigate("/"); // Redirige a la página principal
        } else {
          setError("Error al crear el evento");
        }
      } else {
        setError("Dirección no encontrada");
      }
    } catch (error) {
      setError("Error al crear el evento");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Crear Evento</h1>
      <div className="mb-3">
        <label className="form-label">Nombre</label>
        <input
          type="text"
          className="form-control"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Fecha y Hora</label>
        <input
          type="text"
          className="form-control"
          placeholder="dd/mm/aa hh:mm"
          value={timestamp}
          onChange={(e) => setTimestamp(e.target.value)}
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Lugar</label>
        <input
          type="text"
          className="form-control"
          value={lugar}
          onChange={(e) => setLugar(e.target.value)}
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Imagen del Evento</label>
        <input
          type="file"
          className="form-control"
          onChange={(e) => {
            setImagen(e.target.files[0]);
            handleImageUpload(e.target.files[0]);
          }}
        />
        {imagenURL && (
          <img
            src={imagenURL}
            alt="Previsualización Imagen del Evento"
            className="img-thumbnail mt-3"
            style={{ maxHeight: "200px" }}
          />
        )}
      </div>
      {error && <div className="text-danger mb-3">{error}</div>}
      <button className="btn btn-primary" onClick={handleCreateEvent} disabled={loading}>
        {loading ? "Creando..." : "Crear Evento"}
      </button>
    </div>
  );
};

export default EventCreatePage;