from djitellopy import tello
import cv2
import numpy as np
import time
import H_tello
import threading
import H_manual, H_track


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters_create()

def tello_control():
    cv2.namedWindow('tello', 0)
    cv2.resizeWindow('tello', 400, 300)
    cv2.imshow("tello", 0)
    if (not H_tello.telloTakeoff) and H_tello.telloVideo:
        # H_tello.me.takeoff()
        print("----------TELLO TAKEOFF-------------")
        H_tello.telloTakeoff = True
    while True:
        if H_tello.TELLO_STATE == H_tello.EMERGENCY_STOP:
            break

        # 手动控制
        if H_tello.TELLO_STATE == H_tello.STATE_MANUAL:
            print("----------TELLO STATE: MANUAL-------------")
            H_manual.manualControl()

        # 追踪
        if H_tello.TELLO_STATE == H_tello.STATE_TRACK:
            print("----------TELLO STATE: TRACK-------------")
            H_track.trackTarget()


        # 降落
        if H_tello.TELLO_STATE == H_tello.STATE_LAND:
            print("----------TELLO STATE: LAND-------------")
            print("tello landing...")
            break
        # # 测距（直线距离）
        # sdistance = H_distance.calculate_distance(im0, info)
        #
        # # 降落操作
        # if(sdistance > 0):
        #     lheight = me.get_height()
        #     ldistance = math.sqrt((pow(sdistance, 2) - pow(lheight, 2)))
        #     me.send_rc_control(0, 15, 0, 0)
        #     time.sleep(ldistance / 10)
        #     me.send_rc_control(0, 0, 0, 0)
        #     me.land()
        #     exit()

tello_control = threading.Thread(target=tello_control)


def run():
    while True:

        _, frame = H_tello.cap.read()
        if not _ :
            frame = 0
        # frame = cv2.resize(img, (H_tello.w, H_tello.h))
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
        # # # https://blog.csdn.net/dgut_guangdian/article/details/107814300
        # if ids is not None:
        #     print(corners)
        #     print(ids)
        #     # print(rejectedImgPoints)

        #     #画出标志位置
        #     cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        #     width = corners[0][0][1][0] - corners[0][0][0][0]
        #     high = corners[0][0][1][1] - corners[0][0][0][0]
        cv2.imshow('detect',frame)
        if H_tello.TELLO_STATE == H_tello.EMERGENCY_STOP:
            break

    # cv2.imshow("frame",frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    # tello_control.start()
    # run()
    # cap = cv2.VideoCapture(0)
    # ret, frame = cap.read()
    # while 1:
    #     if ret:
    #         cv2.imshow('frame', frame)  # 显示读取到的这一帧画面

    #     else:
    #         cap.release()
    #         cv2.destroyAllWindows()
    # print('it is start')
    # cap = cv2.VideoCapture(0)     # 读取视频
    # ret, frame = cap.read()
    # while ret == True:               # 当视频被打开时：
    #     ret, frame = cap.read()         # 读取视频，读取到的某一帧存储到frame，若是读取成功，ret为True，反之为False
    #     if ret:                         # 若是读取成功
    #         cv2.imshow('frame', frame)  # 显示读取到的这一帧画面
    #         key = cv2.waitKey(25)       # 等待一段时间，并且检测键盘输入
    #         if key == ord('q'):         # 若是键盘输入'q',则退出，释放视频
    #             cap.release()           # 释放视频
    #             break
    #     else:
    #         cap.release()
    # cv2.destroyAllWindows()             # 关闭所有窗口
    run()
