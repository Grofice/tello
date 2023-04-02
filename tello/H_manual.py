import cv2
from H_tello import sendCommand, TELLO_STATE, STATE_MANUAL, STATE_TRACK, STATE_LAND
import H_tello
speed = 50


def manualControl():
    while True:
        # H_tello.me.get_battery()


        lr, fb, ud, yaw = 0, 0, 0, 0

        key = cv2.waitKey(1)
        if key == ord('R'):
            H_tello.TELLO_STATE = STATE_LAND
            break
        if key == ord('R'):
            H_tello.TELLO_STATE = STATE_TRACK
            break
        if key == ord('Q'):
            H_tello.TELLO_STATE = H_tello.EMERGENCY_STOP
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
        print("lr: %4d | fb: %4d | ud: %4d | yaw: %4d" % (lr, fb, ud, yaw))
    sendCommand(0, 0, 0, 0)