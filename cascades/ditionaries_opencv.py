"""implementing OpenCV Haar Cascade objects detection
- face, mouth, eyes"""

from imutils.video import VideoStream #access webcam
import argparse #for command line arguments
import imutils # for opencv convinience functions
import time #for sleep statements
import os # for building path files
import cv2 as cv

#############################################################################################################
# PART 1

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascades", type=str, default="cascades", 
                help="path to input directory containing haar cascades")
                # --cascades point to the directory containing our pre-trained
                # face, eye, mouth
args = vars(ap.parse_args())      

#load each of these Haar cascades from disk
#initialize a ditionary that maps the name of the haar cascades to their function

detectorPaths = {
    "face" : "haarcascade_frontalface_default.xml",
    "eyes" : "haarcascade_eye.xml",
    "stop" : "stop_cascade.xml"
} #defines a dictionary that maps, the name of the detector[key] to its corresponding
#file path[value].

#initialize a dictionary to store our haar cascade detctors
detectors = {} #will have the same key as detector_path (face, eyes, stop) but the value
# will be the Haar cascade once it's loaded from disk via cv.CascadeClassifier...

#loop over our detector paths
for (name, path) in detectorPaths.items():
    #for each detector, build a full file path, load the haar cascade from disk,
    #  and store in the detectors dictionary
    path = os.path.sep.join([args["cascades"], path])
    detectors[name] = cv.CascadeClassifier(path)

#since all the detectors have been loaded, we proceed to accessing our video stream

#############################################################################################################

# PART 2

#initialize the video stream and allow the camera to warm up :: do a push up
vs = VideoStream(src=0).start()
#time.sleep(2.0)

#loop over frames in the video stream
while True:
    #grab the frame from video stream, resize it, convert to gray scale
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #performe face detection using the apropriate haar cascade
    faceRects = detectors["face"].detectMultiScale(
        gray, scaleFactor=1.05, minNeighbors=5, minSize=(30,30),
        flags=cv.CASCADE_SCALE_IMAGE
    ) #face is the dominant cascade.....locate any faces in the input frame

    ############################ PART 2(a)
    #loop through each face locations and apply our eye, mouth Haar Cascades:
    #loop over the face bounding boxes

    for (fX, fY, fW, fH) in faceRects:
        #extract the face ROI
        faceROI = gray[fY: fY+fH, fX:fX + fW]

        #apply eye detection to the face ROI
        eyeRect = detectors["eyes"].detectMultiScale(
            faceROI, scaleFactor=1.1, minNeighbors=10, minSize=(15,15),
            flags=cv.CASCADE_SCALE_IMAGE
        )

        #apply stop detection to the face ROI
        stopRects = detectors["stop"].detectMultiScale(
            faceROI, scaleFactor=1.1, minNeighbors=10, 
            minSize=(15,15), flags=cv.CASCADE_SCALE_IMAGE
        )
    
        ########################## PART 2(b)
        #just as we have looped over all face detections, we need to do the same for our eyes,
        # and mouth detection.

        #loop over the eye bounding boxes.
        for (eX, eY, eW, eH) in eyeRect:
            #draw the eye bounding box
            ptA = (fX+eX, fY + eY)
            ptB = (fX + eX + eW, fY + eY + eH)
            cv.rectangle(frame, ptA, ptB, (0,0,255),2)

        #loop over the stop bounding boxes
        for (sX, sY, sW, sH) in stopRects:
            #draw a bounding box over it
            ptA = (fX+sX, fY+sY)
            ptB = (fX+sX+sW, fY+sY+sH)
            cv.rectangle(frame, ptA, ptB, (25,0,0), 2)

        #finally, draw the face bounding box on the frame
        cv.rectangle(frame, (fX,fY), (fX+fW, fY+fH), (0,0,255), 2)

    #show the output of the frame
    cv.imshow("Frame", frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv.destroyAllWindows()
vs.stop()
    
