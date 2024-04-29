# import libraries
import cv2
import mediapipe as mp
import threading
import pyautogui
from CONFIG import *

pyautogui.FAILSAFE = False

# use camera
cap = cv2.VideoCapture(0)
# edit the camera's sizes
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_size[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_size[1])

# load the Hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# variables
left_d_min = int((cap_size[0]-mouse_size[0])/2)
left_d_max = int(left_d_min+mouse_size[0])
cc = (0, 0)
click = False
v = round(user_size[0]/mouse_size[0], 2)
isAlive = True

def mouse(): # thread for editing mouse's position and clicking
    global cc, click
    last_val = (0, 0)
    last_click = False
    while isAlive:
        print(cc, click)
        if click:
            if not last_click:
                pyautogui.click()
                last_click = click
        else:
            last_click = False

        if cc != (0, 0) and cc != last_val and cc[0] <= user_size[0] and cc[1] <= user_size[1]:
            pyautogui.moveTo(cc[0], cc[1])
            last_val = cc

def camera(): # thread for viewing with a camera
    global cc, click, isAlive
    while isAlive:
        x, y = 0, 0
        suc, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if suc:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(frame_bgr)
            cv2.rectangle(frame, (left_d_min, 0), (left_d_max, mouse_size[1]), (255, 0, 0), 3)

            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    x_val, y_val = hand_landmarks.landmark[8].x * cap_size[0], hand_landmarks.landmark[8].y * cap_size[1]

                    cv2.circle(frame, (int(x_val), int(y_val)), 20, (0, 0, 255), 2)
                    click = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y

                    if not x_val > left_d_min - 10:
                        x = 0
                    elif not x_val < left_d_max+10:
                        x = user_size[0]
                    else:
                        x = (x_val - left_d_min) * v

                    if not y_val < mouse_size[1]+10:
                        y = user_size[1]
                    else:
                        y = y_val*v

                    cc = (x, y)

        cv2.imshow('vouse v1.0.0', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            isAlive = False
    cap.release()
    cv2.destroyAllWindows()

# create, start and wait for ending with threads
camTH = threading.Thread(target=camera, args=())
mouseTH = threading.Thread(target=mouse, args=())

camTH.start()
mouseTH.start()

camTH.join()
mouseTH.join()