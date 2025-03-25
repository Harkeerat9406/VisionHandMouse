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

prev_wrist_y = None
fist_closed = False
previous_finger_state= {"left_click": False, "right_click": False}
ready_for_gesture = True
ready_for_gesture = True

while cap.isOpened():
    ret, frame= cap.read()
    if not ret:
        break

    landmarks_dict, frame, results = tracker.find_hands(frame)


    #CURSOR MOVEMENT
    if 8 in landmarks_dict:
        frame_x, frame_y= landmarks_dict[8]
        frame_height, frame_width, _ = frame.shape
        screen_x= screen_width - (frame_x / frame_width) * screen_width * 1.3
        screen_y=  (frame_y / frame_height) * screen_height *1.3 
        pyautogui.moveTo(screen_x, screen_y)




    #LEFT CLICK
    if 4 in landmarks_dict and 12 in landmarks_dict:
        thumb_middle_dist = tracker.distance(landmarks_dict[12], landmarks_dict[4])
        if previous_finger_state["left_click"] == False and thumb_middle_dist < 30:
            pyautogui.click()
            previous_finger_state["left_click"] = True
        
        if thumb_middle_dist >= 30 and previous_finger_state["left_click"]== True:
            previous_finger_state["left_click"] = False




    #RIGHT CLICK
    if 4 in landmarks_dict and 16 in landmarks_dict:
        thumb_ring_dist = tracker.distance(landmarks_dict[16], landmarks_dict[4])
        if previous_finger_state["right_click"]== False and thumb_ring_dist < 20:
            pyautogui.rightClick()
            previous_finger_state["right_click"] = True
        
        if thumb_ring_dist>=20 and previous_finger_state["right_click"] == True:
            previous_finger_state["right_click"] = False




    #ZOOM IN/OUT
    if 4 in landmarks_dict and 17 in landmarks_dict and 0 in landmarks_dict:
        
        wrist_y = landmarks_dict[0][1]
        
        if prev_wrist_y is not None:                      #Ensure its not the first frame
            thumb_pinky_dist = tracker.distance(landmarks_dict[4], landmarks_dict[17])

            if thumb_pinky_dist < 40:
                delta_y = wrist_y - prev_wrist_y
                if delta_y > 30:
                    pyautogui.scroll(150)
                elif delta_y <-30:
                    pyautogui.scroll(-150)
        
        prev_wrist_y = wrist_y




    #SHOW DESKTOP
    if all(finger in landmarks_dict for finger in [0, 4, 8, 12, 16, 20]):
        wrist = landmarks_dict[0]
        fingertips = [landmarks_dict[4], landmarks_dict[8], landmarks_dict[12], landmarks_dict[16], landmarks_dict[20]]

        avg_distance = sum(tracker.distance(wrist, finger) for finger in fingertips)/ len(fingertips)

        if avg_distance < 100 and not fist_closed:
            # pyautogui.hotkey("winleft", "D")
            pyautogui.keyDown("win")
            pyautogui.press("d")
            pyautogui.keyUp("win")
            fist_closed = True
        
        if avg_distance >= 100 and fist_closed:
            fist_closed = False




    #SWITCH APPLICATIONS/TABS
    if all(finger in landmarks_dict for finger in [0, 4, 8, 12, 16, 20]):
        gesture_orientation = tracker.palm_orientation(landmarks_dict)
        
        #SWITCH APPLICATION
        # if gesture_orientation == 'switch_app':
        #     rotation_side = tracker.detect_rotation(landmarks_dict)

        #     if rotation_side == 'left' and ready_for_gesture:
        #         pyautogui.keyDown('alt')
        #         pyautogui.press('tab')
        #         pyautogui.press('left')
        #         pyautogui.press('left')
        #         pyautogui.keyUp('alt')
        #         ready_for_gesture = False

        #     elif rotation_side == 'right' and ready_for_gesture:
        #         pyautogui.keyDown('alt')
        #         pyautogui.press('tab')
        #         pyautogui.keyUp('alt')
        #         ready_for_gesture = False
            
        #     elif rotation_side == 'upright' and not ready_for_gesture:
        #         ready_for_gesture = True

        # NOTES: switching application window isnt functioning properly, it will be added later so for now we will keep detecting orientation of hand

        
        if gesture_orientation == 'switch_tab':
            rotation_side = tracker.detect_rotation(landmarks_dict)
            if rotation_side == 'left' and ready_for_gesture:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                ready_for_gesture = False
            
            elif rotation_side == 'right' and ready_for_gesture:
                pyautogui.hotkey('ctrl', 'tab')
                ready_for_gesture = False
            
            elif rotation_side == 'upright' and not ready_for_gesture:
                ready_for_gesture = True



    cv2.namedWindow("Hand Window", cv2.WINDOW_NORMAL)  # Allows window resizing
    cv2.setWindowProperty("Hand Window", cv2.WND_PROP_TOPMOST, 1)  # Keeps it on top
    cv2.imshow("Hand Window", frame)
    

    if cv2.waitKey(1) == ord('q'):
        cv2.setWindowProperty("Hand Window", cv2.WND_PROP_TOPMOST, 0)  # Remove always-on-top
        break

cap.release()
cv2.destroyAllWindows()