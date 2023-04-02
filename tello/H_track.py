import numpy as np
import time
import H_tello
import cv2
landTargetError = 400
fbTarget = 400
fbAllowError = 600

w = H_tello.w
h = H_tello.h
pElr, pEfb, pEud, pEyaw = 0, 0, 0, 0
kpidLR = [0.5, 0, 1]
kpidFB = [0.18, 0, 0.2]
kpidUD = [0.5, 0, 1]
kpidYAW = [0.5, 0, 1]


def infoPrint(lr, elr, x, fb, efb, area, ud, eud, y, yaw, eyaw, lwDiff):
    print("lr: %4d [%4d, %4d] || fb: %4d [%4d, %4d] || ud: %4d [%4d, %4d] || yaw: %4d [%4d, %4d]"
          % (lr, elr, x, fb, efb, area, ud, eud, y, yaw, eyaw, lwDiff))
    return


def trackAirfield(info, pElr, pEfb, pEud, pEyaw):
    # info=[[x, y, w, h], conf]
    x, y = info[0][0] * w, info[0][1] * h
    area = info[0][2] * w * info[0][3] * h
    # lwRatio = (info[0][2] * w) / (info[0][3] * h)
    lwDiff = (info[0][3] * h) - (info[0][2] * w)

    elr = x - w//2
    efb = fbTarget - area
    eud = y - h//2
    eyaw = lwDiff
    if pEyaw > lwDiff:
        eyaw = -lwDiff

    lr = kpidLR[0] * elr + kpidLR[1] * 0 + kpidLR[2] * (elr - pElr)
    fb = kpidFB[0] * efb + kpidFB[1] * 0 + kpidFB[2] * (efb - pEfb)
    ud = kpidUD[0] * eud + kpidUD[1] * 0 + kpidUD[2] * (eud - pEud)
    yaw = kpidYAW[0] * eyaw + kpidYAW[1] * 0 + kpidYAW[2] * (eyaw - pEyaw)

    lr = int(np.clip(lr, -50, 50))
    fb = int(np.clip(fb, -50, 50))
    ud = int(np.clip(ud, -50, 50))
    yaw = int(np.clip(yaw, -100, 100))

    if info[1] == 0:
        elr, efb, eud, eyaw = 0, 0, 0, 0
        lr, fb, ud, yaw = 0, 0, 0, 0
    infoPrint(lr, elr, x, fb, efb, area, ud, eud, y, yaw, eyaw, lwDiff)
    if H_tello.telloVideo:
        H_tello.sendCommand(lr, fb, ud, yaw)
    return elr, efb, eud, eyaw


def trackTarget():
    global pElr, pEfb, pEud, pEyaw
    while True:
        # H_tello.me.get_battery()

        
        key = cv2.waitKey(1)
        if key == ord('Q'):
            H_tello.TELLO_STATE = H_tello.EMERGENCY_STOP
            break
        if key == ord('M'):
            H_tello.TELLO_STATE = H_tello.STATE_MANUAL
            break
        if key == ord('L'):
            H_tello.TELLO_STATE = H_tello.STATE_LAND
        if H_tello.TELLO_STATE == H_tello.STATE_LAND and pEfb < landTargetError:
            H_tello.me.land()
        pElr, pEfb, pEud, pEyaw = trackAirfield(H_tello.info, pElr, pEfb, pEud, pEyaw)

# def trackAirfield_1(info, pError):
#     global telloTakeoff
#     if not telloTakeoff and telloVideo:
#         # me.takeoff()
#         telloTakeoff = True
#     x, y = info[0][0] * w, info[0][1] * h  # info=[[x, y, w, h], conf]
#     area = info[0][2] * w * info[0][3] * h
#     fb = 0
#     error = x - w//2
#     speed = kpid[0] * error + kpid[2] * (error - pError)
#     speed = int(np.clip(speed, -100, 100))
#
#     if fbRange[0] < area < fbRange[1]:
#         fb = 0
#     elif area > fbRange[1]:
#         fb = -15
#     elif area < fbRange[0] and area != 0:
#         fb = 15
#
#     if x == 0:
#         speed = 0
#         error = 0
#     print("fb: %d\t\trotate: %d\t\tarea: %d\t\t"%(fb, speed, area))
#     # if telloVideo:
#         # me.send_rc_control(0, fb, 0, speed)
#     return error

