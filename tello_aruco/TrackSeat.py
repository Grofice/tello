import numpy as np
import time
import Tello
from Excelwrite import writeExcel
import Track
import threading
import math


# fbTarget = 4000
# LfbTarget = 45000
fbTarget = 70
LfbTarget = 220

w = Tello.w
h = Tello.h
pElr, pEfb, pEud, pEyaw = 0, 0, 0, 0
aElr, aEfb, aEud, aEyaw = 10, 10, 10, 5
aElr, aEfb, aEud, aEyaw = 10, 10, 10, 5

# 4000

# kpidLR = [0.3, 0, 12]
# kpidFB = [0.02, 0, 3]
# kpidUD = [0.3, 0, 8]
# kpidYAW = [0.5, 0, 0]

kpidLR = [0.3, 0, 12]
# kpidFB = [0.015, 0, 1.2]
kpidFB = [0.5, 0, 3]
kpidUD = [0.5, 0, 5]
kpidYAW = [0.5, 0, 0]

# 45000
LkpidLR = [0.1 , 0, 0.8]
# LkpidFB = [0.0015, 0, 0.15]
LkpidFB = [0.25, 0, 2]
LkpidUD = [0.1, 0, 0.8]
LkpidYAW = [0.5, 0, 0]


def infoPrint(id, lr, elr, x, fb, efb, markw, ud, eud, y, yaw, eyaw, lwDiff):
    print("[SEAT: %d] lr: %4d [%4d, %4d] || fb: %4d [%4d, %4d] || ud: %4d [%4d, %4d] || yaw: %4d [%4d, %4d]"
          % (id, lr, elr, x, fb, efb, markw, ud, eud, y, yaw, eyaw, lwDiff))
    # print("fb: %4d [%3d(%6d), %3d, %3d(%6d)] area: %6d [vgx: %4d agx: %4d]"
    #       % (fb, kpidFB[0] * efb , efb, kpidFB[1] * 0 , kpidFB[2] * (efb - pEfb), efb - pEfb, area, H_tello.me.get_speed_x(), H_tello.me.get_acceleration_x()))
    
    # print("lr: %4d [%3d, %3d, %3d] || elr: %6d elr-pElr: %6d || x: %6d"
    #       % (lr, kpidLR[0] * elr , kpidLR[1] * 0 , kpidLR[2] * (elr - pElr),  elr, elr - pElr, x))
    return


def trackSeat():
    global pElr, pEfb, pEud, pEyaw
    if Tello.AUTO_SE and Tello.info[1] != Tello.TELLO_SEAT:
        Track.TRACK_STATE = Track.TRACK_SEARCH
        Tello.PRE_STATE = Tello.STATE_TRACK
        Track.PRE_STATE = Track.TRACK_SEAT
        return
    # if Tello.info[1] == Tello.TELLO_SEAT:
    #     print("Tracking seat " + str(Tello.info[1]))

    # lwRatio = (Tello.info[0][2] * w) / (Tello.info[0][3] * h)
    # lwDiff = (Tello.info[0][3] * h) - (Tello.info[0][2] * w)
    lwDiff = 0

    # Tello.info=[[[左上][右上][右下][左下]], id]
    x1, y1, x2, y2 = Tello.info[0][0][0], Tello.info[0][0][1], Tello.info[0][1][0], Tello.info[0][1][1]
    x3, y3, x4, y4 = Tello.info[0][2][0], Tello.info[0][2][1], Tello.info[0][3][0], Tello.info[0][3][1]
    xm1, ym1, xm2, ym2 = (x1 + x2) // 2, (y1 + y2) //2, (x3 + x4) // 2, (y3 + y4) //2
    markx, marky = (x1 + x3)//2, (y1 + y3)//2
    markw, markh =  math.sqrt((x1 - x2)**2 + (y1 - y2)**2), math.sqrt((x3 - x4)**2 + (y3 - y4)**2),
    area = markw * markh

    elr = markx - w//2
    # efb = fbTarget - area
    efb = fbTarget - markw
    eud = h//2 - marky

    eyaw = lwDiff
    if pEyaw > lwDiff:
        eyaw = -lwDiff
    eyaw = 0

    # 判断是否满足降落条件
    if Tello.AUTO_SW and Tello.info[1] == Tello.TELLO_SEAT and abs(elr) < aElr and abs(efb) < aEfb and abs(eud) < aEud and abs(aEyaw):
        print("----------Auto Landing-------------")
        Track.TRACK_STATE = Track.TRACK_LAND
    print("Tracking Seat %d elr: %4d efb: %4d eud: %4d eyaw: %4d" % (Tello.info[1], elr, efb, eud, eyaw))

    if Track.TRACK_STATE == Track.TRACK_SEAT:
        lr = kpidLR[0] * elr + kpidLR[1] * 0 + kpidLR[2] * (elr - pElr)
        fb = kpidFB[0] * efb + kpidFB[1] * 0 + kpidFB[2] * (efb - pEfb)
        ud = kpidUD[0] * eud + kpidUD[1] * 0 + kpidUD[2] * (eud - pEud)
        yaw = kpidYAW[0] * eyaw + kpidYAW[1] * 0 + kpidYAW[2] * (eyaw - pEyaw)

        lr = int(np.clip(lr, -20, 20))
        fb = int(np.clip(fb, -20, 20))
        ud = int(np.clip(ud, -20, 20))
        yaw = int(np.clip(yaw, -100, 100))

        # TEST
        fb = 0
        lr = 0
        # ud = 0
        yaw = 0

    elif Track.TRACK_STATE == Track.TRACK_LAND:
        # print(H_tello.me.get_height())
        if(Tello.telloTakeoff and Tello.me.get_distance_tof() <= 20):
            Tello.me.emergency()
            Tello.TELLO_STATE = Tello.STATE_LAND
            return
        # efb = LfbTarget - area
        efb = LfbTarget - markw
        lr = LkpidLR[0] * elr + LkpidLR[1] * 0 + LkpidLR[2] * (elr - pElr)
        fb = LkpidFB[0] * efb + LkpidFB[1] * 0 + LkpidFB[2] * (efb - pEfb)
        ud = LkpidUD[0] * eud + LkpidUD[1] * 0 + LkpidUD[2] * (eud - pEud)
        yaw = LkpidYAW[0] * eyaw + LkpidYAW[1] * 0 + LkpidYAW[2] * (eyaw - pEyaw)

        lr = int(np.clip(lr, -20, 20))
        fb = int(np.clip(fb, -15, 15))
        ud = int(np.clip(ud, -20, 20))
        yaw = int(np.clip(yaw, -100, 100))


    if Tello.info[1] == 0:
        elr, efb, eud, eyaw = 0, 0, 0, 0
        lr, fb, ud, yaw = 0, 0, 0, 0

    if Tello.info[1] == Tello.TELLO_SEAT:
        Track.lx, Track.ly = markx, marky

    # writeExcel([markx, area, marky])

    infoPrint(Tello.info[1], lr, elr, markx, fb, efb, markw, ud, eud, marky, yaw, eyaw, 0)

    if Tello.telloVideo:
        Tello.sendCommand(lr, fb, ud, yaw)

    

    
    pElr, pEfb, pEud, pEyaw = elr, efb, eud, eyaw
    




