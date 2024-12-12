import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAPI } from "../../context/APIContext";
import { useData } from "../../context/DataContext";

const EventEditPage = () => {
  const { eventos, media } = useAPI();
  const { getActualEvent, setActualEvent } = useData();
  const navigate = useNavigate();
  const [event, setEvent] = useState(getActualEvent());
  const [nombre, setNombre] = useState(event?.nombre || "");
  const [timestamp, setTimestamp] = useState("");
  const [lugar, setLugar] = useState(event?.lugar || "");
  const [imagen, setImagen] = useState(null);
  const [imagenURL, setImagenURL] = useState(event?.imagen || "");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Función para convertir el timestamp al formato "dd/mm/aaaa hh:mm"
  const formatDateToInput = (timestamp) => {
    const date = new Date(timestamp);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${day}/${month}/${year} ${hours}:${minutes}`;
  };

  // Función para convertir el formato "dd/mm/yyyy hh:mm" al requerido para el backend
  const parseInputToTimestamp = (input) => {
    // En este caso, el input ya está en formato "dd/mm/yyyy hh:mm"
    return input; // Devolver directamente el valor tal cual
  };

  // Al cargar, convertir el timestamp inicial al formato deseado
  useEffect(() => {
    if (event?.timestamp) {
      setTimestamp(formatDateToInput(event.timestamp));
    }
  }, [event]);

  useEffect(() => {
    if (!event) {
      navigate("/"); // Redirige a la página principal si no hay evento seleccionado
    }
  }, [event, navigate]);

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

  const handleUpdateEvent = async () => {
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

        const updatedEvent = {
          ...event,
          nombre,
          timestamp: parseInputToTimestamp(timestamp), // Convertir al formato requerido
          lugar,
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          imagen: imagenURL,
        };

        const eventResponse = await eventos.update(event._id, updatedEvent);
        if (eventResponse.status >= 200 && eventResponse.status < 300) {
          setActualEvent(updatedEvent);
          navigate("/"); // Redirige a la página principal
        } else {
          setError("Error al actualizar el evento");
        }
      } else {
        setError("Dirección no encontrada");
      }
    } catch (error) {
      setError("Error al actualizar el evento");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Editar Evento</h1>
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
          placeholder="dd/mm/aaaa hh:mm"
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
      <button className="btn btn-primary" onClick={handleUpdateEvent} disabled={loading}>
        {loading ? "Actualizando..." : "Actualizar Evento"}
      </button>
    </div>
  );
};

export default EventEditPage;
