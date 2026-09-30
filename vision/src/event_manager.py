from datetime import datetime
from pathlib import Path
import cv2


class EventManager:
    def __init__(self,camera_id, output_dir="recordings/intrusions"):
        self.camera_id= camera_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_intrusion(self, frame, track_id, box):
        timestamp = datetime.now()

        time_string = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        full_filename = (
            f"intrusion_{time_string}_id-{track_id}_full.jpg"
        )

        crop_filename = (
            f"intrusion_{time_string}_id-{track_id}_crop.jpg"
        )

        full_path = self.output_dir / full_filename
        crop_path = self.output_dir / crop_filename

        # Save full camera frame
        if not cv2.imwrite(str(full_path), frame):
            raise RuntimeError("Failed to save intrusion frame.")

        # Get bounding box
        x1, y1, x2, y2 = map(int, box)

        height, width = frame.shape[:2]

        # Keep coordinates inside image boundaries
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        # Crop the detected person
        person_crop = frame[y1:y2, x1:x2]

        if person_crop.size == 0:
            raise RuntimeError("Intruder crop is empty.")

        if not cv2.imwrite(str(crop_path), person_crop):
            raise RuntimeError("Failed to save intruder crop.")

        return {
            "event_type": "INTRUSION",
            "track_id": track_id,
            "timestamp": timestamp.isoformat(),
            "image_path": str(full_path),
            "crop_path": str(crop_path),
            "camera_id": self.camera_id
        }