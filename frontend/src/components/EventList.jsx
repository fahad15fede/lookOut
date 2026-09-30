import EventCard from './EventCard';
import './EventList.css';

function EventList({ events, emptyMessage = "No security events recorded." }) {
    if (events.length === 0) {
        return (
            <div className="event-list-empty">
                <p>{emptyMessage}</p>
            </div>
        );
    }

    return (
        <div className="event-list">
            {events.map((event) => (
                <EventCard key={event.id} event={event} />
            ))}
        </div>
    );
}

export default EventList;
