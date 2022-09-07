import os #module provides functions of interacting with the OS
import cv2 as cv

#declare a face_cascade variable that loads a cascade for face detection
#the variable is a cascade classifier object 
face_cascade = cv.CascadeClassifier(
    './cascades/haarcascade_frontalface_default.xml'
)
#CascadeClassifier expects a grayscale image
img = cv.imread('faces.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#Performe the actual face detection 
faces = face_cascade.detectMultiScale(gray, 1.08, 5)
#1.08 - is a scaling factor, >1.0 determines the downscaling ratio of the image at each 
#iteration ->  downscaling, is to achieve scale invariance by matching various faces to 
#window size
#5 - minNeighbor, the min number of overlapping detections that are required inorder to 
#retain a detection result -> the higher the number of overlapping detections, the more 
#certain we are that it is a face that has been detected
"""" the value returned from face detection, is a list of tuples representing the face
rectangles.  """


for(x,y,w,h) in faces:
    img = cv.rectangle(img, (x,y), (x+w, y+h), (255,250,0), 2) #the rectangle fxn allows 
    #us to draw rectanles at the specified coordinate

#cv.namedWindow('Faces Detected')
cv.imshow('Window', img)
cv.imwrite('faces.jpg', img)
cv.waitKey(0)

