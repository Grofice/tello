import Tello
import numpy as np
import Track

from Excelwrite import writeExcel
import math


w, h = Tello.w, Tello.h

# fbRange = [50,60]
# pid = [0.4, 0.4, 0]
# pEyaw = 0

# YT = h // 3
YT = 350

# CID = H_tello.TELLO_CABIN
# SID = H_tello.TELLO_SEAT
# N = SID - CID
N = 1
fbTarget = 80 * N
# udTarget = YT + (N - 1) / N * (YT - h // 2) 
udTarget = h // 2 + (YT - h // 2) / N


pElr, pEfb, pEud, pEyaw = 0, 0, 0, 0
aElr, aEfb, aEud, aEyaw = 10, 10, 10, 5
aElr, aEfb, aEud, aEyaw = 20, 20, 20, 5
kpidLR = [0.001, 0, 0]
kpidFB = [0.5, 0, 3]
kpidUD = [0.005, 0, 0]
kpidYAW = [0.3, 0, 3]


def infoPrint(id, lr, elr, x, fb, efb, markw, ud, eud, y, yaw, eyaw, lwDiff):
    print("[CABIN: %d] lr: %4d [%4d, %4d] || fb: %4d [%4d, %4d] || ud: %4d [%4d, %4d] || yaw: %4d [%4d, %4d]"
          % (id, lr, elr, x, fb, efb, markw, ud, eud, y, yaw, eyaw, lwDiff))

    # print("fb: %4d [%3d(%6d), %3d, %3d(%6d)] area: %6d [vgx: %4d agx: %4d]"
    #       % (fb, kpidFB[0] * efb , efb, kpidFB[1] * 0 , kpidFB[2] * (efb - pEfb), efb - pEfb, area, H_tello.me.get_speed_x(), H_tello.me.get_acceleration_x()))
    
    # print("lr: %4d [%3d, %3d, %3d] || elr: %6d elr-pElr: %6d || x: %6d"
    #       % (lr, kpidLR[0] * elr , kpidLR[1] * 0 , kpidLR[2] * (elr - pElr),  elr, elr - pElr, x))
    return


def trackCabin():
    global pElr, pEfb, pEud, pEyaw
    if Tello.AUTO_SE and Tello.info[1] != Tello.TELLO_CABIN:
        Track.TRACK_STATE = Track.TRACK_SEARCH
        Tello.PRE_STATE = Tello.STATE_TRACK
        Track.PRE_STATE = Track.TRACK_CABIN
        return

    fbTarget = 60 / N
    # udTarget = YT - (N - 1) / N * (YT - h // 2) 
    # udTarget = h // 2 + (YT - h // 2) / N
    fbTarget = 65
    udTarget = 400

    # if Tello.info[1] == Tello.TELLO_CABIN:
    #     print("Tracking cabin " + str(Tello.info[1]))


    lwDiff = 0

    x1, y1, x2, y2 = Tello.info[0][0][0], Tello.info[0][0][1], Tello.info[0][1][0], Tello.info[0][1][1]
    x3, y3, x4, y4 = Tello.info[0][2][0], Tello.info[0][2][1], Tello.info[0][3][0], Tello.info[0][3][1]
    xm1, ym1, xm2, ym2 = (x1 + x2) // 2, (y1 + y2) //2, (x3 + x4) // 2, (y3 + y4) //2
    markx, marky = (x1 + x3)//2, (y1 + y3)//2
    markw, markh =  math.sqrt((x1 - x2)**2 + (y1 - y2)**2), math.sqrt((x3 - x4)**2 + (y3 - y4)**2),
    area = markw * markh
    corner = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
    if corner != 0:     
        dist = 7000 / corner
    else:
        dist = 0
    
    angle =  math.atan2((ym2-ym1), (xm2-xm1))
    theta = angle*(180 /math.pi)

    elr = (markx - w//2) * dist
    # efb = fbTarget - markw
    # efb = fbTarget - area
    efb = dist - fbTarget
    eud = (udTarget - marky) * dist
    eyaw = theta - 90

    # 判断是否满足切换条件
    if Tello.AUTO_SW and Tello.info[1] == Tello.TELLO_CABIN and abs(elr) < aElr and abs(efb) < aEfb and abs(eud) < aEud and abs(aEyaw):
        # print("----------Auto Landing-------------")
        Track.TRACK_STATE = Track.TRACK_SWITCH
        return
    # print("Tracking Cabin %d elr: %4d efb: %4d eud: %4d eyaw: %4d" % (Tello.info[1], elr, efb, eud, eyaw))

 
    lr = kpidLR[0] * elr + kpidLR[1] * 0 + kpidLR[2] * (elr - pElr)
    fb = kpidFB[0] * efb + kpidFB[1] * 0 + kpidFB[2] * (efb - pEfb)
    ud = kpidUD[0] * eud + kpidUD[1] * 0 + kpidUD[2] * (eud - pEud)
    yaw = kpidYAW[0] * eyaw + kpidYAW[1] * 0 + kpidYAW[2] * (eyaw - pEyaw)

    lr = int(np.clip(lr, -30, 30))
    fb = int(np.clip(fb, -30, 30))
    ud = int(np.clip(ud, -30, 30))
    yaw = int(np.clip(yaw, -30, 30))


    if Tello.info[1] == 0:
        elr, efb, eud, eyaw = 0, 0, 0, 0
        lr, fb, ud, yaw = 0, 0, 0, 0
    if Tello.info[1] == Tello.TELLO_CABIN:
        Track.lx, Track.ly = markx, marky
    
    infoPrint(Tello.info[1], lr, elr, markx, fb, efb, dist, ud, eud, marky, yaw, eyaw, theta)
    # print("[N: %d] fbT: %4d efb: %4d markw: %4d|| udT: %4d eud: %4d marky: %4d" % (N, fbTarget, efb, markw, udTarget, eud, marky))
    if Tello.telloVideo:
        # 
        Tello.sendCommand(lr, fb, ud, yaw)
    # writeExcel([markx, markw, marky])
    Tello.TEXT = "markw " + str((int)(markw)) + "area " + str((int)(area)) + "corner " + str((int)(corner)) 
    writeExcel([markw, area, corner])
    # if Tello.info[1] != 0 and abs(elr) < aElr and abs(efb) < aEfb and abs(eud) < aEud and abs(aEyaw):
    #     H_track.TRACK_STATE = H_track.TRACK_SWITCHING

    
    pElr, pEfb, pEud, pEyaw = elr, efb, eud, eyaw


    