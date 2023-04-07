import numpy as np
import time
import Tello
from Excelwrite import writeExcel
import Track
import Timer
import cv2


fbTarget = 4000

w = Tello.w
h = Tello.h
pElr, pEfb, pEud, pEyaw = 0, 0, 0, 0

# 4000
# kpidLR = [0.3, 0, 12]
# kpidFB = [0.02, 0, 3]
# kpidUD = [0.3, 0, 8]
# kpidYAW = [0.5, 0, 0]
kpidLR = [0.15, 0, 4]
kpidFB = [0.015, 0, 1.2]
kpidUD = [0.15, 0, 4]
kpidYAW = [0.5, 0, 0]



def infoPrint(lr, elr, x, fb, efb, area, ud, eud, y, yaw, eyaw, lwDiff):
    # print("[Correct by Seat %d]lr: %4d [%4d, %4d] || fb: %4d [%4d, %4d] || ud: %4d [%4d, %4d] || yaw: %4d [%4d, %4d]"
    #       % (lr, elr, x, fb, efb, area, ud, eud, y, yaw, eyaw, lwDiff))
    print("[Correct by Seat %d]lr: %4d [%4d, %4d] || fb: %4d [%4d, %4d]"
          % (Tello.info[1], lr, elr, x, fb, efb, area))
    # print("fb: %4d [%3d(%6d), %3d, %3d(%6d)] area: %6d [vgx: %4d agx: %4d]"
    #       % (fb, kpidFB[0] * efb , efb, kpidFB[1] * 0 , kpidFB[2] * (efb - pEfb), efb - pEfb, area, H_tello.me.get_speed_x(), H_tello.me.get_acceleration_x()))
    
    # print("lr: %4d [%3d, %3d, %3d] || elr: %6d elr-pElr: %6d || x: %6d"
    #       % (lr, kpidLR[0] * elr , kpidLR[1] * 0 , kpidLR[2] * (elr - pElr),  elr, elr - pElr, x))
    return

def correct():
    global pElr, pEfb, pEud, pEyaw
    if Tello.info[1] == Tello.TELLO_SEAT:
        Track.TRACK_STATE = Track.TRACK_SEARCH
        Tello.PRE_STATE = Tello.STATE_TRACK
        Track.PRE_STATE = Track.TRACK_SWITCH
        return
    # Tello.info=[[[左上][右上][右下][左下]], id]
    markx, marky = (Tello.info[0][0][0] + Tello.info[0][1][0])//2, (Tello.info[0][1][1] + Tello.info[0][2][1])//2
    markw, markh = Tello.info[0][1][0] - Tello.info[0][0][0], Tello.info[0][2][1] - Tello.info[0][1][1]
    area = markw * markh

    elr = markx - w//2
    efb = fbTarget - area
    eud = h//2 - marky

    lwDiff = 0
    eyaw = lwDiff
    if pEyaw > lwDiff:
        eyaw = -lwDiff
    eyaw = 0

    lr = kpidLR[0] * elr + kpidLR[1] * 0 + kpidLR[2] * (elr - pElr)
    fb = kpidFB[0] * efb + kpidFB[1] * 0 + kpidFB[2] * (efb - pEfb)
    ud = kpidUD[0] * eud + kpidUD[1] * 0 + kpidUD[2] * (eud - pEud)
    yaw = kpidYAW[0] * eyaw + kpidYAW[1] * 0 + kpidYAW[2] * (eyaw - pEyaw)

    lr = int(np.clip(lr, -20, 20))
    fb = int(np.clip(fb, -20, 20))
    ud = int(np.clip(ud, -20, 20))
    yaw = int(np.clip(yaw, -100, 100))

    if Tello.info[1] == 0:
        elr, efb, eud, eyaw = 0, 0, 0, 0
        lr, fb, ud, yaw = 0, 0, 0, 0

    if Tello.info[1] == Tello.TELLO_SEAT:
        Track.lx, Track.ly = markx, marky

    # writeExcel([markx, area, marky])

    # infoPrint(lr, elr, markx, fb, efb, area, ud, eud, marky, yaw, eyaw, lwDiff)

    if Tello.telloVideo:
        Tello.sendCommand(lr, fb, (int)(-Tello.GUID_3D_SPEED/2), 0)
    

    
    pElr, pEfb, pEud, pEyaw = elr, efb, eud, eyaw


def trackSwitch():
    # 无人机降落，判断识别到的id
    Tello.sendCommand(0, 0, (int)(-Tello.GUID_3D_SPEED/2), 0)
    Timer.start()
    while True:
        key = cv2.waitKey(1)
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            return
        
        if Tello.info[1] == Tello.TELLO_SEAT:
            Tello.sendCommand(0, 0, 0, 0)
            Track.TRACK_STATE = Track.TRACK_SEAT
            return
        if Tello.info[1] < Tello.TELLO_SEAT:
            Tello.TEXT = "Tracking Seat...(Correct by id " + str(Tello.info[1]) + ")"
            correct()
            if Track.TRACK_STATE == Track.TRACK_SWITCH:
                continue
            else:
                Tello.sendCommand(0, 0, 0, 0)
                return
        if Tello.info[1] > Tello.TELLO_SEAT:
            break
        # 无人机高度过低
        if(Tello.telloTakeoff and Tello.me.get_distance_tof() <= 10):
            break

        
    # 没找到机位，回到原高度，切换到手动模式，发出警告
    totalTime = Timer.elapsed()
    Timer.end()
    print("The specified seat was not found: blocked/lost.")
    Tello.TEXT = "Can't find Seat! Returning to the original height."
    Tello.sendCommand(0, 0, (int)(Tello.GUID_3D_SPEED/2), 0)
    Timer.start()
    while Timer.elapsed() <= totalTime:
        key = cv2.waitKey(1)
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            return
    Timer.end()
    Tello.TELLO_STATE = Tello.STATE_MANUAL
    








    






