import cv2
import mediapipe as mp
import os
import sys
import numpy as np
import copy
import itertools

# Suppress MediaPipe logging messages by disabling all
os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stderr.fileno())


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands


def pre_process_point_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] - base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] - base_y) / image_height

    # Convert to a one-dimensional list
    temp_point_history = list(itertools.chain.from_iterable(temp_point_history))

    return temp_point_history

def calc_bounding_rect(image, hand_landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(hand_landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)
    return [x, y, x + w, y + h]
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

def draw_bounding_rect(image, brect):
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                  (0, 0, 0), 1)
    return image

def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:

        # Thumb
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (255, 255, 0), 2)

        # Index finger
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (255, 255, 0), 2)

        # Middle finger
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (255, 255, 0), 2)

        # Ring finger
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (255, 255, 0), 2)

        # Little finger
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (255, 255, 0), 2)

        # Palm
        cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), (255, 255, 0), 2)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), (0, 0, 0), 6)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), (255, 255, 0), 2)

    for index, landmark in enumerate(landmark_point):

        # Wrist 1
        if index == 0:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Wrist 2
        if index == 1:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Thumb: Root
        if index == 2:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Thumb: 1st joint
        if index == 3:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Thumb: fingertip
        if index == 4:
            cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        # Index finger: Root
        if index == 5:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Index finger: 2nd joint
        if index == 6:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Index finger: 1st joint
        if index == 7:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Index finger: fingertip
        if index == 8:
            cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        # Middle finger: Root
        if index == 9:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Middle finger: 2nd joint
        if index == 10:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Middle finger: 1st joint
        if index == 11:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0),-1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Middle finger: fingertip
        if index == 12:
            cv2.circle(image, (landmark[0], landmark[1]), 8,(255, 255, 0),-1)
            cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        # Ring finger: Root
        if index == 13:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Ring finger: 2nd joint
        if index == 14:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Ring finger: 1st joint
        if index == 15:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Ring finger: fingertip
        if index == 16:
            cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        # Little finger: Root
        if index == 17:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Little finger: 2nd joint
        if index == 18:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Little finger: 1st joint
        if index == 19:
            cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)

        # Little finger: fingertip
        if index == 20:
            cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 0), -1)
            cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image

def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv2.circle(image, (point[0], point[1]), 1 + int(index / 2),
                                   (152, 251, 152), 2)

    return image