# def trackTarget():
#     global pElr, pEfb, pEud, pEyaw
#     while True:
#         # H_tello.me.get_battery()
#         key = cv2.waitKey(1)
       
#         if key == ord('Q'):
#             Tello.TELLO_STATE = Tello.EMERGENCY_STOP
#             if Tello.telloVideo and Tello.telloTakeoff:
#                 Tello.me.land()
#             break
#         if key == ord('M'):
#             Tello.TELLO_STATE = Tello.STATE_MANUAL
#             break
#         # if key == ord('L'):
#         #     land.start()

#         if key == ord('L'):
#             Tello.TELLO_STATE = Tello.STATE_LAND
#             # 方案2
#             # land.start()
#         # if H_tello.TELLO_STATE == H_tello.STATE_LAND and pEfb < landTargetError:
#         #     # H_tello.me.send_rc_control(0, 3, 0, 0)
#         #     H_tello.me.land()
#         if key == ord('Z'):
#             Track.TRACK_STATE = TRACK_CABIN
#         if key == ord('X'):
#             Track.TRACK_STATE = TRACK_SEAT

#         if key == ord('N'):
#             TrackCabin.N = TrackCabin.N + 1

#         if Track.TRACK_STATE == TRACK_CABIN:
#             # print("----------Tracking cabin-------------")
#             TrackCabin.pElr, TrackCabin.pEfb, TrackCabin.pEud, TrackCabin.pEyaw = TrackCabin.trackCabin(Tello.Tello.info)
#         elif Track.TRACK_STATE == TRACK_SEAT:
#             # print("----------Tracking seat-------------")
#             pElr, pEfb, pEud, pEyaw = trackAirfield(Tello.Tello.info, pElr, pEfb, pEud, pEyaw)
#         # elif H_track.TRACK_STATE == TRACK_SWITCHING:
#             # id = H_tello.Tello.info[1]
#             # if(H_tello.telloTakeoff and id == 0 and H_tello.me.get_distance_tof() <= 10):
#             #     H_tello.me.emergency()
#             #     # H_tello.sendCommand(0, 0, 0, 100)
#             #     H_tello.TELLO_STATE = H_tello.STATE_LAND
#             # if(id == H_tello.TELLO_SEAT):
#             #     H_track.TRACK_STATE = TRACK_SEAT
#             # elif id == 0:
#             #     H_tello.sendCommand(0, 0, 0, -5)
#             # else:
#             # # 未识别到任何机位
#             # if id == 0:





