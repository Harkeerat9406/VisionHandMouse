# Runs the main application, captures video, and integrates hand tracking with cursor control.

from hand_tracker import HandTracker
import cv2
import pyautogui

cap = cv2.VideoCapture(0)

screen_width, screen_height= pyautogui.size()


if not cap.isOpened():
    print("Cannot Open Webcam!!")
    exit(0)

tracker= HandTracker()

while cap.isOpened():
    ret, frame= cap.read()
    if not ret:
        break

    landmarks_dict, frame, results = tracker.find_hands(frame)
    
    if 8 in landmarks_dict:
        frame_x, frame_y= landmarks_dict[8]
        frame_height, frame_width, _ = frame.shape
        screen_x= screen_width - (frame_x / frame_width) * screen_width
        screen_y=  (frame_y / frame_height) * screen_height
        pyautogui.moveTo(screen_x, screen_y)


    cv2.imshow("Hand Window", frame)
    

    if cv2.waitKey(1) == ord('q'):
        break