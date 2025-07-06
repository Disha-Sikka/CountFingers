import cv2
import time
import handtrackingmodule as htm
cap=cv2.VideoCapture(0)

ptime=0

detector = htm.handDetector(detection_confidence=0.8,tracking_confidence=0.8)
while True:
    success, vid= cap.read()
    vid=detector.detectHands(vid)
    lms=detector.findPosition(vid, draw=False)
    tips=[4,8,12,16,20]
    count=[]
    cv2.rectangle(vid, (20, 400), (200, 150), (0, 255, 0), cv2.FILLED)
    cv2.putText(vid, 'Fingers Open: ', (30,180), cv2.FONT_HERSHEY_PLAIN
                , 1.3, (255,0,0), 2)
    if len(lms)>0:
        if lms[0][1]<lms[2][1]:
            if lms[4][1]<lms[3][1] and lms[4][1]<lms[2][1]:
                count.append(0)
            else:
                count.append(1)
        elif lms[0][1]>lms[2][1]:
            if lms[4][1]>lms[3][1] and lms[4][1]>lms[2][1]:
                count.append(0)
            else:
                count.append(1)

        for ids in range(1,5):
           if lms[tips[ids]][2]>lms[tips[ids]-2][2]:
               count.append(0)
           else:
               count.append(1)

        cv2.putText(vid, str(sum(count)), (55,350), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 8)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(vid, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)


    cv2.imshow('Video', vid)
    cv2.waitKey(1)