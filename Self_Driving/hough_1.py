#line detection 

import cv2 as cv
import numpy as np
 
 #read the required image in which operations is to be 
 # performed
img = cv.imread('/home/machio_b/Documents/Python/OpenCV_4/Self_Driving/road.jpg')

#conver the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#image = cv.imshow("gray",gray)

#do some edge detection on the image
edges = cv.Canny(gray, 400,600, apertureSize=3)
#image = cv.imshow("edges", edges)

#return an array of r and theta values
lines = cv.HoughLines(edges, 1, np.pi/180, 200)
# for i in lines:
#     print(lines)

#create a looping fuction that runs till rho and theta values are 
# in the range of the 2d array

for r_theta in lines:
    arr = np.array(r_theta[0], dtype=np.float64)
    r, theta = arr
    #print(r, theta)

    #store the value of cos theta and sin theta
    a = np.cos(theta)
    b = np.sin(theta)
    print(a,b)
    #store values rcos theta and  rsin theta 
    x0 = r*a
    y0 = r*b
    print(x0, y0)
    #store the rounded off values of (rcos/sin(theta)+/-1000sin/cos(theta))
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))

    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    print((x1,y1), (x2,y2))

    #draw a line in img from the points (x1,y1) and (x2,y2)
    cv.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
    

cv.waitKey(0)
cv.imwrite('linedetected.jpg', img)