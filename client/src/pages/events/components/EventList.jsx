import React from 'react';
import EventItem from './EventItem';

const EventList = ({ events }) => {
  return (
    <div className="row">
      {events.map((event) => (
        <div className="col-md-4 col-sm-6 mb-4" key={event._id}>
          <EventItem event={event} />
        </div>
      ))}
    </div>
  );
};

export default EventList;
