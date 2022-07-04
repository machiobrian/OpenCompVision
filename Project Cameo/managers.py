from configparser import NoOptionError
from fileinput import filename
import cv2 as cv
import numpy as np
import time


class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None,
                shouldMirrorPreview = False):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFileName = None
        self._videoEncoding = None
        self._videoWriter = None
        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    #setter and getter methods for the CaptureMethod properties
    @property #getter
    def channel(self):
        return self._channel
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None
    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
                self._frame, self._channel
            )
        return self._frame
    @property
    def isWritingImage(self):
        return self._imageFileName is not None
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

#most members are non-public -> underscore e.g. in self._enteredFrame
#single underscore -> the variable should be accessed only within its class and 
#not its subclass

    #the enterFrame method

    #only grabs a frame, the actual reading is postponed to a subsequent reading
    #of the frame variable
    def enterFrame(self):
        """Capture the next Frame, if any"""
        #first confirm the previous frame was exited
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching, exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()
            #grab / synchronizes a frame

    #the exit frame method -> takes image from the current channel,estimates the frame rates
    #shows the image via the windows managwe(if any) and fulfills any pending request to 
    #write the image to files

    def exitFrame(self):
        """Draw to Windows/ Write to files, then release the frame"""

        #check whether any grabbed frame is retrievable
        #the getter may retrieve and cache the frame
        if self.frame is None:
            self._enteredFrame = False
            return
        
        #Update the FPS estimate and related variables
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        #Draw to the Window, if any.
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = np.fliplr(self._frame)
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        #Draw to the image file if any
        if self.isWritingImage:
            cv.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        #write to video file if any
        self._writeVideoFrame() #calling of a helper method -> to be defined later

        #Release VideoFrame
        self._frame = None
        self._enteredFrame = False

    #other file writing methods
    #updates the parameters fro file writing operations, the actual writing operations
    # are postponed to the next call of exit frame
    def writeImage(self, filename):
        """Write the next edited farme to an image file"""
        self._imageFileName = filename
    def startWritingVideo(
        self, filename, 
        encoding = cv.VideoWriter_fourcc('M','J','P','G')):
        '''start writing exited frames to a video file'''
        self._videoFileName = filename
        self._videoEncoding = encoding
    def stopWritingVideo(self):
        """Stop writing exited frames to a video file"""
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

    #later -> create/append 
    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv.CAP_PROP_FPS)
            if fps <= 0.0:
                #since the capture estimate is unknown use an estimate
                if self._framesElapsed < 20:
                    #wait unit more frames elapse so that the
                    #estimate is more stable -> that is, if frame rate is unknown, skip
                    #some frames at the start to allow build up of estimates of frame rate
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(
                        cv.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                        cv.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv.VideoWriter(
                self._videoFileName, self._videoEncoding,
                fps, size)
        self._videoWriter.write(self._frame)

class WindowManager(object): #comes in place of Opencv funtions of window creation that
    #is not object-oriented
    #only for keyboard events
    def __init__(self, windowName, keyPressCallback = None):
        self.keypressCallback = keyPressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    #methods to manage te life cycle of the window and its events
    @property
    def isWindowCreated(self):
        return self._isWindowCreated
    def createWindow(self):
        cv.namedWindow(self._windowName)
        self._isWindowCreated = True
    def show(self, frame):
        cv.imshow(self._windowName, frame)
    def destroyWindow(self):
        cv.destroyWindow(self._windowName)
        self._isWindowCreated = False
    def processEvents(self):
        keycode = cv.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            self.keypressCallback(keycode)