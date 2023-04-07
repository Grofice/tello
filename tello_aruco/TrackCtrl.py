import cv2
import Track
import Tello
from TrackSearch import trackSearch
from TrackCabin import trackCabin
from TrackSwitch import trackSwitch
from TrackSeat import trackSeat

def trackTarget():
    while True:
        # H_tello.me.get_battery()
        key = cv2.waitKey(1)
       
        if key == ord('Q'):
            Tello.TELLO_STATE = Tello.EMERGENCY_STOP
            if Tello.telloVideo and Tello.telloTakeoff:
                Tello.me.land()
            break
        if key == ord('M'):
            Tello.TELLO_STATE = Tello.STATE_MANUAL
            break

        if key == ord('Z'):
            Track.TRACK_STATE = Track.TRACK_CABIN
        if key == ord('X'):
            Track.TRACK_STATE = Track.TRACK_SWITCH
        if key == ord('C'):
            Track.TRACK_STATE = Track.TRACK_SEAT
        if key == ord('V'):
            Track.TRACK_STATE = Track.TRACK_LAND


        # if key == ord('N'):
        #     Track.TRACKCabin.N = Track.TRACKCabin.N + 1

        if Tello.TELLO_STATE == Tello.STATE_TRACK:
            if Track.TRACK_STATE == Track.TRACK_SEARCH:
                print("----------Searching-------------")
                Tello.TEXT = "Searching"
                trackSearch()
            elif Track.TRACK_STATE == Track.TRACK_CABIN:
                # print("----------TRACKing cabin-------------")
                # Tello.TEXT = "Tracking Cabin"
                trackCabin()
            elif Track.TRACK_STATE == Track.TRACK_SWITCH:
                print("----------Switching-------------")
                Tello.TEXT = "Switching"
                trackSwitch()
            elif Track.TRACK_STATE == Track.TRACK_SEAT or Track.TRACK_STATE == Track.TRACK_LAND:
                # print("----------TRACKing seat-------------")
                if Track.TRACK_STATE == Track.TRACK_LAND:
                    Tello.TEXT = "Auto Landing"
                else:
                    Tello.TEXT = "Tracking Seat"
                trackSeat()
        else:
            Track.TRACK_STATE = Track.TRACK_SEARCH
            break






        # elif H_Track.Track.Track.TRACK_STATE == Track.TRACK_SWITCHING:
            # id = H_tello.info[1]
            # if(H_tello.telloTakeoff and id == 0 and H_tello.me.get_distance_tof() <= 10):
            #     H_tello.me.emergency()
            #     # H_tello.sendCommand(0, 0, 0, 100)
            #     H_tello.TELLO_STATE = H_tello.STATE_LAND
            # if(id == H_tello.TELLO_SEAT):
            #     H_Track.Track.Track.TRACK_STATE = Track.TRACK_SEAT
            # elif id == 0:
            #     H_tello.sendCommand(0, 0, 0, -5)
            # else:
            # # 未识别到任何机位
            # if id == 0: