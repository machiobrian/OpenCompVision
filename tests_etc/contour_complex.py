import cv2 as cv
import numpy as np


img = cv.pyrDown(cv.imread("test.jpg", cv.IMREAD_UNCHANGED))

ret, thresh = cv.threshold(cv.cvtColor(img, cv.COLOR_BGR2GRAY), 127, 255,
                                        cv.THRESH_BINARY)
contours, heir = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#for each contour, find and draw the bounding box, min. enclosing rect/circle
for c in contours:
    #find the bounding box coordinates
    x,y,w,h = cv.boundingRect(c) #calculate a simple bounding box
    cv.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2) #draw the rectangle
    #find the min. area rectangle enclosing the subject 
    rect = cv.minAreaRect(c)
    #calculate the coordinates of the min area rect - calculation is in floating point
    box = cv.boxPoints(rect)
    #normalize the coordinates to integers - convert to integers, pixels are in int
    box = np.int0(box)
    #draw the contours - in integer form using Opencv
    cv.drawContours(img, [box], 0, (0,0,255), 3)

    #calculat ethe center and radius of te min enclosing circle
    (x,y), radius = cv.minEnclosingCircle(c)
    #cast to integers
    center = (int(x), int(y))
    radius = int(radius)

    #draw the circle
    img = cv.circle(img, center, radius, (0,255,0), 2)

cv.drawContours(img, contours, -1, (255,0,0), 1)
cv.imshow("contours", img)




#cv.imshow('new', img)
cv.waitKey(0)
cv.destroyWindow()