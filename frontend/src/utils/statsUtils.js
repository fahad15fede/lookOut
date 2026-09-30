import { isToday } from './dateUtils';

export function calculateStats(events) {
    const totalEvents = events.length;
    const todayEvents = events.filter(event => isToday(event.detected_at)).length;
    
    const latestTrackId = events.length > 0 
        ? Math.max(...events.map(e => e.track_id))
        : 0;

    return {
        totalEvents,
        todayEvents,
        latestTrackId
    };
}
