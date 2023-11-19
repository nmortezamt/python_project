# Control volume with hands detection
import cv2
import numpy as np
import math
import pyautogui

# initialize variables
cap = cv2.VideoCapture(0)
prev_vol = 0

# Define a range for skin color in HSV
lower_skin = np.array([0,20,70], dtype=np.uint8)
upper_skin = np.array([20,255,255], dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1) #Flip the frame horizontally

    # Region of interest (ROI) for detecting the hand
    roi = frame[100:300, 100:300]
    cv2.rectangle(frame, (100,100), (300,300), (0,255,0), 0)
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Extract the hand from the ROI
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the maximum area (the hand)
    if contours:
        hand_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(hand_contour)
        if M["m00"]:
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.circle(roi, (cx, cy), 5, [0,0,255], -1)
        
        distance = math.sqrt((cx - 150) ** 2 + (cy - 150) ** 2)
        volume = int(np.interp(distance, [0, 100], [0, 100]))
        
        if volume != prev_vol:
            pyautogui.press("volumeup" if volume > prev_vol else "volumedown")
            prev_vol = volume
    
    cv2.imshow("Hand Gesture Volume Control", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
