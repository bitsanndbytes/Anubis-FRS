import os
from threading import Thread
import cv2
import face_recognition
import numpy as np
import multiprocessing


def get_encoded():
    encoded = {}

    for dirpath, dnames, fnames in os.walk(r'./static/faces'):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = face_recognition.load_image_file(r"./static/faces/" + f)
                encoding = face_recognition.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


class camstream:
    def __init__(self,src):
        # for capturing cameras
        self.capture = cv2.VideoCapture(src)
        self.thread=Thread(target=self.update, args=())
        # for Threading for all the cameras
        self.thread.daemon = True
        self.thread.start()

    def process(self):
        self.process_this_frame = True
        p1 = multiprocessing.Process(target=self.process_this_frame, args=())
        p2 = multiprocessing.Process(target=get_encoded, args=())
        p1.daemon = True
        p2.start()
        p1.start()


    def update(self):
        faces = get_encoded()
        known_face_encodings = list(faces.values())
        known_face_names = list(faces.keys())
        face_locations = []
        face_encodings = []
        face_names = []
        self.process_this_frame = True
        while True:
             _,self.frame = self.capture.read()

             if self.process_this_frame:
                small_frame = cv2.resize(self.frame, (0,0), fx=0.25, fy=0.25 )
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
             self.process_this_frame = not self.process_this_frame
             for (top, right, bottom, left), name in zip(face_locations, face_names):
                 top *= 4
                 right *= 4
                 bottom *= 4
                 left *= 4
                 
                 cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
                 cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                 font = cv2.FONT_HERSHEY_DUPLEX
                 cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    def getFrame(self):
        return self.frame




cam2 = camstream(0)

while True:
    try:
        myframe1 = cam2.getFrame()
        cv2.imshow('test', myframe1)
    except:
        print('No camera')
    if cv2.waitKey(1)==ord('q'):
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)

