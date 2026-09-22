from datetime import datetime
from pathlib import Path

import cv2


class EventManager:

    def __init__(self, output_dir="recordings/intrusions"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_intrusion(self, frame, track_id):

        timestamp = datetime.now()

        filename = (
            f"intrusion_"
            f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}_"
            f"id-{track_id}.jpg"
        )

        filepath = self.output_dir / filename

        success = cv2.imwrite(str(filepath), frame)

        if not success:
            raise RuntimeError("Failed to save intrusion screenshot.")

        event = {
            "event_type": "INTRUSION",
            "track_id": track_id,
            "timestamp": timestamp.isoformat(),
            "image_path": str(filepath)
        }

        return event