import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
import { useAPI } from "../../context/APIContext";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { Icon } from "leaflet";
import { useNavigate } from "react-router-dom"; // Importamos useNavigate
import "leaflet/dist/leaflet.css";

const PaisesViewPage = () => {
  const { getUser } = useAuth();  // Obtener usuario
  const { paises } = useAPI();  // Llamar a la API para los países
  const [visitedCountries, setVisitedCountries] = useState([]);  // Países visitados
  const [mapCenter, setMapCenter] = useState([51.505, -0.09]);  // Posición inicial del mapa
  const [loading, setLoading] = useState(false);  // Estado de carga
  const [error, setError] = useState(null);  // Estado de error
  const [email, setEmail] = useState("");  // Email del usuario
  const [selectedCountryImage, setSelectedCountryImage] = useState(""); // Imagen del país seleccionado
  const navigate = useNavigate(); // Función para navegar

  // Icono personalizado para los marcadores
  const countryIcon = new Icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  // Función para obtener el email del usuario
  const fetchUserEmail = () => {
    const user = getUser();
    if (user && user.email) {
      setEmail(user.email);  // Establecer el email del usuario
    } else {
      setError("No se encontró información del usuario. Inicia sesión nuevamente.");
    }
  };

  // Función para obtener los países visitados
  const fetchVisitedCountries = async () => {
    if (!email) return;  // No hacer nada si no hay email

    setLoading(true);
    setError(null);

    try {
      const response = await paises.getByEmail(email);  // Obtener países visitados usando el email
      if (response.status >= 200 && response.status < 300) {
        setVisitedCountries(response.data);
        if (response.data.length > 0) {
          // Si hay países visitados, centrar el mapa en el primer país
          setMapCenter([response.data[0].lat, response.data[0].lon]);
        }
      } else {
        setError("Error al obtener los países visitados.");
      }
    } catch (error) {
      setError("Error al obtener los países visitados.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserEmail();  // Obtener el email al cargar el componente
  }, []);

  useEffect(() => {
    if (email) {
      fetchVisitedCountries();  // Realizar la búsqueda de países cuando se tiene el email
    }
  }, [email]);

  // Componente para centrar el mapa
  const MapCenter = () => {
    const map = useMap();

    useEffect(() => {
      map.setView(mapCenter, map.getZoom());
    }, [map, mapCenter]);

    return null;
  };

  // Función para manejar la selección de un marcador
  const handleMarkerClick = (countryImage) => {
    setSelectedCountryImage(countryImage);  // Establecer la imagen seleccionada
  };

  // Función para navegar a la página de creación de país
  const handleCreateCountry = () => {
    navigate("/paises/create"); // Redirige a /paises/create
  };

  return (
    <div className="container py-5">
      <h1 className="text-center mb-4">Países Visitados</h1>

      <div className="text-center mb-4">
        {/* Botón "Crear País" */}
        <button className="btn btn-success" onClick={handleCreateCountry}>
          Crear País Visitado
        </button>
      </div>

      {loading && <div className="text-center mt-5">Cargando...</div>}
      {error && <div className="text-center mt-5 text-danger">{error}</div>}

      {!loading && !error && visitedCountries.length > 0 && (
        <div className="mb-4">
          <MapContainer center={mapCenter} zoom={5} style={{ height: "400px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MapCenter />
            {visitedCountries.map((country) => (
              <Marker
                key={country.id}
                position={[country.lat, country.lon]}
                icon={countryIcon}
                eventHandlers={{
                  click: () => handleMarkerClick(country.imagen),  // Al hacer clic, actualizar la imagen
                }}
              >
                <Popup>{country.nombre}</Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      )}

      {!loading && !error && visitedCountries.length === 0 && (
        <div className="text-center mt-5">No se encontraron países visitados.</div>
      )}

      {/* Mostrar la imagen del país seleccionado debajo del mapa */}
      {selectedCountryImage && (
        <div className="text-center mt-4">
          <h5>Imagen del País</h5>
          <img
            src={selectedCountryImage}
            alt="Imagen del País"
            className="img-fluid"
            style={{ maxHeight: "300px" }}
          />
        </div>
      )}
    </div>
  );
};

export default PaisesViewPage;
