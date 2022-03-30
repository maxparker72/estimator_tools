import cv2 as cv
import numpy as np

im = cv.imread('MS1-111-MW-A03.jpg')
imgray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshhold(imgray, 127,255,0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(im, contours, -1, (0,255,0), 3)
cv.imshow(im)

