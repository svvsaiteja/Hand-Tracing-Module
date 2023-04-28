import cv2
import pyautogui
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils



while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h,w,c = img.shape
            index_y8 = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*w
            index_y6 = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*w
            middle_y8 = handLms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*w
            middle_y6 = handLms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*w
            
            
            if(index_y8<index_y6 or  middle_y8<middle_y6):
                print(1)
                
                
                
            mp_drawing.draw_landmarks(img,handLms,mp_hands.HAND_CONNECTIONS)

    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
