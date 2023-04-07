import time

timerOpen = False

startTime = 0

def start():
    global startTime, timerOpen
    startTime = time.time()
    timerOpen = True

def elapsed():
    return time.time() - startTime

def end():
    global startTime, timerOpen
    startTime = 0
    timerOpen = False

if __name__ == '__main__':
    startt = time.time()
    start()
    while elapsed() <= 5:
        print("loading")
    print(time.time()-startt)
    print(elapsed())