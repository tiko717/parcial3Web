import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useAPI } from "../../context/APIContext";
import { useData } from "../../context/DataContext";
import { Icon } from "leaflet";
import 'leaflet/dist/leaflet.css';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const EventViewPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { eventos } = useAPI();
  const { getActualEvent, setActualEvent } = useData();
  const [event, setEvent] = useState(getActualEvent());
  const [loading, setLoading] = useState(!event);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await eventos.getById(id);
        if (response.status >= 200 && response.status < 300) {
          setEvent(response.data);
          setActualEvent(response.data);
        } else {
          setError("Error al obtener el evento");
        }
      } catch (error) {
        setError("Error al obtener el evento");
      } finally {
        setLoading(false);
      }
    };

    if (!event) {
      fetchEvent();
    }
  }, [id, event, eventos, setActualEvent]);

  const handleDeleteEvent = async () => {
    try {
      const response = await eventos.delete(id);
      if (response.status >= 200 && response.status < 300) {
        navigate("/"); // Redirigir a la lista de eventos
      } else {
        setError("Error al eliminar el evento");
      }
    } catch (error) {
      setError("Error al eliminar el evento");
    } finally {
      setShowModal(false); // Cerrar el modal
    }
  };

  const handleEditEvent = () => {
    navigate(`/events/${id}/edit`);
  };

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>{error}</div>;

  const eventIcon = new Icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  return (
    <div className="container py-5">
      <button className="btn btn-secondary mb-3" onClick={() => navigate(-1)}>Volver</button>
      <div className="card mb-4 shadow-sm">
        <div className="card-body">
          <h1 className="card-title mb-4">{event.nombre}</h1>
          <div className="mb-3">
            <button className="btn btn-primary me-2" onClick={handleEditEvent}>Editar</button>
            <button className="btn btn-danger" onClick={() => setShowModal(true)}>Eliminar</button>
          </div>
          <p className="card-text"><strong>Fecha y Hora:</strong> {new Date(event.timestamp).toLocaleString()}</p>
          <p className="card-text"><strong>Lugar:</strong> {event.lugar}</p>
          <p className="card-text"><strong>Latitud:</strong> {event.lat}</p>
          <p className="card-text"><strong>Longitud:</strong> {event.lon}</p>
          <p className="card-text"><strong>Organizador:</strong> {event.organizador}</p>
          <div className="mb-4">
            <img src={event.imagen || "https://via.placeholder.com/400x250"} alt={event.nombre} className="img-fluid" />
          </div>
          <div className="mb-4">
            <MapContainer center={[event.lat, event.lon]} zoom={13} style={{ height: "400px", width: "100%" }}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <Marker position={[event.lat, event.lon]} icon={eventIcon}>
                <Popup>{event.nombre}</Popup>
              </Marker>
            </MapContainer>
          </div>          
        </div>
      </div>

      {/* Modal de confirmación para eliminar el evento */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirmar eliminación</Modal.Title>
        </Modal.Header>
        <Modal.Body>¿Estás seguro de que deseas eliminar este evento?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancelar
          </Button>
          <Button variant="danger" onClick={handleDeleteEvent}>
            Eliminar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default EventViewPage;
