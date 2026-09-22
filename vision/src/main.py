import cv2

from detector import PersonDetector
from intrusion import IntrusionDetector
from event_manager import EventManager

def main():

    detector = PersonDetector()

    # Temporary boundary position
    intrusion_detector = IntrusionDetector(boundary_y=350)

    event_manager = EventManager()

    camera = cv2.VideoCapture(0)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        raise RuntimeError("Could not open camera.")
    
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Camera resolution: {width}x{height}")

    cv2.namedWindow(
        'sentinelAI',
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        'sentinelAI',
        1200,
        800
    )

    while True:

        success, frame = camera.read()

        if not success:
            break

        result = detector.track(frame)

        # Draw our security boundary
        intrusion_detector.draw_boundary(frame)

        boxes = result.boxes

        if boxes is not None and boxes.id is not None:

            coordinates = boxes.xyxy.cpu().numpy()
            track_ids = boxes.id.int().cpu().tolist()

            for box, track_id in zip(coordinates, track_ids):

                x1, y1, x2, y2 = map(int, box)
                person_crop = frame[y1:y2, x1:x2]

                if person_crop.size > 0:
                    cv2.imshow(f"Person ID {track_id}", person_crop)

                # Bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 255),
                    2
                )

                # Person tracking point
                point = intrusion_detector.get_feet_position(
                    (x1, y1, x2, y2)
                )

                cv2.circle(
                    frame,
                    point,
                    6,
                    (255, 255, 255),
                    -1
                )

                point = intrusion_detector.get_feet_position(
                    (x1, y1, x2, y2)
                )

                cv2.circle(
                    frame,
                    point,
                    6,
                    (255, 255, 255),
                    -1
                )

                state = intrusion_detector.get_state(point)

                intrusion = intrusion_detector.check_intrusion(
                    track_id,
                    point
                )

                if intrusion:

                    status = f"ID {track_id} - INTRUSION"

                    event = event_manager.save_intrusion(
                        frame,
                        track_id
                    )

                    print("\n🚨 INTRUSION DETECTED")
                    print(f"Person ID: {event['track_id']}")
                    print(f"Time: {event['timestamp']}")
                    print(f"Evidence: {event['image_path']}")

                else:

                    status = f"ID {track_id} - {state.upper()}"

                cv2.putText(
                    frame,
                    status,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

        cv2.imshow(
            "SentinelAI",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()