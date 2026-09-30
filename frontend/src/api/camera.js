const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getCameras() {
    const response = await fetch(`${API_URL}/api/cameras`);

    if (!response.ok) {
        throw new Error("Failed to fetch cameras");
    }

    return await response.json();
}