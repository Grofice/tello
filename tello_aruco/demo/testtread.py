import threading

def run():
    print("123")



class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # 执行任务
            pass

    def stop(self):
        self._stop_event.set()

if __name__ == '__main__':
    t = MyThread(target=run)
    t.start()

    # 停止线程
    t.stop()

    # 重新启动线程
    t = MyThread()
    t.start()
