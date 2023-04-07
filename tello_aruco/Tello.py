from djitellopy import tello
import cv2

AUTO_SW = False
# AUTO_SW = True

AUTO_SE = False
# AUTO_SE = True

TELLO_CABIN = 1
TELLO_SEAT = 11

# 显示信息
TEXT = "Manual"

# 引导速度和相关时间设置
GUID_3D_SPEED = 40
GUID_YAW_SPEED = 60
T_YAW_360 = 6.0
T_3D_200 = 5.0
T_WAIT = 3.0

telloVideo = False
telloVideo = True
telloTakeoff = False
me = tello.Tello()
w, h = 665, 500

# 识别程序识别到的信息
info = [[[0, 0],
       [0, 0],
       [0, 0],
       [0, 0]], 0]


ctrlThread = False

M2T = False
EMERGENCY_STOP = -1
STATE_MANUAL = 0
STATE_TRACK = 1
STATE_LAND = 2

TELLO_STATE = STATE_MANUAL
PRE_STATE = STATE_MANUAL






if telloVideo:
    me.connect()
    print(me.get_battery())
    me.streamon()
    cap = cv2.VideoCapture('udp:/0.0.0.0:11111', cv2.CAP_FFMPEG)
    while True:
        ret, frame = cap.read()
        if(ret):
            break
else:
    print("computer video")
    cap = cv2.VideoCapture(0)
    # while True:
    #     _, frame = cap.read()
    #     cv2.imshow("testQuit", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('Q'):
    #         break


def sendCommand(lr, fb, ud, yaw):
    # if lr != 0 or fb != 0 or ud != 0 or yaw != 0:
    #     print("lr: %4d fb: %4d ud %4d yaw %4d" % (lr, fb, ud, yaw))
    me.send_rc_control(lr, fb, ud, yaw)
    # me.send_rc_control(0, 0, 0, 0)



