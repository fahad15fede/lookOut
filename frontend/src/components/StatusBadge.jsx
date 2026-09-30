import './StatusBadge.css';

function StatusBadge({ online }) {
    return (
        <div className={`status-badge ${online ? 'status-online' : 'status-offline'}`}>
            <span className="status-dot"></span>
            <span className="status-text">
                {online ? 'System Online' : 'System Offline'}
            </span>
        </div>
    );
}

export default StatusBadge;
