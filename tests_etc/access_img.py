import cv2 as cv

img = cv.imread('test.jpg')
#manipulate the top most pixel to white
#img[0,0] = [255,255,255]