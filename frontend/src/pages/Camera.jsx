import { useEffect, useState, useCallback } from "react";
import { getCameras } from "../api/camera";
import "./Camera.css";

function Camera() {
    const [cameras, setCameras] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadCameras = useCallback(async () => {
        try {
            const data = await getCameras();

            setCameras(data);
            setError(null);
        } catch (err) {
            console.error(err);
            setError("Unable to load cameras");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadCameras();

        const interval = setInterval(() => {
            loadCameras();
        }, 5000);

        return () => {
            clearInterval(interval);
        };
    }, [loadCameras]);

    if (loading) {
        return (
            <div className="cameras-page">
                <div className="cameras-loading">
                    <div className="loading-spinner"></div>
                    <p>Loading cameras...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="cameras-page">
                <div className="cameras-error">
                    <div className="error-icon">⚠️</div>
                    <h2>Camera Service Unavailable</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="cameras-page">

            <div className="cameras-heading">
                <div>
                    <h1>Cameras</h1>
                    <p>
                        Monitor connected security cameras and vision services.
                    </p>
                </div>

                <span>
                    {cameras.length} camera{cameras.length !== 1 ? "s" : ""}
                </span>
            </div>

            {cameras.length === 0 ? (
                <div className="cameras-empty">
                    <p>No cameras have been registered.</p>
                </div>
            ) : (
                <div className="cameras-grid">

                    {cameras.map((camera) => (

                        <div
                            className="camera-card"
                            key={camera.id}
                        >

                            <div className="camera-card-header">

                                <div>
                                    <h2>{camera.name}</h2>

                                    <p>
                                        {camera.location || "No location specified"}
                                    </p>
                                </div>

                                <span
                                    className={
                                        camera.status === "online"
                                            ? "camera-status online"
                                            : "camera-status offline"
                                    }
                                >
                                    {camera.status}
                                </span>

                            </div>

                            <div className="camera-preview">
                                <div className="preview-placeholder">
                                    <span>Camera Preview</span>
                                    <small>
                                        Live streaming will be added later
                                    </small>
                                </div>
                            </div>

                            <div className="camera-details">

                                <div className="camera-detail">
                                    <span>Camera ID</span>
                                    <strong>{camera.id}</strong>
                                </div>

                                <div className="camera-detail">
                                    <span>Source</span>
                                    <strong>{camera.source}</strong>
                                </div>

                                <div className="camera-detail">
                                    <span>Vision Service</span>
                                    <strong>{camera.vision_status}</strong>
                                </div>

                                <div className="camera-detail">
                                    <span>Detection Model</span>
                                    <strong>{camera.detection_model}</strong>
                                </div>

                                <div className="camera-detail">
                                    <span>Tracking</span>
                                    <strong>{camera.tracking}</strong>
                                </div>

                                <div className="camera-detail">
                                    <span>Enabled</span>
                                    <strong>
                                        {camera.is_enabled ? "Yes" : "No"}
                                    </strong>
                                </div>

                            </div>

                        </div>

                    ))}

                </div>
            )}

        </div>
    );
}

export default Camera;