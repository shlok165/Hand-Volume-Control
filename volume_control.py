
import cv2
import mediapipe as mp
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



# Initialize camera
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Hand detector
detector = htm.handDetector(detectionCon=0.75)

# Audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()  # (-96.0, 0.0, 0.125)
minVol, maxVol = volRange[0], volRange[1]

# Smoothing parameters
smoothness = 10
vol_history = []
current_vol = volume.GetMasterVolumeLevel()

# FPS tracking
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        # Get thumb and index finger positions
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Draw landmarks and line
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        # Calculate distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)
        
        # Smooth length calculation
        if len(vol_history) > smoothness:
            vol_history.pop(0)
        vol_history.append(length)
        smooth_length = sum(vol_history) / len(vol_history)
        
        # Volume bar parameters
        bar_height = 200
        bar_width = 40
        bar_x = 50
        bar_y = 150
        
        # Map length to volume (with buffer zones)
        vol = np.interp(smooth_length, [30, 220], [minVol, maxVol])
        
        # Smooth volume transition
        current_vol = current_vol + (vol - current_vol) / 10
        volume.SetMasterVolumeLevel(current_vol, None)
        
        # Volume percentage (0-100)
        vol_per = np.interp(current_vol, [minVol, maxVol], [0, 100])
        
        # Color gradient for center circle
        color_ratio = np.interp(smooth_length, [30, 220], [0, 1])
        r = int(255 * color_ratio)
        g = int(255 * (1 - color_ratio))
        cv2.circle(img, (cx, cy), 10, (0, g, r), cv2.FILLED)
        
        # Draw volume bar
        filled_height = int(bar_height * (vol_per / 100))
        cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), 2)
        cv2.rectangle(img, (bar_x, bar_y + bar_height - filled_height), 
                     (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(vol_per)}%', (bar_x - 10, bar_y + bar_height + 30), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    
    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
