import cv2 as cv
import time

key = 0

start = time.perf_counter()

while key & 0xFF != 27:
    img = cv.imread('detect.png')
    end = time.perf_counter()
    timen = end - start
    if timen<1.1:
        cv.putText(img,'I am a hot dog',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)

    cv.imshow('img',img)
    key = cv.waitKey(500)

cv.destroyAllWindows()