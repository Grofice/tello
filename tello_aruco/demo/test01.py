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
# ![](C:/Users/23796/AppData/Local/Temp/WeChat Files/d9e9d1e0c722200b29f43d0699edbde.png)

# print(rejectedImgPoints)

#画出标志位置
cv.aruco.drawDetectedMarkers(frame, corners, ids)

print(corners[0][0][0][0])
print(ids[0][0])
info = [corners[0][0], ids[0][0]]
print(info)
markx, marky = (info[0][0][0] + info[0][1][0])//2, (info[0][1][1] + info[0][2][1])//2
markw, markh = info[0][1][0] - info[0][0][0], info[0][2][1] - info[0][1][1]
print(markx, marky, markw, markh)
cv.imwrite('detect.png',frame)

# cv.imshow("frame",frame)
# cv.waitKey(0)
# cv.destroyAllWindows()