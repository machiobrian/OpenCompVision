from turtle import color
import cv2 as cv
import numpy as np

img = np.zeros((200,200), dtype=np.uint8) #create an empty blvck img
img [50:150, 50:150] = 255 #place a white square in it,
            #ability of an array to assign values to a slice

ret, thresh = cv.threshold(img, 127, 255, 0) #threshold the image
contours, heirachy = cv.findContours(thresh, cv.RETR_TREE,
        cv.CHAIN_APPROX_SIMPLE)

color = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
img = cv.drawContours(color, contours, -1, (0,255,0), 2)
cv.imshow("contours", color)
#cv.imshow("color", img)


cv.waitKey(0)
cv.destroyAllWindows()