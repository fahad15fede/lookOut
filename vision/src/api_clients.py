import requests


class LookoutAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def send_intrusion_event(self, event):
        payload = {
            "event_type": event["event_type"],
            "track_id": event["track_id"],
            "detected_at": event["timestamp"],
            "image_path": event["image_path"],
            "crop_path": event["crop_path"],
            "camera_id": event["camera_id"]
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/events",
                json=payload,
                timeout=5
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            print(f"[API ERROR] Could not send event: {error}")
            return None

    def send_camera_status(self, camera_id, camera_status, vision_status):
        
        payload={
            "status": camera_status,
            "vision_status": vision_status
        }

        try:
            response = requests.patch(
                f"{self.base_url}/api/cameras/{camera_id}/status",
                json=payload,
                timeout=5
            )

            response.raise_for_status()

            return response.json()
        except requests.RequestException as error:
            print(f"[API ERROR] Could not send camera status: {error}")
            return None