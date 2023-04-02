from threading import Thread
import threading
from time import sleep, ctime
import cv2 as cv

# def ShowText(img):
#     cv.putText(img,'this is a picture',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)

# def ShowImage(filename):
#     img = cv.imread(filename)
#     t = Thread(target=ShowText,args=(img))
#     t.start()
#     t.join()
#     cv.imshow('img',img)
#     key = cv.waitKey(5000)
#     cv.destroyAllWindows()

# if __name__ == '__main__':
#     ShowImage('image_01.png')

class myThread(threading.Thread):
