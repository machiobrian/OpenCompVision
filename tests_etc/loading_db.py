import os
import cv2 as cv
import numpy as np

#create a function to read images
#goes through a directory, subdir, loads images, resizes them and puts 
#the resized images in a list
"""builds 2 lists, a list of peoples names and initials based on subfolder name
, a list of labels or numeric IDs associated with loaded images"""

def read_images(path, image_size):
    names = []
    training_images, training_labels = [], [] #
    label = 0

    for dirname, subdirnames, filesnames in os.walk(path):
        for subdirname in subdirnames:
            names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)

            for filename in os.listdir(subject_path):
                img = cv.imread(os.path.join(subject_path, filename),
                cv.IMREAD_GRAYSCALE)

                if img is None:
                    continue #if file cannot be loaded as an image skip
                
                img = cv.resize(img, image_size)
                training_images.append(img)
                training_labels.append(label)
            label += 1

    training_images = np.asarray(training_images, np.uint8)
    training_labels = np.asarray(training_labels, np.uint32)
    return names, training_images, training_labels

#Calling the read_image function
path_to_training_images = './face_db/yaleB11'
training_image_size = (200, 200)
names, training_images, training_labels = read_images(path_to_training_images,
                                                     training_image_size)
#with the array of training images, and an array of their labels
#create and train a face recognizer by passing the image arrays and labek array

model  = cv.face.EigenFaceRecognizer_create()
model.train(training_images, training_labels)

#initialize a face detector
face_cascade = cv.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

#initialize a camera feed, iterates over the frames, performe face detection/recognition

camera = cv.VideoCapture(0)
while (cv.waitKey(1) == -1):
    success, frame = camera.read()
    if success:
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),1)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            roi_gray = gray[x:x+w, y:y+h]
            if roi_gray.size == 0:
                #ROI is empty. the face may be at the edge therefore, skip it
                continue
            roi_gray = cv.resize(roi_gray, training_image_size)
            label, confidence = model.predict(roi_gray)
            text = '%s, confidence=%.2f' % (names[label], confidence)
            cv.putText(frame, text, (x, y - 20),
            cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv.imshow('Face Recognition', frame)