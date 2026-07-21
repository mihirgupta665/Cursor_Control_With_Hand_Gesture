import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing= mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannnot Open Camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't Receive Frames")
        break

    frame=cv2.flip(frame, 1)
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("live video", frame) 

    if cv2.waitKey(1)==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

