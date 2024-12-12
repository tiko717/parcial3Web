import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useData } from '../../../context/DataContext';

const EventItem = ({ event }) => {
  const { setActualEvent } = useData();
  const navigate = useNavigate();

  const handleClick = () => {
    setActualEvent(event);
    navigate("/events/" + event._id);
  };

  return (
    <div
      onClick={handleClick}
      className="card shadow-lg h-100 border-0 rounded-lg overflow-hidden"
      style={{ cursor: 'pointer', transition: 'transform 0.3s ease' }}
      onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
      onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
    >
      <img
        src={event.imagen}
        className="card-img-top"
        alt={event.nombre}
        style={{ objectFit: 'cover', height: '200px' }}
      />
      <div className="card-body d-flex flex-column">
        <h5 className="card-title text-center mb-3 text-uppercase">{event.nombre}</h5>
        <p className="card-text text-center text-muted small mb-2">
          {new Date(event.timestamp).toLocaleString()}
        </p>
        <p className="card-text text-center text-muted small">
          Organizador: <strong>{event.organizador}</strong>
        </p>
        <div className="d-flex justify-content-between align-items-center mt-auto">
          <button className="btn btn-info btn-block text-white font-weight-bold">
            Ver más
          </button>
        </div>
      </div>
    </div>
  );
};

export default EventItem;
