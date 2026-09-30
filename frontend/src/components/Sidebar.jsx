import { NavLink } from 'react-router-dom';
import './Sidebar.css';

function Sidebar() {
    return (
        <aside className="sidebar">
            <nav className="sidebar-nav">
                <NavLink 
                    to="/" 
                    className={({ isActive }) => 
                        isActive ? 'nav-item nav-item-active' : 'nav-item'
                    }
                    end
                >
                    <span className="nav-icon">📊</span>
                    <span className="nav-text">Dashboard</span>
                </NavLink>

                <NavLink 
                    to="/events" 
                    className={({ isActive }) => 
                        isActive ? 'nav-item nav-item-active' : 'nav-item'
                    }
                >
                    <span className="nav-icon">🚨</span>
                    <span className="nav-text">Events</span>
                </NavLink>

                <NavLink                
                    to="/cameras" 
                    className={({ isActive }) => 
                        isActive ? 'nav-item nav-item-active' : 'nav-item'
                    }
                >
                    <span className="nav-icon">🎥</span>
                    <span className="nav-text">Camera</span>
                </NavLink>

                <div className="nav-item nav-item-disabled">
                    <span className="nav-icon">⚙️</span>
                    <span className="nav-text">Settings</span>
                    <span className="nav-badge">Soon</span>
                </div>
            </nav>
        </aside>
    );
}

export default Sidebar;
