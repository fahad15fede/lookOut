from ultralytics import YOLO

class PersonDetector:

    def __init__(self):
        self.model = YOLO('yolo11n.pt')
    def track(self, frame):

        results=self.model.track(
            frame,
            classes=[0],
            persist=True,
            tracker='bytetrack.yaml',
            verbose=False
        )

        return results[0]

