const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getEvents(){
    const response = await fetch(`${API_URL}/api/events`);

    if(!response.ok){
        throw new Error(`Failed to fetch events: ${response.status}`);
    }

    const events = await response.json();
    return events;
}

export function getEvidenceUrl(path) {
    if (!path) {
        return null;
    }

    const filename = path.replaceAll("\\", "/").split("/").pop();
    return `${API_URL}/evidence/${filename}`;
}