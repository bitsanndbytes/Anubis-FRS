from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

#defining prototext and caffemodel paths
caffeModel = "res10_300x300_ssd_iter_140000.caffemodel"
prototextPath = "deploy_prototxt.txt"

#Load Model
print("Loading model...................")
net = cv2.dnn.readNetFromCaffe(prototextPath,caffeModel)

# initialize the video stream to get the video frames
print("[INFO] starting video stream...")
vs = VideoStream(src='').start()
time.sleep(2.0)

while True :
    #Get the frams from the video stream and resize to 400 px
    frame = vs.read()
    frame = imutils.resize(frame,width=800)
    location = detector.detect_faces(frame)
    if len(location) > 0:
            for face in location:
                x, y, width, height = face['box']
                x2, y2 = x + width, y + height
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 4)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
