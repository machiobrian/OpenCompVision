
########################################################################################

                #Loads all cascades into a dictionary

import argparse #used for command line arguments
import os
import cv2 as cv

#step in loading all our haarcascades.

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascades", type=str, default="cascades",
                help="path containing haar cascades")
args = vars(ap.parse_args())  #vars() -> takes an object as a parameter 
#the object may b a module, class nstance or any object with a __dict__ attribute          
# --cascade points us to the directory with the xml files#########IMPORTANT
# A dictionary strores attributes of an object. therefore, we initialize a dictionary 
# that maps the name of the haar cascade into their function
# 

detector_paths = {
    "face" : "haarcascade_frontalface_default.xml",
    "eyes" : "haarcascade_eye.xml"
}   #"name" : "path" 

#map the values to keys

detectors = {} #initialize an empty dictionary to store our cascadess, once loaded

#loop over our detector paths.
for (name, path) in detector_paths.items():
    #build a full file path and load haarcascade from disk, and store in the 
    #initialized empty dictionary
    path = os.path.sep.join([args["cascades"], path])
    detectors[name] = cv.CascadeClassifier(path)

########################################################################################

cap = cv.VideoCapture(0)

while True:
    _,img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    img_scaled = detectors["eyes"].detectMultiScale(gray, 1.3, 2)
    img1_scaled = detectors["face"].detectMultiScale(gray, 1.3, 2)

    for (x,y,w,h) in img1_scaled:
            face_rect = cv.rectangle(img, (x,y),(x+w,y+h),(0,23,256),2)
            print("eyes detected")
    for (x,y,w,h) in img_scaled:
            eyes_rect = cv.rectangle(img, (x,y),(x+w,y+h),(0,23,256),2)            
            print("face detected")

    cv.imshow("img", img)
    key = cv.waitKey(30)
    if key == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        break                                      
