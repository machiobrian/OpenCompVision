from random import random
import cv2 as cv
import numpy as np
import os

#make an array of 120,000 random bytes
randomByteArray = bytearray(os.urandom(120000)) #generate random bytes
# convert to numpy array
flatNumpyArray = np.array(randomByteArray)

#convert the array to make 400x300 grayscale image
grayImage = flatNumpyArray.reshape(300, 400)
cv.imwrite('RandomColor.png', grayImage)

#convert the array to make a 400x300 color image
bgrImage = flatNumpyArray.reshape(400, 100, 3)
cv.imwrite('colorImage.png', bgrImage)