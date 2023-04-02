# import numpy as np
# import time
# import cv as cv

# # 相机的畸变系数和内参矩阵
# dist=np.array(([[-0.58650416 , 0.59103816, -0.00443272 , 0.00357844 , -0.27203275]]))
# mtx=np.array([[398.12724231, 0, 304.35638757],[0, 345.38259888, 282.49861858],[0, 0, 1]])
# # newcameramtx=np.array([[189.076828   ,  0.    ,     361.20126638]
# #  ,[  0 ,2.01627296e+04 ,4.52759577e+02]
# #  ,[0, 0, 1]])

# #读取图片
# frame=cv.imread('test01.png')
# gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
# parameters =  cv.aruco.DetectorParameters_create()

# #使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
# corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

# print(corners)
# print(ids)
# # print(rejectedImgPoints)

# rvec, tvec, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
# print(rvec)
# print(tvec)

# #画出标志位置
# cv.aruco.drawAxis(frame, mtx, dist, rvec[0, :, :], tvec[0, :, :], 0.1)
# cv.aruco.drawDetectedMarkers(frame, corners, ids)

# print(corners[0][0][1][0])

# width = corners[0][0][1][0] - corners[0][0][0][0]
# high = corners[0][0][1][1] - corners[0][0][0][0] 

# cv.imwrite('testresult01.png',frame)

# # cv.imshow("frame",frame)
# # cv.waitKey(0)
# # cv.destroyAllWindows()

import cv2 as cv
import numpy as np

def Rotate(filename):
    image = cv.imread(filename)

    print(image.shape)

    #读取图片
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
    parameters =  cv.aruco.DetectorParameters_create()

    #使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    #画出标志位置
    cv.aruco.drawDetectedMarkers(image, corners, ids)

    width = corners[0][0][1][0] - corners[0][0][0][0]
    high = corners[0][0][1][1] - corners[0][0][0][0]

    cv.imwrite('testresult01.png',image)

    # cv.imshow("frame",frame)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # 取得图像中心点，当做旋转的中心
    height, width = image.shape[:2]
    center = (width/2, height/2)

    # 创建2d旋转矩阵
    # center：旋转中心
    # angle：旋转角度
    # scale：比例因子，用于将图像向上或向下缩放
    rotate_matrix = cv.getRotationMatrix2D(center=center, angle=45, scale=1)
    print(rotate_matrix)

    # 使用旋转矩阵对图像应用仿射变换
    # src：原图
    # M：变换矩阵
    # dsize：输出图像的大小
    rotated_image = cv.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

    cv.imshow('Original image', image)
    cv.imshow('Rotated image', rotated_image)

    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    Rotate('image/test01.png')
