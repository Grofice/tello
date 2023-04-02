import numpy as np
import time
import cv2 as cv

dist=np.array(([[-0.58650416 , 0.59103816, -0.00443272 , 0.00357844 ,-0.27203275]]))
newcameramtx=np.array([[189.076828   ,  0.    ,     361.20126638]
 ,[  0 ,2.01627296e+04 ,4.52759577e+02]
 ,[0, 0, 1]])
mtx=np.array([[398.12724231  , 0.      ,   304.35638757],
 [  0.       ,  345.38259888, 282.49861858],
 [  0.,           0.,           1.        ]])

#读取图片
frame=cv.imread('image/test01.png')
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters =  cv.aruco.DetectorParameters_create()

#使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

print(corners)
print(ids)
# print(rejectedImgPoints)

rvec, tvec, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)



#画出标志位置
cv.aruco.drawAxis(frame, mtx, dist, rvec[0, :, :], tvec[0, :, :], 0.03)
cv.aruco.drawDetectedMarkers(frame, corners, ids)

print(corners[0][0][1][0])

width = corners[0][0][1][0] - corners[0][0][0][0]
high = corners[0][0][1][1] - corners[0][0][0][0]

cv.imwrite('image/testresult01.png',frame)

# cv.imshow("frame",frame)
# cv.waitKey(0)
# cv.destroyAllWindows()