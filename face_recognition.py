#we are to generate data for face recognition .. revisit

import cv2 as cv
import os

output_folder = './bm'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

faces_cascade = cv.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('./haarcascade_eye.xml')

camera = cv.VideoCapture(0)
count = 0

while (cv.waitKey(1)==-1):
    success, frame = camera.read()
    if success:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #face detect
        faces = faces_cascade.detectMultiScale(gray, 1.3, 5, minSize =(120,120))
        #no face smaller than 120 by 120 will be detected => we are sitting near the camera
        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 2)
            face_img = cv.resize(gray[y:y+h, x:x+w], (200,200))
            face_filename = '%s/%d.pgm' % (output_folder, count)
            cv.imwrite(face_filename, face_img)
            count =+ 1
        cv.imshow('Capturing Faces....', frame)