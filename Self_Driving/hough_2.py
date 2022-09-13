import cv2 as cv
import numpy as np

#read image
image = cv.imread('/home/machio_b/Documents/Python/OpenCV_4/Self_Driving/road.jpg')

#convert image to gray scale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)
cv.imshow("gr", blurred)
#get the edges: canny edge detection
edges = cv.Canny(blurred, 400, 600, apertureSize=3)
cv.imshow("edges", blurred)

#use HoughLinesP method to directly obtain line and end points
lines_list = [] #create an empty list to store the lines

lines = cv.HoughLinesP(
    edges, #input the edge image
    1, #distance resoulution in pixels
    np.pi/180, #angle resolution in radians
    threshold=100, #min number of votes required for a valid line
    minLineLength=5, #minimum allowed length of line
    maxLineGap=10 #max allowed gap btn length of lines for joining them
)

#iterate over the points
for points in lines:
    #extract the points nested in the list
    x1,x2,y1,y2 = points[0]
    #draw the lines joining the points on the original image
    cv.line(image, (x1,y1), (x2,y2), (0,255,0), 2)
    #maintain a look up list for points
    lines_list.append([(x1,y1), (x2,y2)])

#save rge result image
cv.imwrite('halfp.png', image)

cv.waitKey(0)