# Handles hand detection and landmark extraction using MediaPipe.

import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands= self.mp_hands.Hands(max_num_hands= 1)
        self.mp_drawing= mp.solutions.drawing_utils

    def find_hands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results= self.hands.process(rgb_frame)
        landmarks_dict = {}

        if results.multi_hand_landmarks:
            frame_height, frame_width, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
                for id, landmark in enumerate(hand_landmarks.landmark):
                    pixel_x = int(landmark.x * frame_width)
                    pixel_y = int(landmark.y * frame_height)
                    
                    if id in [0, 4, 8, 12, 16, 17, 20]:
                        landmarks_dict[id] = (pixel_x, pixel_y)

        return landmarks_dict, frame, results
    

    def distance(self, p1, p2):
        return math.sqrt((p1[0]-p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    

    def palm_orientation(self, landmarks_dict):
        wrist_x, wrist_y = landmarks_dict[0]
        index_x, index_y = landmarks_dict[8]
        pinky_x, pinky_y = landmarks_dict[20]

        horizontal_diff = abs(pinky_x - index_x)
        # if horizontal_diff > 70:  # Hand is rotated
        #     return 'switch_app'
        if horizontal_diff > 30:
            return 'switch_tab'
        return None



    def detect_rotation(self, landmarks_dict):
        wrist_x = landmarks_dict[0][0]
        fingertips_x = [landmarks_dict[i][0] for i in [4, 8, 12, 16, 20]]
        avg_fingertips_x = sum(fingertips_x)/len(fingertips_x)

        if avg_fingertips_x < wrist_x - 30:
            return 'right'                          #because webcam view is inverted
        elif avg_fingertips_x > wrist_x + 30:
            return 'left' 
        return 'upright'