from threading import Thread
import cv2
import time
import math
import os, sys
import face_recognition
import numpy as np



class vStream:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    def __init__(self,src):
        self.capture=cv2.VideoCapture(src)
        self.thread=Thread(target=self.update, args=())
        self.thread.daemon=True
        self.thread.start()
        self.encode_faces()
    
    def encode_faces(self):
        for image in os.listdir('./static/faces'):
            face_image = face_recognition.load_image_file(f"./static/faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names) 

    def update(self):
        
        while True:
            _,self.frame= self.capture.read()
            
            
    def getFrame(self):
        return self.frame


    def face(self):
         if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    self.face_names.append(f'{name} ({confidence})')

                self.process_current_frame = not self.process_current_frame

            # Display the results
                for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                # Create the frame with the name
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(self.frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

cam1 = vStream(0)
cam2 = vStream('rtsp://admin:Water44!@10.0.0.190:554/cam/realmonitor?channel=1&subtype=0')

while True:
    try:
        myframe1 = cam1.getFrame()
        myframe1 = cam1.face()
        myframe2 = cam2.getFrame()
        cv2.imshow('web', myframe1)
        cv2.imshow('pic', myframe2)
    except:
        print('None')
    if cv2.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)

