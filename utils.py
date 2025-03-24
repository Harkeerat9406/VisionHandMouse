# Stores helper functions if needed.

import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Cannot open webcam")
    exit(0)

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Failed to capture frame")
        break

    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
