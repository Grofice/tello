import time
from H_tello import me, telloTakeoff, telloVideo, sendCommand
from H_tello import TELLO_STATE, STATE_MANUAL, STATE_TRACK, STATE_LAND
import H_distance
import H_track
import H_manual
import math
import cv2


def tello_control():
    cv2.namedWindow('tello', 0)
    cv2.resizeWindow('tello', 400, 300)
    cv2.imshow("tello", 0)
    global telloTakeoff
    if (not telloTakeoff) and telloVideo:
        me.takeoff()
        print("----------TELLO TAKEOFF-------------")
        telloTakeoff = True
    while True:
        # 手动控制
        if TELLO_STATE == STATE_MANUAL:
            print("----------TELLO STATE: MANUAL-------------")
            H_manual.manualControl()

        # 追踪
        if TELLO_STATE == STATE_TRACK:
            print("----------TELLO STATE: TRACK-------------")
            H_track.trackTarget()
            return
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