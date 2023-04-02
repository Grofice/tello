from djitellopy import tello
import cv2

telloVideo = False
# telloVideo = True
telloTakeoff = False
me = tello.Tello()
w, h = 360, 240

info = [[0, 0, 0, 0], 0]

ctrlThread = False

EMERGENCY_STOP = 0
STATE_MANUAL = 1
STATE_TRACK = 2
STATE_LAND = 3

TELLO_STATE = STATE_MANUAL




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
    ret, frame = cap.read()
    # while 1:
    #     if ret:
    #         cv2.imshow('frame', frame)  # 显示读取到的这一帧画面
    #         key = cv2.waitKey(25)
    #     else:
    #         cap.release()
    #         cv2.destroyAllWindows()


def sendCommand(lr, fb, ud, yaw):

    # me.send_rc_control(lr, fb, ud, yaw)
    me.send_rc_control(0, 0, 0, 0)



