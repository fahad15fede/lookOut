import cv2

from detector import PersonDetector
from intrusion import IntrusionDetector
from event_manager import EventManager
from api_clients import LookoutAPIClient

def main():

    detector = PersonDetector()

    # Temporary boundary position
    intrusion_detector = IntrusionDetector(boundary_y=350)

    CAMERA_ID = 1
    CAMERA_SOURCE = 1

    event_manager = EventManager(
            camera_id=CAMERA_ID
        )
    api_client = LookoutAPIClient()

    camera = cv2.VideoCapture(CAMERA_SOURCE)


    if not camera.isOpened():
        api_client.send_camera_status(
            camera_id=CAMERA_ID,
            camera_status="offline",
            vision_status="offline"
        )
        raise RuntimeError("Could not open camera.")

    print("[CAMERA] Camera opened successfully")

    response = api_client.send_camera_status(
        camera_id=CAMERA_ID,
        camera_status="online",
        vision_status="running"
    )

    print("[CAMERA STATUS RESPONSE]", response)
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
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
        raw_frame = frame.copy()
        result = detector.track(frame)

        # Draw our security boundary
        intrusion_detector.draw_boundary(frame)

        boxes = result.boxes

        if boxes is not None and boxes.id is not None:

            coordinates = boxes.xyxy.cpu().numpy()
            track_ids = boxes.id.int().cpu().tolist()

            for box, track_id in zip(coordinates, track_ids):

                x1, y1, x2, y2 = map(int, box)

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
                        track_id,
                        box
                    )

                    print("\n🚨 INTRUSION DETECTED")
                    print(f"Person ID: {event['track_id']}")
                    print(f"Time: {event['timestamp']}")
                    print(f"Evidence: {event['image_path']}")
                    print(f"Person crop: {event['crop_path']}")

                    saved_event = api_client.send_intrusion_event(event)

                    if saved_event:
                        print(f"Stored in database with ID: {saved_event['id']}")

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


    api_client.send_camera_status(
        camera_id= CAMERA_ID,
        camera_status="offline",
        vision_status="offline"
    )
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()