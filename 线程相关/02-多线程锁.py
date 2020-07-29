import threading
import time
import os
import random


def booth(tid):
    global i
    global lock
    while True:
        # 获取锁
        lock.acquire()
        if i != 0:
            i = i - 1
            print("窗口:", tid, ",剩余票数:", i)
            # time.sleep(0.5)
        else:
            print("Thread_id", tid, "No more tickets")
            os._exit(0)
        # 释放锁
        lock.release()
        time.sleep(0.1)


i = 10
lock = threading.Lock()
threads = []

for k in range(10):
    threads.append(threading.Thread(target=booth, args=(k,)))
    threads[k].start()