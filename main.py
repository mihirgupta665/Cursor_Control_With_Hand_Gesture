import cv2
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
    cv2.imshow("live video", frame) 

    if cv2.waitKey(1)==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

