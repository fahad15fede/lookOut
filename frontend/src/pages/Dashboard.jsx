import { useState, useEffect, useCallback } from 'react';
import { getEvents } from '../api/events';
import { calculateStats } from '../utils/statsUtils';
import StatCard from '../components/StatCard';
import EventList from '../components/EventList';
import './Dashboard.css';

function Dashboard({ onSystemStatusChange }) {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshing, setRefreshing] = useState(false);

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

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="loading-spinner"></div>
                <p>Loading security events...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="dashboard-error">
                <div className="error-icon">⚠️</div>
                <h2>Unable to connect to lookOut backend</h2>
                <p>{error}</p>
                <button onClick={handleRefresh} className="btn-retry">
                    Retry Connection
                </button>
            </div>
        );
    }

    const stats = calculateStats(events);
    const recentEvents = events.slice(0, 6);

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h2 className="dashboard-title">Dashboard Overview</h2>
                <button 
                    onClick={handleRefresh} 
                    className="btn-refresh"
                    disabled={refreshing}
                >
                    {refreshing ? '↻ Refreshing...' : '↻ Refresh'}
                </button>
            </div>

            <div className="stats-grid">
                <StatCard
                    title="Total Events"
                    value={stats.totalEvents}
                    icon="📊"
                    variant="primary"
                />
                <StatCard
                    title="Today's Events"
                    value={stats.todayEvents}
                    icon="📅"
                    variant="warning"
                />
                <StatCard
                    title="Latest Track ID"
                    value={stats.latestTrackId}
                    icon="🔢"
                    variant="default"
                />
                <StatCard
                    title="System Status"
                    value="Online"
                    icon="✓"
                    variant="success"
                />
            </div>

            <div className="recent-section">
                <h3 className="section-title">Recent Intrusions</h3>
                <EventList 
                    events={recentEvents}
                    emptyMessage="No security events recorded."
                />
            </div>
        </div>
    );
}

export default Dashboard;
