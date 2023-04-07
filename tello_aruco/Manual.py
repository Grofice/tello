import cv2
from Tello import sendCommand, TELLO_STATE, STATE_MANUAL, STATE_TRACK, STATE_LAND
import Tello
import Track
import time
speed = 100


def manualControl():
    while True:
        lr, fb, ud, yaw = 0, 0, 0, 0

        key = cv2.waitKey(1)
        if key == ord('B'):
            if (not Tello.telloTakeoff) and Tello.telloVideo:
                Tello.me.takeoff()
                print(Tello.me.get_battery())
                print("----------TELLO TAKEOFF-------------")
            Tello.telloTakeoff = True
        # if key == ord('R'):
        #     Tello.TELLO_STATE = STATE_LAND
        #     break
        if key == ord('T'):
            Tello.PRE_STATE = Tello.STATE_MANUAL
            Tello.TELLO_STATE = STATE_TRACK
            if Tello.AUTO_SE:
                Track.TRACK_STATE = Track.TRACK_SEARCH
            else:
                Track.TRACK_STATE = Track.TRACK_CABIN
            break
        if key == ord('Q'):
            Tello.TELLO_STATE = Tello.EMERGENCY_STOP
            break

        if key == ord('W'):
            ud = speed
        elif key == ord('S'):
            ud = -speed

        if key == ord('A'):
            yaw = -speed
        elif key == ord('D'):
            yaw = speed

        if key == 56:
            fb = speed
        elif key == 50:
            fb = -speed

        if key == 52:
            lr = -speed
        elif key == 54:
            lr = speed

        sendCommand(lr, fb, ud, yaw)
        # if lr != 0 or fb != 0 or ud != 0 or yaw != 0:
        #     print("lr: %4d | fb: %4d | ud: %4d | yaw: %4d" % (lr, fb, ud, yaw)) 
        time.sleep(0.1)
    sendCommand(0, 0, 0, 0)