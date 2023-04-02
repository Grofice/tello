import numpy as np
import time
import cv2 as cv

#相机纠正参数
dist=np.array(([[-0.58650416 , 0.59103816, -0.00443272 , 0.00357844 ,-0.27203275]]))
newcameramtx=np.array([[189.076828   ,  0.    ,     361.20126638]
 ,[  0 ,2.01627296e+04 ,4.52759577e+02]
 ,[0, 0, 1]])
mtx=np.array([[398.12724231  , 0.      ,   304.35638757],
 [  0.       ,  345.38259888, 282.49861858],
 [  0.,           0.,           1.        ]])

cap = cv.VideoCapture(0)

font = cv.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

#num = 0
while True:
    ret, frame = cap.read()
    h1, w1 = frame.shape[:2]
    # 读取摄像头画面
    # 纠正畸变
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (h1, w1), 0, (h1, w1))
    dst1 = cv.undistort(frame, mtx, dist, None, newcameramtx)
    x, y, w1, h1 = roi
    dst1 = dst1[y:y + h1, x:x + w1]
    frame=dst1

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
    parameters =  cv.aruco.DetectorParameters_create()
    dst1 = cv.undistort(frame, mtx, dist, None, newcameramtx)

    #使用cv.aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,cv.aruco_dict,parameters=parameters)

#    如果找不到id
    if ids is not None:

        rvec, tvec, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        # 估计每个标记的姿态并返回值rvet和tvec ---不同
        # from camera coeficcients
        (rvec-tvec).any() # get rid of that nasty numpy value array error

        for i in range(rvec.shape[0]):
            cv.aruco.drawAxis(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03)
            cv.aruco.drawDetectedMarkers(frame, corners)
        cv.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv.LINE_AA)
    else:
        cv.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv.LINE_AA)

    cv.imshow("frame",frame)
    key = cv.waitKey(1)

    if key == 27:         # 按esc键退出
        print('esc break...')
        cap.release()
        cv.destroyAllWindows()
        break

    if key == ord(' '):   # 按空格键保存
        filename = str(time.time())[:10] + ".png"
        cv.imwrite(filename, frame)