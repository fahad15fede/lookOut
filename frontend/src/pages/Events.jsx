import { useState, useEffect, useCallback } from 'react';
import { getEvents } from '../api/events';
import { isToday } from '../utils/dateUtils';
import EventList from '../components/EventList';
import './Events.css';

function Events({ onSystemStatusChange }) {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshing, setRefreshing] = useState(false);
    const [filter, setFilter] = useState('all');
    const [searchTrackId, setSearchTrackId] = useState('');

    const loadEvents = useCallback(async () => {
        try {
            const data = await getEvents();
            setEvents(data);
            setError(null);
            if (onSystemStatusChange) {
                onSystemStatusChange(true);
            }
        } catch (err) {
            setError(err.message);
            if (onSystemStatusChange) {
                onSystemStatusChange(false);
            }
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }, [onSystemStatusChange]);

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadEvents();
    }, [loadEvents]);

    async function handleRefresh() {
        setRefreshing(true);
        await loadEvents();
    }

    function getFilteredEvents() {
        let filtered = events;

        if (filter === 'today') {
            filtered = filtered.filter(event => isToday(event.detected_at));
        }

        if (searchTrackId.trim()) {
            const trackId = parseInt(searchTrackId, 10);
            if (!isNaN(trackId)) {
                filtered = filtered.filter(event => event.track_id === trackId);
            }
        }

        return filtered;
    }

    if (loading) {
        return (
            <div className="events-loading">
                <div className="loading-spinner"></div>
                <p>Loading security events...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="events-error">
                <div className="error-icon">⚠️</div>
                <h2>Unable to connect to lookOut backend</h2>
                <p>{error}</p>
                <button onClick={handleRefresh} className="btn-retry">
                    Retry Connection
                </button>
            </div>
        );
    }

    const filteredEvents = getFilteredEvents();

    return (
        <div className="events-page">
            <div className="events-header">
                <h2 className="events-title">Security Events</h2>
                <button 
                    onClick={handleRefresh} 
                    className="btn-refresh"
                    disabled={refreshing}
                >
                    {refreshing ? '↻ Refreshing...' : '↻ Refresh'}
                </button>
            </div>

            <div className="events-controls">
                <div className="filter-buttons">
                    <button 
                        className={`filter-btn ${filter === 'all' ? 'filter-btn-active' : ''}`}
                        onClick={() => setFilter('all')}
                    >
                        All Events ({events.length})
                    </button>
                    <button 
                        className={`filter-btn ${filter === 'today' ? 'filter-btn-active' : ''}`}
                        onClick={() => setFilter('today')}
                    >
                        Today ({events.filter(e => isToday(e.detected_at)).length})
                    </button>
                </div>

                <div className="search-box">
                    <input
                        type="text"
                        placeholder="Search by Track ID..."
                        value={searchTrackId}
                        onChange={(e) => setSearchTrackId(e.target.value)}
                        className="search-input"
                    />
                </div>
            </div>

            <div className="events-content">
                <EventList 
                    events={filteredEvents}
                    emptyMessage="No events match your filters."
                />
            </div>
        </div>
    );
}

export default Events;
