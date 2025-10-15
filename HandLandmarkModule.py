import mediapipe as mp
import cv2
import csv

from collections import deque
from HandModel import KeyPointClassifier
from HandModel import PointHistoryClassifier
from HandDetectionModule import calc_bounding_rect, calc_landmark_list, draw_landmarks
from HandDetectionModule import pre_process_point_history, pre_process_landmark

mp_hands = mp.solutions.hands
keypoint_classifier = KeyPointClassifier()
point_history_classifier = PointHistoryClassifier()

# Initialize the point history deque
point_history = deque(maxlen=16)
# Load the labels for keypoint classifier and point history classifier
keypoint_classifier_labels = []
with open('C:/Users/chenr/Documents/GitHub/HandGestureDJITello/HandModel/keypoint_classifier/keypoint_classifier_label.csv',
          encoding='utf-8-sig') as f:
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

point_history_classifier_labels = []
with open('C:/Users/chenr/Documents/GitHub/HandGestureDJITello/HandModel/point_history_classifier/point_history_classifier_label.csv',
          encoding='utf-8-sig') as f:
    point_history_classifier_labels = csv.reader(f)
    point_history_classifier_labels = [row[0] for row in point_history_classifier_labels]

class handLandmarkDetector:
    def __init__(self, mode=False, maxHands=2, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        self.image_trigger = False
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                         min_detection_confidence=self.detectionConf,
                                         min_tracking_confidence=self.trackConf)
        self.mp_draw = mp.solutions.drawing_utils
    def findHands(self, img, draw=True):
        img = cv2.flip(img,1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            # Draw hand to image
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def drawFingerPoint(self, img, drawLeft=True, drawRight=True, finger=8):

        if self.results.multi_hand_landmarks:
            for id_hand, hnd in enumerate(self.results.multi_handedness):
                # left/right hand name
                hand_name = hnd.classification[0].label

                hand = self.results.multi_hand_landmarks[id_hand]

                h, w, c = img.shape

                # Bounding box calculation
                brect = calc_bounding_rect(img, hand)

                # Landmark calculation
                landmark_list = calc_landmark_list(img, hand)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:
                    point_history.append(landmark_list[8])
                else:
                    point_history.append([0, 0])

                # Finger gesture classification
                finger_gesture_id = 0
                point_history_len = len(point_history)
                if point_history_len == 16:
                    pre_processed_point_history_list = pre_process_point_history(img, point_history)
                    finger_gesture_id = point_history_classifier(pre_processed_point_history_list)

                # Finger gesture state (Move/close/pointer/Hand sign) text
                finger_gesture_text = point_history_classifier_labels[finger_gesture_id]
                finger_state_text = hand_name + " finger: " + finger_gesture_text

                # This is used for Debug
                #print(hand_name,':',finger_gesture_text)

                # Hand state (open/close) text
                hand_sign_text = keypoint_classifier_labels[hand_sign_id]
                hand_state_text = hand_name + " hand: " + hand_sign_text


                if drawLeft and hand_name == 'Left':

                    img = draw_landmarks(img, landmark_list)
                    ind_finger_l_x, ind_finger_l_y = landmark_list[finger]
                    cv2.circle(img, (int(ind_finger_l_x), int(ind_finger_l_y)), 25, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, hand_name, (int(w * 0.19), int(h * 0.05)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # Draw bounding box for left hand
                    cv2.rectangle(img, (brect[0], brect[1]), (brect[2], brect[3]), (255, 255, 0), 1)
                    cv2.putText(img, hand_state_text, (brect[0] + 5, brect[1] - 4),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                    # Display finger_gesture_text for left finger on the bottom-left corner
                    cv2.putText(img, finger_state_text, (int(w * 0.11), int(h * 0.95)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

                    # Store left hand info and wait for return
                    left_hand_info = [(ind_finger_l_x, ind_finger_l_y), hand_sign_text, hand_name]

                if drawRight and hand_name == 'Right':

                    img = draw_landmarks(img, landmark_list)
                    ind_finger_r_x, ind_finger_r_y = landmark_list[finger]
                    cv2.circle(img, (int(ind_finger_r_x), int(ind_finger_r_y)), 25, (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, hand_name, (int(w * 0.75), int(h * 0.05)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    # Draw bounding box for right hand
                    cv2.rectangle(img, (brect[0], brect[1]), (brect[2], brect[3]), (255, 255, 0), 1)
                    cv2.putText(img, hand_state_text, (brect[0] + 5, brect[1] - 4),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                    # Display finger_gesture_text for right finger on the bottom-right corner
                    cv2.putText(img, finger_state_text, (int(w * 0.76), int(h * 0.95)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                    # Store left hand info and wait for return
                    right_hand_info = [(ind_finger_r_x, ind_finger_r_y), hand_sign_text, hand_name]


                    # Image capture trigger
                    if right_hand_info[1] == 'OK':
                        self.image_trigger = True

                try:
                    return [left_hand_info[0], right_hand_info[0], self.image_trigger]
                except:
                    pass

def in_circle(center_x, center_y, radius, coords):
    x, y = coords
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

