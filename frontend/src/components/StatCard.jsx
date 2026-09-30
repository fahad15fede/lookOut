import './StatCard.css';

function StatCard({ title, value, icon, variant = 'default' }) {
    return (
        <div className={`stat-card stat-card-${variant}`}>
            <div className="stat-card-content">
                <div className="stat-card-header">
                    <span className="stat-card-title">{title}</span>
                    {icon && <span className="stat-card-icon">{icon}</span>}
                </div>
                <div className="stat-card-value">{value}</div>
            </div>
        </div>
    );
}

export default StatCard;
