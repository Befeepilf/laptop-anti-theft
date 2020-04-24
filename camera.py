#!/usr/bin/env python3

import sys
from google.cloud import storage
from google.cloud import firestore
import numpy as np
import cv2
import time
from multiprocessing import Process, Queue

BUCKET_URL = 'your-bucket-url.appspot.com'
SNAPSHOTS_PATH = 'AntiTheft/snapshots/'

def runCamera(queue):
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(-1)
    if(vc.isOpened()):
        success, frame = vc.read()
    else:
        success = False

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while success:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces):
            queue.put(np.copy(frame))

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('preview', frame)

        # exit on ESC
        if cv2.waitKey(20) == 27:
            break
        success, frame = vc.read()

    vc.release()
    cv2.destroyWindow('preview')


def saveFrame(frame):
    sys.stdout.write("saving frame...")
    blob = storage.Blob('{}{}.jpg'.format(SNAPSHOTS_PATH, time.time()), bucket)
    blob.upload_from_string(cv2.imencode('.jpg', frame)[1].tostring(), 'image/jpeg')
    firestore_client.collection('T430').add({
        'type': 'img',
        'url': blob.path,
        'timestamp': {'.sv': 'timestamp'}
    })
    sys.stdout.write(" done!\n")


storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_URL)
firestore_client = firestore.Client()

q = Queue()
p = Process(target=runCamera, args=(q,))
p.start()
while p.is_alive():
    if not q.empty():
        pass
        saveFrame(q.get())
