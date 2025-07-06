import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode=mode
        self.max_hands=max_hands
        self.model_complexity=model_complexity
        self.detection_confidence=detection_confidence
        self.tracking_confidence=tracking_confidence
        self.mpHands = mp.solutions.hands
        self.Hands = self.mpHands.Hands(self.mode, self.max_hands, self.model_complexity,
                                        self.detection_confidence, self.tracking_confidence)
        self.mpDraw= mp.solutions.drawing_utils


    def detectHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.Hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handlm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handlm, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handno=0, draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand= self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    if id == 4 or id == 8:
                        cv2.circle(img, (cx, cy), 10, (255, 255, 0), 3)

        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    cTime = 0
    pTime = 0
    detector=handDetector()
    while True:
        success, img = cap.read()
        img= detector.detectHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (15, 80), cv2.FONT_ITALIC, 2, (255, 0, 255), 3)

        cv2.imshow('image', img)
        cv2.waitKey(1)

if __name__=='__main__':
    main()