import StatusBadge from './StatusBadge';
import './Header.css';

function Header({ systemOnline }) {
    return (
        <header className="header">
            <div className="header-content">
                <div className="header-title">
                    <h1>lookOut</h1>
                    <p className="header-subtitle">Home Security Dashboard</p>
                </div>
                <div className="header-status">
                    <StatusBadge online={systemOnline} />
                </div>
            </div>
        </header>
    );
}

export default Header;
