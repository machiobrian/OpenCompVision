#houghlinesp - probabilistic -> detect lines and return the two end points
#houghlines - detect line and return the represetation of each line as a 
# single point and an angle w/out info of the end points

import cv2 as cv
import numpy as np

img = cv.imread('vlines.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 120)
minLineLength = 20
maxLineGap = 5
lines = cv.HoughLinesP(edges, 9, np.pi/180.0, 200,
                    minLineLength, maxLineGap)
for x1, y1, x2, y2 in lines[0]:
    cv.line(img, (x1,y1), (x2,y2), (0,255,0), 2)

cv.imshow("edges", edges)
cv.imshow("lines", img)                    
#cv.imshow('lines', gray)
cv.waitKey(0)
cv.destroyWindow()