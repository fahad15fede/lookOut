import cv2

for index in range(5):
    camera = cv2.VideoCapture(index)

    if camera.isOpened():
        success, frame = camera.read()

        if success:
            print(
                f"Camera {index}: WORKING - "
                f"{frame.shape[1]}x{frame.shape[0]}"
            )
        else:
            print(f"Camera {index}: OPENED but cannot read frame")
    else:
        print(f"Camera {index}: unavailable")

    camera.release()