import cv2
import mediapipe as mp
import pyautogui
import time
import math

mp_hands = mp.solutions.hands
mp_drawing= mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

#gesture time control
click_start_time=None
click_times=[]
click_cooldown=0.5
scroll_mode=False
freeze_cursor=False
screenshot_cooldown=2
last_screenshot_time=0

screen_w,screen_h = pyautogui.size()
print("\n hand mouse control.")
prev_screen_x, prev_screen_y = 0,0

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

        #get finger tips
        thumb_tip=hand_landmarks.landmark[4]
        index_tip=hand_landmarks.landmark[8]
        middle_tip=hand_landmarks.landmark[12]
        ring_tip=hand_landmarks.landmark[16]

        fingers=[
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0 
            for tip in [8, 12, 16, 20]
        ]

        #distance between thumb 
        dist=math.hypot(thumb_tip.x-index_tip.x, thumb_tip.y-index_tip.y)
        if dist<0.06:
            if not freeze_cursor:
                freeze_cursor=True
                click_times.append(time.time())

                # double click check
                if len(click_times)>=2 and click_times[-1]-click_times[-2]<0.4:
                    pyautogui.doubleClick()
                    cv2.putText(frame, "Double Click", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
                    click_times=[]
                # single click
                else:
                    pyautogui.click()
                    cv2.putText(frame, "Single Click", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        else:
            if freeze_cursor:
                time.sleep(0.1)
            freeze_cursor=False 

        # move cursor wrt index finger
        if not freeze_cursor:
            screen_x = int(index_tip.x * screen_w)
            screen_y = int(index_tip.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y, duration=0.05)
            prev_screen_x, prev_screen_y = screen_x, screen_y

        # Scrolling
        if sum(fingers)==4:
            scroll_mode=True
        else:
            scroll_mode=False

        if scroll_mode:
            if index_tip.y<0.4:
                pyautogui.scroll(120)
                cv2.putText(frame, "Scroll Up", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif index_tip.y>0.6:
                pyautogui.scroll(-120)
                cv2.putText(frame, "Scroll Down", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        
        #ScreenShot
        if(sum(fingers) == 0):
            current_time=time.time()
            if current_time-last_screenshot_time>screenshot_cooldown:
                pyautogui.screenshot(f"screenshots/screenshot_{int(current_time)}.png")
                cv2.putText(frame, "ScreenShot Taken!", (10,130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
                last_screenshot_time=current_time


            

            


    cv2.imshow("live video", frame) 

    if cv2.waitKey(1)==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

