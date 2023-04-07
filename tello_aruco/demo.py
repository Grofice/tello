from djitellopy import tello
import Timer

# import math
me = tello.Tello()
me.connect()
# print(me.query_sdk_version())
# while True:
#     print(me.get_distance_tof())
#     # me.send_rc_control(0, 0, 0, 0)

# print(1/2)
me.takeoff()
me.send_rc_control(0, 0, 0, 60)
Timer.start()
while Timer.elapsed() <= 6:
    print(Timer.elapsed())
me.land()



# fbRange = [50,60]
# pid = [0.4, 0.4, 0]
# pEyaw = 0
h = 500
# YT = h // 3
YT = 467
# CID = H_tello.TELLO_CABIN
# SID = H_tello.TELLO_SEAT
# N = SID - CID
N = 2
udTarget = YT - (N - 1) / N * (YT
                                - h // 2) 
udTarget = h // 2 + (YT - h // 2) / N
# print()
# print(udTarget)


x1, y1, x2, y2 = 1, 1, 1, 0
angle =  math.atan2((y2-y1), (x2-x1))
theta = angle*( 180 /math.pi)
eyaw = theta - 90
print(angle)
print(theta)
print(eyaw)
