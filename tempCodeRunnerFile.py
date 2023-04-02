import numpy as np
import time
import cv2 as cv

#读取图片
frame=cv.imread('test.png')
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters =  cv.aruco.DetectorParameters_create()

#使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

print(corners)
print(ids)
# print(rejectedImgPoints)

#画出标志位置
cv.aruco.drawDetectedMarkers(frame, corners, ids)

print(corners[0][0][1][0])

width = corners[0][0][1][0] - corners[0][0][0][0]
high = corners[0][0][1][1] - corners[0][0][0][0] 

cv.imwrite('detect.png',frame)

# cv.imshow("frame",frame)
# cv.waitKey(0)
# cv.destroyAllWindows()