from djitellopy import tello
import cv2
import numpy as np
import time
import Tello
import threading
import Manual, TrackCtrl, Track
import Excelwrite




aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters_create()

def tello_control():
    cv2.namedWindow('tello', 0)
    cv2.resizeWindow('tello', 400, 300)
    cv2.imshow("tello", 0)
    while True:
        if Tello.TELLO_STATE == Tello.EMERGENCY_STOP:
            Tello.TEXT = "Emergency Stoping"
            Excelwrite.excel.save(Excelwrite.SAVE_PATH + Excelwrite.FILE_NAME + str(Excelwrite.NUMBER)+'.xlsx')
            break
        elif Tello.TELLO_STATE == Tello.STATE_MANUAL:
            print("----------TELLO STATE: MANUAL-------------")
            Tello.TEXT = "Manual"
            Manual.manualControl()
        elif Tello.TELLO_STATE == Tello.STATE_TRACK:
            print("----------TELLO STATE: TRACK-------------")
            Tello.TEXT = "Track"
            TrackCtrl.trackTarget()
        elif Tello.TELLO_STATE == Tello.STATE_LAND:
            print("----------TELLO STATE: LAND-------------")
            Tello.TEXT = "Landed"
            print("tello landing...")
            Tello.me.end()
            break

tello_control = threading.Thread(target=tello_control)


def run():
    while True:
        _, frame = Tello.cap.read()
        frame = cv2.resize(frame, (Tello.w, Tello.h))
        if Tello.TELLO_STATE == Tello.STATE_TRACK:
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
            # # https://blog.csdn.net/dgut_guangdian/article/details/107814300
            if ids is not None:
                i = 0
                for id in ids:
                    if Track.TRACK_STATE == Track.TRACK_SEARCH and ids[i][0] != 0:
                        Tello.info = [corners[i][0], ids[i][0]]
                    elif Track.TRACK_STATE == Track.TRACK_CABIN and ids[i][0] == Tello.TELLO_CABIN:
                        Tello.info = [corners[i][0], ids[i][0]]
                    elif Track.TRACK_STATE == Track.TRACK_SWITCH and ids[i][0] >= Tello.TELLO_SEAT:
                        Tello.info = [corners[i][0], ids[i][0]]
                    elif Track.TRACK_STATE == Track.TRACK_SEAT and ids[i][0] == Tello.TELLO_SEAT:
                        Tello.info = [corners[i][0], ids[i][0]]
                    else:
                        Tello.info = [[[0, 0], [0, 0], [0, 0], [0, 0]], 0]
                    i = i + 1

                # if ids[0][0] == 33:
                #     H_tello.info = [corners[0][0], ids[0][0]]
                # else:
                #     H_tello.info = [[[0, 0], [0, 0], [0, 0], [0, 0]], 0]

                #画出标志位置
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            else:
                Tello.info = [[[0, 0], [0, 0], [0, 0], [0, 0]], 0]

            
        
        if cv2.waitKey(1) & 0xFF == ord('Q') or Tello.TELLO_STATE == Tello.EMERGENCY_STOP:
            cv2.destroyAllWindows()
            break
        cv2.putText(frame,Tello.TEXT,(0,25),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
        cv2.imshow('Video',frame)

    # cv2.imshow("frame",frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    tello_control.start()
    tello_control
    run()