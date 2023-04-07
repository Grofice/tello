import cv2 as cv 
import time 
from threading import Thread

class WebcamStream :
    def __init__(self, stream_id=0):
        # stream_id=0时为本地摄像头
        self.stream_id = stream_id 
        
        # 获取视频流
        self.vcap = cv.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of webcam hardware/input stream: {}".format(fps_input_stream))
            
        # 读取单帧
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)

        # 读取下一帧的时候stopped为False
        self.stopped = True 
 
        self.t = Thread(target=self.update, args=())
        # 线程daemon执行
        self.t.daemon = True 
        
    # 开始线程
    def start(self):
        self.stopped = False
        self.t.start()

    # 读下一帧 
    def update(self):
        while True :
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # 返回最后读取的帧 
    def read(self):
        return self.frame

    # 停止线程 
    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    # 创建一个Webstream类
    webcam_stream = WebcamStream(stream_id=0)

    # 将webcam_stream.stopped置为False
    # 开启线程 t，用于执行update操作
    webcam_stream.start()

    # num_frames_processed为已经处理的画面帧数
    num_frames_processed = 0

    # 开始计时
    start = time.time()
    while True :
        if webcam_stream.stopped is True:
            break
        else :
            # 读取帧
            frame = webcam_stream.read()

        # 设置延迟以处理帧
        # 单位：s 
        delay = 0.03
        time.sleep(delay) 

        num_frames_processed += 1

        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key & 0xFF == 27:
            break

        elif key & 0xFF == ord('w'):
            # start_w = time.time()
            tmp = num_frames_processed
            while True:
                if webcam_stream.stopped is True:
                    break;
                else:
                    frame = webcam_stream.read()
                
                delay = 0.01
                time.sleep(delay) 
                num_frames_processed += 1
                print(num_frames_processed)
                cv.putText(frame,'I want become a better one',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
                cv.imshow('frame', frame)
                # delay = 0.01
                # time.sleep(delay)
                # end_w = time.time()

                if num_frames_processed-tmp > 700:
                    break

        elif key & 0xFF == ord('s'):
            cv.putText(frame,'you have a great opinion',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
            cv.imshow('frame', frame)
            delay = 0.03
            time.sleep(delay) 

    end = time.time()
    webcam_stream.stop() 

    elapsed = end-start
    fps = num_frames_processed/elapsed 
    print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(fps, elapsed, num_frames_processed))

    cv.destroyAllWindows()
