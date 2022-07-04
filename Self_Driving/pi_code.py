
from cv2 import threshold
"""Importing the Necessary Libs for Opencv and Pi"""

from PiCamera.array import PiRGBArray
import RPi.GPIO as GPIO #control the motors
from picamera import PiCamera #interface the camera attached to the Pi
import time # introduce delays
import cv2 as cv #used for image Processing
import numpy as np
import math

"""Declare some variables and some GPIO"""

GPIO.setmode(GPIO.BCM) #sets the mode to be used, board is numbered according to 
#the mapping of pins - and BCM fro GPIOs as they are

#declaring functions of the GPIOs
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

#setting all pins to low during startup - refer to schematic for mapping
GPIO.outputs(5,GPIO.LOW)
GPIO.outputs(12,GPIO.LOW)
GPIO.outputs(19,GPIO.LOW)
GPIO.outputs(13,GPIO.LOW)

# Variables to store data about track and rotation
theta = 0
minLineLength = 5
maxLineGap = 10

"""Use the PiCam and link it to variables and performe startup commands"""
camera = PiCamera
camera.resolution = (640, 480) #reduce the video recording resolution
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

"""Program Logic 1 - Get me the Lanes"""

#open a loop to continuously take input from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
    
    #after first iteration, set all the GPIO LOW
    GPIO.outputs(5,GPIO.LOW)
    GPIO.outputs(12,GPIO.LOW)
    GPIO.outputs(19,GPIO.LOW)
    GPIO.outputs(13,GPIO.LOW)

    time.sleep(0.0)
    image  = frame.array #converts th eimages into an array form
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #convert image to grayscale
    blurred = cv.GaussianBlur(gray, (5,5), 0) #smoothens the image
    edged = cv.Canny(blurred, 85,85) #bring out boarders out of the images
    lines = cv.HoughLinesP(edged, 1, np.pi/180, 10, minLineLength, maxLineGap) #to identify 
    #shapes and lines


# """Program Logic 2 - Turn Decision"""
# after drawing the lines, ew map out the distances as vectors and measure their 
# angles from horizontal
    if(lines != []):
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv.line(image, (x1,y1), (x2,y2),(0,255,0), 2)
                theta = theta+math.atan2((y2-y1),(x2-x1)) #add the measured angles and predict 
                #the path of the lane
    
#with the data at hand, let us control the robot
    threshold = 6

    if(theta>threshold):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        print("left")
       
    if(theta<-threshold):
        GPIO.output(12, GPIO.LOW)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)
        print("right")

    if(abs(theta)<threshold):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)
        print ("straight")

    theta=0
    cv.imshow("Frame",image)
    key = cv.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break


