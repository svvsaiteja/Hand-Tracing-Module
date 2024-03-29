import cv2
import mediapipe as mp
import time
import HandTracking as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1080, 640


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0
detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()


minVolume = volumeRange[0]
maxVolume = volumeRange[1]
vol = 0
volBar = 400
volPercent = 0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 153, 51), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 153, 51), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 153, 51), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 153, 51), 3)

        length = math.hypot(x2-x1, y2-y1)

        vol = np.interp(length, [30, 300], [minVolume, maxVolume])
        volBar = np.interp(length, [30, 300], [400, 150])
        volPercent = np.interp(length, [30, 300], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (200,200,200), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400),
                      (200,200,200), cv2.FILLED)
        cv2.putText(img, f'{int(volPercent)} %', (10, 80), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (200,200,200), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                (200,200,200), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
