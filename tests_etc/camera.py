#capture cam frames -> write to an AVI file

import cv2 as cv
from cv2 import VideoWriter
cameraCapture = cv.VideoCapture(0) #device index
fps = 30 #an assumption
size = (int(cameraCapture.get(cv.CAP_PROP_FRAME_WIDTH)),
        int(cameraCapture.get(cv.CAP_PROP_FRAME_WIDTH)))
VideoWriter = cv.VideoWriter(
    'myOutPut.avi', cv.VideoWriter_fourcc('I','4','2','0'),
    fps, size)

success, frame = cameraCapture.read()
numFramesRemaining = 10*fps-1 #10 secs of frames
while success and numFramesRemaining > 0:
    VideoWriter.write(frame)
    success, frame = cameraCapture.read()
    numFramesRemaining -=1