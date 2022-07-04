import cv2 as cv
from managers import WindowManager, CaptureManager

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo',self.onKeypress)
        self._captureManager = CaptureManager(
            cv.VideoCapture(0), self._windowManager, True
        )
    #the run method
    def run(self):
        """Run the Main Loop"""
        self._windowManager.createWindow()
        while self._windowManager._isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # TODO: Filter the frame  (chapter 3)
                pass
            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    
    #the onkeypress method
    def onKeypress(self, keycode):
        """
        Handles a key press
        space -> Take a screenshot.
        tab -> Start/stop recording a screencast.
        escape -> Quit.
        """

        if keycode == 32: #space
            self._captureManager.writeImage('Screenshot.png')
        elif keycode == 9: #tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
                    'screencast.avi'
                )
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: #escape
            self._windowManager.destroyWindow()

#instantiating the main block that runs cameo;
if __name__ == "__main__":
    Cameo().run()
