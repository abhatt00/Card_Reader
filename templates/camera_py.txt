from time import time
import cv2
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.window = cv2.namedWindow("test")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while(self.video.isOpened()):
            try: 
                # Capture frame-by-frame
                cv2.waitKey(2)
                ret, frame = self.video.read()
                #convert frame into gray color
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #noise reducing to find card
                gray = cv2.bilateralFilter(gray,11,17,17)
                edge = cv2.Canny(gray,30,200)
                contours,hier = cv2.findContours(edge.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                contour = sorted(contours,key=cv2.contourArea, reverse=True)[1]
                if(contours):
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    areaContour = cv2.contourArea(contour)
                    areaBox = cv2.contourArea(box)
                    if(areaBox>0):
                        valid = areaContour/areaBox>0.95
                        cv2.drawContours(frame, contours, 0, (0,255,0), 3)
                if ret == True:
                
                    # Display the resulting frame
                    cv2.imshow('Frame',frame)
                    ret, jpeg = cv2.imencode('.jpg',frame)
                    return jpeg.tobytes()
                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            except: 
                print("Something went wrong")
                
            
            # Break the loop
            else: 
                break
            
        