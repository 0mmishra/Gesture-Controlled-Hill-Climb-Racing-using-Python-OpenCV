import cv2
import mediapipe as mp
import pyautogui  # or use keyboard module
import time

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

prev_action = None

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Detect if fist (all fingers down)
            fingers = []
            tips = [8, 12, 16, 20]
            for tip in tips:
                if lm[tip].y < lm[tip - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if fingers == [0, 0, 0, 0] and prev_action != "brake":
                pyautogui.keyDown("left")  # simulate brake
                pyautogui.keyUp("right")
                print("BRAKE")
                prev_action = "brake"
            elif fingers == [1, 1, 1, 1] and prev_action != "accelerate":
                pyautogui.keyDown("right")  # simulate gas
                pyautogui.keyUp("left")
                print("ACCELERATE")
                prev_action = "accelerate"
    else:
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        prev_action = None

    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
