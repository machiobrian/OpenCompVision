#an object with divese shape -> no two points within the shape whose
#connecting lines goes outside the perimeter of the shape.

import cv2 as cv
import numpy as np

img = cv.pyrDown(cv.imread('face2.jpg', cv.IMREAD_UNCHANGED)) #unchanged ->
            #loads an image from a file
ret, thresh = cv.threshold(cv.cvtColor(img, cv.COLOR_BGR2GRAY),
                        127, 255, cv.THRESH_BINARY) #binary -> fixed level threshold
                                                    #to each pixel 
                                                    
contours, heir = cv.findContours(thresh, cv.RETR_EXTERNAL, 
                                        cv.CHAIN_APPROX_SIMPLE)

black = np.zeros_like(img)
for cnt in contours:
    epsilon = 0.01 * cv.arcLength(cnt, True)
    approx  = cv.approxPolyDP(cnt, epsilon,True)
    hull = cv.convexHull(cnt)

    cv.drawContours(black, [cnt], -1, (0,255,0), 2)
    cv.drawContours(black, [approx], -1, (255, 255, 0), 2)
    cv.drawContours(black, [hull], -1, (0,0,255), 2)
cv.imshow("hull", black)
cv.waitKey()
cv.destroyWindow()