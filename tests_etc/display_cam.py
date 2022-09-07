from pydoc import cli
import click
import cv2 as cv

clicked = False

def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv.EVENT_LBUTTONUP:
        clicked = True

cameraCapture = cv.VideoCapture(0)
cv.namedWindow('myWindow')
cv.setMouseCallback('myWindow', onMouse)

print('Showing Camera Feed. Click Window or any key to Stop')
success, frame = cameraCapture.read()
while success and cv.waitKey(1) == -1 and not clicked:
    cv.imshow('myWindow', frame)
    success, frame = cameraCapture.read()
cv.destroyWindow('myWindow')
cameraCapture.release()