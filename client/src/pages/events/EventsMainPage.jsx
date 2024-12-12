import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle } from "react-leaflet";
import { useAPI } from "../../context/APIContext";
import { Icon } from "leaflet";
import EventList from "./components/EventList";
import 'leaflet/dist/leaflet.css'; // Asegúrate de importar el CSS de Leaflet

const EventsMainPage = () => {
  const { eventos } = useAPI();
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [address, setAddress] = useState(""); // Dirección introducida
  const [mapCenter, setMapCenter] = useState([51.505, -0.09]); // Posición inicial del mapa
  const [latLon, setLatLon] = useState(null); // Coordenadas de la ubicación encontrada
  const [radius, setRadius] = useState(0.2); // Radio de búsqueda
  const METROS_POR_GRADO = 111000; // Aproximación de metros por grado de latitud/longitud

  // Icono personalizado para las chinchetas
  const eventIcon = new Icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  // Función para buscar eventos cercanos
  const handleSearch = async () => {
    if (!address) return;

    setLoading(true);
    setError(null);
    setLatLon(null); // Reiniciar coordenadas

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${address}`
      );
      const data = await response.json();

      if (data && data.length > 0) {
        const { lat, lon } = data[0];
        setLatLon({ lat, lon });
        setMapCenter([lat, lon]);
        setRadius(0.2);

        const eventResponse = await eventos.getNearby(lat, lon, `&sort=timestamp`);
        if (eventResponse.status >= 200 && eventResponse.status < 300) {
          setEvents(eventResponse.data);
        } else {
          setError("Error al obtener los eventos");
        }
      } else {
        setError("Dirección no encontrada");
      }
    } catch (error) {
      setError("Error al obtener la localización o los eventos");
    } finally {
      setLoading(false);
    }
  };

  const MapCenter = () => {
    const map = useMap();
    map.setView(mapCenter, map.getZoom());
    return null;
  };

  // Función para manejar la creación de un nuevo evento
  const handleCreateEvent = () => {
    navigate("/events/create");
  };

  return (
    <div className="container py-5">
      <h1 className="text-center mb-4">Página principal de eventos</h1>
      <div className="mb-4">
        <h3>Crear evento</h3>
        {/* Botón Crear Evento */}
        <button className="btn btn-success mt-4" onClick={handleCreateEvent}>
          Crear Evento
        </button>
      </div>


      <div className="mb-4">
        <h3>Buscar eventos cercanos</h3>
        {/* Barra de búsqueda */}
        <input
          type="text"
          className="form-control"
          placeholder="Introduce una dirección postal"
          value={address}
          onChange={(e) => setAddress(e.target.value)}          
        />
        <button className="btn btn-primary mt-2" onClick={handleSearch}>
          Buscar
        </button>

        
      </div>


      {/* Mostrar lat y lon de la ubicación encontrada */}
      {latLon && (
        <div className="mb-4">
          <p><strong>Latitud:</strong> {latLon.lat}</p>
          <p><strong>Longitud:</strong> {latLon.lon}</p>
        </div>
      )}

      {/* Mapa de OpenStreetMap */}
      <div className="mb-4">
        <MapContainer center={mapCenter} zoom={13} style={{ height: "400px", width: "100%" }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <MapCenter />
          {events.map((event) => (
            <Marker key={event.id} position={[event.lat, event.lon]} icon={eventIcon}>
              <Popup>{event.nombre}</Popup>
            </Marker>
          ))}
          {latLon && (
            <Circle
              center={[latLon.lat, latLon.lon]}
              radius={METROS_POR_GRADO * radius}
              color="blue"
              fillColor="blue"
              fillOpacity={0.2}
            />
          )}
          {latLon && (
            <Circle
              center={mapCenter}
              radius={200}
              color="red"
              fillColor="red"
              fillOpacity={0.2}
            >
              <Popup>Ubicación encontrada: {address}</Popup>
            </Circle>
          )}
        </MapContainer>
      </div>

      {loading && <div className="text-center mt-5">Cargando...</div>}
      {error && <div className="text-center mt-5 text-danger">{error}</div>}

      {!loading && !error && events.length > 0 && (
        <div className="row">
          <EventList events={events} />
        </div>
      )}
    </div>
  );
};

export default EventsMainPage;