# # 根据检测框信息修改飞行参数
# #
# def trackAirfield(# me, img,
#         info, pErrorRotate, pErrorUp, pErrorFB):
#     global telloTakeoff
#     if not telloTakeoff and telloVideo:
#         me.takeoff()
#         telloTakeoff = True
#     # cv2.circle(img, (int(w / 2), int(h / 2)), 5, (0, 255, 0), cv2.FILLED)   # 以图片中心为圆心，图片高度的一半作圆
#     # if x > 10 or y > 10:
#     #     cv2.line(img, (int(w / 2), int(h / 2)), (x, y), (255, 0, 0), lineThickness)  # 以图片的中心为起点，无人机映射的位置为终点作直线
#     if info[1] == 0:
#         ErrorRotate = 0
#         ErrorUp = 0
#         ErrorFB = 0
#         rotatespeed = 0
#         updownspeed = 0
#         fbspeed = 0
#         area = 0
#         pid[0][0] = pid[0][1] = pid[0][2] = 0
#         pid[1][0] = pid[1][1] = pid[1][2] = 0
#         pid[2][0] = pid[2][1] = pid[2][2] = 0
#     else:
#         x, y = info[0][0] * w, info[0][1] * h  # info=[[x, y, w, h], conf]
#         area = info[0][2] * w * info[0][3] * h
#         ErrorRotate = x - w / 2  # 计算误差值
#         # ErrorUp = 3 * h / 4 - y
#         ErrorUp = 50 - me.get_height()
#         ErrorFB = 1500 - area
#
#         pid[0][0] = kpid[0][0] * ErrorRotate
#         pid[0][1] = pid[0][1] + kpid[0][1] * ErrorRotate
#         pid[0][1] = int(np.clip(pid[0][1], -7, 7))
#         pid[0][2] = kpid[0][2] * (ErrorRotate - pErrorRotate)
#
#         pid[1][0] = kpid[1][0] * ErrorUp
#         pid[1][1] = pid[1][1] + kpid[1][1] * ErrorUp
#         pid[1][1] = int(np.clip(pid[1][1], -5, 5))
#         pid[1][2] = kpid[1][2] * (ErrorUp - pErrorUp)
#
#         pid[2][0] = kpid[2][0] * ErrorFB
#         pid[2][1] = pid[2][1] + kpid[2][1] * ErrorFB
#         pid[2][1] = int(np.clip(pid[2][1], -7, 7))
#         pid[2][2] = kpid[2][2] * (ErrorFB - pErrorFB)
#
#         rotatespeed = pid[0][0] + pid[0][1] + pid[0][2]  # pid
#         updownspeed = pid[1][0] + pid[1][1] + pid[1][2]
#         fbspeed = pid[2][0] + pid[2][1] + pid[2][2]
#
#         rotatespeed = int(np.clip(rotatespeed, -40, 40))  # 划定速度的上下限，避免出现过大或者过小的速度
#         updownspeed = int(np.clip(updownspeed, -40, 40))
#         fbspeed = int(np.clip(fbspeed, -40, 40))
#
#         print("fb: %3d pid: [%2d %2d %2d] error: [%5d %5d] area: %4d \033[31m|\033[0m"
#               % (fbspeed, pid[2][0], pid[2][1], pid[2][2], pErrorFB, ErrorFB, area), end=" ")
#         print("rotate: %3d pid: [%2d %2d %2d] error: [%2d %2d] \033[31m|\033[0m"
#               % (rotatespeed, pid[0][0], pid[0][1], pid[0][2], pErrorRotate, ErrorRotate), end=" ")
#         print("ud: %3d pid: [%2d %2d %2d] error: [%2d %2d]"
#               % (updownspeed, pid[1][0], pid[1][1], pid[1][2], pErrorUp, ErrorUp))
#
#         print("fb: %3d pid: [%2d %2d %2d] error: [%5d %5d] area: %4d |"
#               % (fbspeed, pid[2][0], pid[2][1], pid[2][2], pErrorFB, ErrorFB, area), end=" ", file=pidlog)
#         print("rotate: %3d pid: [%2d %2d %2d] error: [%2d %2d] |"
#               % (rotatespeed, pid[0][0], pid[0][1], pid[0][2], pErrorRotate, ErrorRotate), end=" ", file=pidlog)
#         print("ud: %3d pid: [%2d %2d %2d] error: [%2d %2d]"
#               % (updownspeed, pid[1][0], pid[1][1], pid[1][2], pErrorUp, ErrorUp), file=pidlog)
#     if telloVideo:
#         me.send_rc_control(0, fbspeed, updownspeed, rotatespeed)  # 利用rc控件来实现对于无人机的操控
#     return ErrorRotate, ErrorUp, ErrorFB