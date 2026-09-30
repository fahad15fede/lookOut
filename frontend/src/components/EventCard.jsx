import { getEvidenceUrl } from '../api/events';
import { formatDate, formatTime } from '../utils/dateUtils';
import './EventCard.css';

function EventCard({ event }) {
    const fullImageUrl = getEvidenceUrl(event.image_path);
    const cropImageUrl = getEvidenceUrl(event.crop_path);

    return (
        <div className="event-card">
            <div className="event-card-image">
                {cropImageUrl ? (
                    <img
                        src={cropImageUrl}
                        alt={`Intrusion event ${event.id}`}
                        className="event-image"
                    />
                ) : (
                    <div className="event-image-placeholder">
                        <span>No Image</span>
                    </div>
                )}
            </div>

            <div className="event-card-content">
                <div className="event-card-header">
                    <span className="event-badge">🚨 {event.event_type}</span>
                    <span className="event-id">#{event.id}</span>
                </div>

                <div className="event-details">
                    <div className="event-detail">
                        <span className="event-label">Camera:</span>
                        <span className="event-value">{event.camera_name || "Unknown Camera"}</span>
                    </div>
                    {event.camera_location && (
                        <div className="event-detail">
                            <span className="event-label">Location:</span>
                            <span className="event-value">{event.camera_location}</span>
                        </div>
                    )}
                    <div className="event-detail">
                        <span className="event-label">Track ID:</span>
                        <span className="event-value">{event.track_id}</span>
                    </div>
                    <div className="event-detail">
                        <span className="event-label">Date:</span>
                        <span className="event-value">{formatDate(event.detected_at)}</span>
                    </div>
                    <div className="event-detail">
                        <span className="event-label">Time:</span>
                        <span className="event-value">{formatTime(event.detected_at)}</span>
                    </div>
                </div>

                {fullImageUrl && (
                    <a
                        href={fullImageUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="event-link"
                    >
                        View Full Evidence →
                    </a>
                )}
            </div>
        </div>
    );
}

export default EventCard;