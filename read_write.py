import numpy as np
import cv2 as cv

img = np.zeros((3,3), dtype=np.uint8)
img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

img1 = cv.imread('test.jpg',cv.IMREAD_GRAYSCALE)
#cv.imshow('window',img1)

print(img1.shape)
#the .shape returns the properties of the image
#print(img)