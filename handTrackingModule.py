import cv2 
import mediapipe as mp  
import time  


class handDetector():
    
    def __init__(self,mode=False,maxHands = 2, detectionCon = 0.5, trackCon=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
        static_image_mode=self.mode,
        max_num_hands=self.maxHands,
        min_detection_confidence=self.detectionCon,
        min_tracking_confidence=self.trackCon
    )


        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img, draw=True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect hands in the RGB image
        self.results = self.hands.process(imgRGB)
        
        # print(results.multi_hand_landmarks)    
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Custom drawing specs (red dots, green lines)
                    landmark_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(
                        color=(0, 0, 255),  # Red (BGR)
                        thickness=2,
                        circle_radius=1
                    )
                    connection_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(
                        color=(0, 255, 0),  # Green (BGR)
                        thickness=2,
                        circle_radius=1
                    )
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS,
                        landmark_drawing_spec=landmark_drawing_spec,
                        connection_drawing_spec=connection_drawing_spec
                    )
        return img     
    
    def  findPosition(self, img, handNo=0, draw=False):
        
        lmList = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
        
            for id, lm in enumerate(myHand.landmark):
                        # print(id,lm)
                        h,w,c = img.shape
                        cx,cy = int(lm.x*w), int(lm.y*h)
                        # print(id,cx,cy)
                        lmList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img,(cx,cy),25,(0,255,0),cv2.FILLED)   
    
    
        return lmList
    
    
    
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()    #OBJECT NAMED DETECTOR CREATER, AND EFAULT PARAMETERS GET PASSED AUTOMATICALLY
    
    while True:
        
        success, img = cap.read()  # success=True if frame captured, img=frame data
        img = detector.findHands(img)    #findHands IS THE METHOD WITHIN CLASS handDetector OF WHICH detector IS OBJECT
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),(3))
        
        # Show the webcam image in a window called "image"
        cv2.imshow("image", img)
        
        # Check if 'q' key is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__=="__main__":
    main()
