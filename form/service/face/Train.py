import cv2 
import numpy as np
from PIL import Image
import os
from form.settings import *
path = PATH_DATASET
recognizer = cv2.face.LBPHFaceRecognizer.create()
face_detector = cv2.CascadeClassifier(PATH_XML)
def getImagesAndLabels(path):
    imagePath = [os.path.join(path,f) for f in os.listdir(path)  if f != ".gitkeep"]
    faceSamples = []
    ids = []
    for imagePath in imagePath:
        PIL_img = Image.open(imagePath).convert("L")
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = face_detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

def training():
    face,ids = getImagesAndLabels(path)
    recognizer.train(face,np.array(ids))
    recognizer.write(PATH_TRAINER)
