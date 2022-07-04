import cv2 as cv
from cv2 import ml_ANN_MLP
import numpy as np

ann = cv.ml.ANN_MLP_create() #crate an untrained ANN
ann.setLayerSizes(np.array([9,15,9], np.uint8))
#first element - size of the input layer
#15 - single hidden layer w/15 nodes
#9 - output layer, 9 nodes

ann.setActivationFunction(cv.ml.ANN_MLP_SIGMOID_SYM, 0.6, 1.0) #configure the activation function
#symmetrical sigmoid activation function
ann.setTrainMethod(cv.ml.ANN_MLP_BACKPROP, 0.1, 0.1) # the training method, backpropagation
ann.setTermCriteria((
    cv.TermCriteria_MAX_ITER | cv.TermCriteria_EPS, 100, 1.0
))

#Training our ANN

#set the inputs / samples its of class 5
training_samples = np.array(
    [[1.2, 1.3, 1.9, 2.2, 2.3, 2.9, 3.0, 3.2, 3.3]],
    np.float32
)
layout = cv.ml.ROW_SAMPLE
#set the outputs/ responses
training_responses = np.array(
    [[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]],
    np.float32
)

data = cv.ml.TrainData_create(
    training_samples, layout, training_responses
)

ann.train(data)

test_samples = np.array(
    [[1.4, 1.5, 1.2, 2.0, 2.5, 2.8, 3.0, 3.1, 3.8]],
    np.float32
)
prediction = ann.predict(test_samples)
print(prediction) #output is a tuple, the first value is the class while the 
#last is the list of arrays

