from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
import os

# camera = PiCamera()
# 
# camera.start_preview()
# sleep(10)
# camera.capture('/home/pi/Desktop/shm_model/yolov5/testImg/img.jpg')
# camera.stop_preview()
# camera.close()

#crop image
# img = cv2.imread('/home/pi/Desktop/shm_model/yolov5/runs/detect/exp17/botrytis (9).jpg')
# print(img.shape[0:2])
# height, width = img.shape[0:2]
# startRow = int(height*.15)
# startCol = int(width*.15)
# endRow = int(height*.85)
# endCol = int(width*.85)
# 
# cropImg = img[startRow:endRow, startCol:endCol]
# 
# cv2.imshow('Original Image', img)
# cv2.imshow('Cropped Image', cropImg)
# cv2.waitKey(0)

#adjust image contrast
img = cv2.imread('/home/pi/Desktop/shm_model/yolov5/testImg/img.jpg')
contrastImg = cv2.addWeighted(img, 0.5, np.zeros(img.shape, img.dtype), 0, 0)
cv2.imshow('Original Image', img)
cv2.imshow('Contrast Image', contrastImg)

path = '/home/pi/Desktop/shm_model/yolov5/testImg'
cv2.imwrite(os.path.join(path , 'imgpred.jpg'), contrastImg)
cv2.waitKey(0)