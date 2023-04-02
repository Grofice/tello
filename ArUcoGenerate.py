import cv2 as cv
import numpy as np
 
# 加载用于生成标记的字典
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
 
markerImage = np.zeros((200, 200), dtype=np.uint8)
# markerImage = cv.aruco.drawMarker(dictionary, 33, 200, markerImage, 1)
markerImage = cv.aruco.drawMarker(dictionary, 1, 200, markerImage, 1)
# markerImage = cv.aruco.drawMarker(dictionary, 11, 200, markerImage, 1)
# markerImage = cv.aruco.drawMarker(dictionary, 12, 200, markerImage, 1)

 
cv.imwrite("marker1.png", markerImage)
# cv.imwrite("marker11.png", markerImage)
# cv.imwrite("marker12.png", markerImage)
