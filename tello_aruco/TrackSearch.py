import Track
import Tello
import Timer
import cv2


# 易失边界，用来判断最后出现的位置
border = 4/5
borderSeat = 1/3

# op: 0为<=，1为!=
def judge(time, op, targetid, stop, targetState):
    Timer.start()
    while Timer.elapsed() <= time:
        if Tello.info[1] == targetid:
            if stop:
                Tello.sendCommand(0, 0, 0, 0)
            Track.TRACK_STATE = targetState
            return True
    if stop:
        Tello.sendCommand(0, 0, 0, 0)
    Timer.end()
    return False

def fromManual():
    # 旋转360度
    Tello.sendCommand(0, 0, 0, (int)(Tello.GUID_YAW_SPEED))
    Timer.start()
    while Timer.elapsed() <= Tello.T_YAW_360:
        if Tello.info[1] == Tello.TELLO_CABIN:
            Tello.sendCommand(0, 0, 0, 0)
            Track.TRACK_STATE = Track.TRACK_CABIN
            return
        key = cv2.waitKey(1)
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            return
    Tello.sendCommand(0, 0, 0, 0)
    Timer.end()

    # 向前2米
    Tello.sendCommand(0, (int)(Tello.GUID_3D_SPEED), 0, 0)
    Timer.start()
    while Timer.elapsed() <= Tello.T_3D_200:
        if Tello.info[1] == Tello.TELLO_CABIN:
            Tello.sendCommand(0, 0, 0, 0)
            Track.TRACK_STATE = Track.TRACK_CABIN
            return
        key = cv2.waitKey(1)
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            return
    Tello.sendCommand(0, 0, 0, 0)
    Timer.end()

     # 旋转180度
    Tello.sendCommand(0, 0, 0, (int)(Tello.GUID_YAW_SPEED))
    Timer.start()
    while Timer.elapsed() <= Tello.T_YAW_360/2:
        if Tello.info[1] == Tello.TELLO_CABIN:
            Tello.sendCommand(0, 0, 0, 0)
            Track.TRACK_STATE = Track.TRACK_CABIN
            return
        key = cv2.waitKey(1)
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            return
    Tello.sendCommand(0, 0, 0, 0)
    Timer.end()

    # 执行结束仍然没有找到，切换回手动模式，发出警告
    Tello.TELLO_STATE = Tello.STATE_MANUAL
    print("Can't find CABIN!")
    # 在视频流上显示
    return

def fromTrackCabin():
    # 最后一次出现在非易失边界中，即视野中间
    if border*Tello.w <= Track.lx <= (1 - border)*Tello.w and border*Tello.h <= Track.ly <= (1 - border)*Tello.h:
        Timer.start()
        while Timer.elapsed() <= Tello.T_WAIT:
            if Tello.info[1] == Tello.TELLO_CABIN:
                Track.TRACK_STATE = Track.TRACK_CABIN
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Timer.end()
    else:
        # 先左右转
        if Track.lx > (1 - border)*Tello.w:
            Tello.sendCommand(0, 0, 0, (int)(Tello.GUID_YAW_SPEED/3))
        else:
            Tello.sendCommand(0, 0, 0, (int)(-Tello.GUID_YAW_SPEED/3))
        Timer.start()
        while Timer.elapsed() <= Tello.T_YAW_360/4:
            if Tello.info[1] == Tello.TELLO_CABIN:
                Tello.sendCommand(0, 0, 0, 0)
                Track.TRACK_STATE = Track.TRACK_CABIN
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Tello.sendCommand(0, 0, 0, 0)
        Timer.end()
        # 再上下
        if Track.ly < (1 - border)*Tello.h:
            Tello.sendCommand(0, 0, (int)(Tello.GUID_3D_SPEED/2), 0)
        else:
            Tello.sendCommand(0, 0, (int)(-Tello.GUID_3D_SPEED/2), 0)
        Timer.start()
        while Timer.elapsed() <= Tello.T_3D_200/2:
            if Tello.info[1] == Tello.TELLO_CABIN:
                Tello.sendCommand(0, 0, 0, 0)
                Track.TRACK_STATE = Track.TRACK_CABIN
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Tello.sendCommand(0, 0, 0, 0)
        Timer.end()

    # 执行结束仍然没有找到，切换回手动模式，发出警告
    Tello.TELLO_STATE = Tello.STATE_MANUAL
    print("Can't find CABIN!")
    # 在视频流上显示
    return

