import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Events from './pages/Events';
import Camera from './pages/Camera';
import './App.css';

function App() {
    const [systemOnline, setSystemOnline] = useState(true);

    return (
        <Router>
            <div className="app">
                <Header systemOnline={systemOnline} />
                <div className="app-layout">
                    <Sidebar />
                    <main className="app-main">
                        <Routes>
                            <Route 
                                path="/" 
                                element={<Dashboard onSystemStatusChange={setSystemOnline} />} 
                            />
                            <Route 
                                path="/events" 
                                element={<Events onSystemStatusChange={setSystemOnline} />} 
                            />
                            <Route path="/cameras" element={<Camera />} />
                        </Routes> 
                    </main>
                </div>
            </div>
        </Router>
    );
}

export default App;
