import cv2 as cv
from cv2 import circle
import numpy as np

planets = cv.imread('face.jpg')
gray_img = cv.cvtColor(planets, cv.COLOR_BGR2GRAY)
gray_img = cv.medianBlur(gray_img, 5)

circles = cv.HoughCircles(gray_img, cv.HOUGH_GRADIENT, 1, 120,
                param1=100, param2=30, minRadius=0, maxRadius=0)

circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    #draw the outter circle
    cv.circle(planets, (i[0],i[1]),i[2],(0,255,0),2)
    #draw the center of the circle
    cv.circle(planets, (i[0],i[1]),2,(0,0,255),3)

#cv.imwrite("planets.jpeg", planets)
cv.imshow("HoughCircles", planets)
cv.waitKey()
cv.destroyWindow()