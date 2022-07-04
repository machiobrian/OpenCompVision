#here we will add, filter functions
import cv2 as cv
import numpy as np
from paramiko import Channel
import utils


def strokeEdges(src, dst, blurKsize=7, edgeKsize=5):
    if blurKsize >= 3:
        blurredSrc = cv.medianBlur(src, blurKsize)
        graySrc=cv.cvtColor(blurredSrc, cv.COLOR_BGR2GRAY)
    else:
        graySrc = cv.cvtColor(blurredSrc, cv.COLOR_BGR2GRAY)
    cv.Laplacian(graySrc, cv.CV_8U, graySrc, ksize=edgeKsize)
    normalizedInverseAlpha = (1.0/255) * (255-graySrc)
    channels = cv.split(src)
    for channel in channels:
        channels[:] = channel * normalizedInverseAlpha
    cv.merge(channels, dst)


class VConvolutionFilter(object):
    """a filter that applies a convolution to V or all of BGR"""
    def __init__(self, kernel):
        self._kernel = kernel
    def apply(self, src, dst):
        """Apply filter with a BGR or gray source and destination"""
        cv.filter2D(src, -1, self._kernel, dst)

class SharpenFilter(VConvolutionFilter):
    """A sharpen filter with a 1-pixel radius"""
    def __init__(self):
        kernel = np.array([[-1, -1, -1],
                            [-1, 9, -1],
                            [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)
        #note: the weights sum up to 1 -> leaves the overall brightness unchanged
        """having a weight sum of 0, the edge detection kernel will turn the edges 
        white and no-edges black"""