def fromTrackSeat():
    # 最后一次出现在非易失边界中，即视野中间
    if borderSeat*Tello.w <= Track.lx <= (1 - borderSeat)*Tello.w and borderSeat*Tello.h <= Track.ly <= (1 - borderSeat)*Tello.h:
        Timer.start()
        while Timer.elapsed() <= Tello.T_WAIT:
            if Tello.info[1] == Tello.TELLO_SEAT:
                Track.TRACK_STATE = Track.TRACK_SEAT
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Timer.end()
    else:
        lr, ud = 0, 0
        if Track.lx > (1 - borderSeat)*Tello.w:
            lr = (int)(Tello.GUID_3D_SPEED/2)
        else:
            lr = (int)(-Tello.GUID_3D_SPEED/2)
        if Track.ly < (1 - borderSeat)*Tello.h:
            ud = (int)(Tello.GUID_3D_SPEED/2)
        else:
            ud = (int)(-Tello.GUID_3D_SPEED/2)
        Tello.sendCommand(lr, 0, ud, 0)
        Timer.start()
        while Timer.elapsed() <= Tello.T_3D_200/2:
            if Tello.info[1] == Tello.TELLO_SEAT:
                Tello.sendCommand(0, 0, 0, 0)
                Track.TRACK_STATE = Track.TRACK_SEAT
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Tello.sendCommand(0, 0, 0, 0)
        Timer.end()

    # 执行结束仍然没有找到，切换回手动模式，发出警告
    Tello.TELLO_STATE = Tello.STATE_MANUAL
    print("Can't find SEAT!")
    # 在视频流上显示
    return


def fromTrackSwitch():
        # 最后一次出现在非易失边界中，即视野中间
    if border*Tello.w <= Track.lx <= (1 - border)*Tello.w:
        Timer.start()
        while Timer.elapsed() <= Tello.T_WAIT:
            if Tello.info[1] != 0:
                Track.TRACK_STATE = Track.TRACK_SWITCH
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Timer.end()
    else:
        if Track.lx > (1 - border)*Tello.w:
            Tello.sendCommand((int)(Tello.GUID_3D_SPEED), 0, 0, 0)
        else:
            Tello.sendCommand((int)(-Tello.GUID_3D_SPEED), 0, 0, 0)

        Timer.start()
        while Timer.elapsed() <= Tello.T_3D_200/4:
            if Tello.info[1] != 0:
                Tello.sendCommand(0, 0, 0, 0)
                Track.TRACK_STATE = Track.TRACK_SWITCH
                return
            key = cv2.waitKey(1)
            if key == ord('M'):
                Tello.TELLO_STATE = Tello.STATE_MANUAL
                return
        Tello.sendCommand(0, 0, 0, 0)
        Timer.end()

    # 执行结束仍然没有找到，切换回手动模式，发出警告
    Tello.TELLO_STATE = Tello.STATE_MANUAL
    print("Can't find SEAT!")
    # 在视频流上显示
    return
    


def trackSearch():
    if Tello.PRE_STATE == Tello.STATE_MANUAL:
        # 从手动操控模式进入
        fromManual()
    elif Tello.PRE_STATE == Tello.STATE_TRACK:
        if Track.PRE_STATE == Track.TRACK_CABIN:
            fromTrackCabin()
        elif Track.PRE_STATE == Track.TRACK_SWITCH:
            fromTrackSwitch()
        elif Track.PRE_STATE == Track.TRACK_SEAT or Track.PRE_STATE == Track.TRACK_LAND:
            fromTrackSeat()
        else:
            pass
    else:
        pass