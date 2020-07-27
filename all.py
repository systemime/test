import time
import sys
import threading
import random


# 生产者
def produce(l):
    global lock
    i = 0
    while 1:
        if i < 5:
            lock.acquire()
            l.append(i)
            lock.release()
            yield i
            i = i + 1
            time.sleep(random.randint(0, 9))
        else:
            return
        # 消费者


def consume(l):
    global lock
    p = produce(l)
    while 1:
        try:
            next(p)
            while len(l) > 0:
                lock.acquire()
                print(l.pop(), threading.current_thread().name)
                lock.release()
        except StopIteration:
            sys.exit(0)


lock = threading.Lock()
l = []

if __name__ == "__main__":
    t1 = threading.Thread(target=consume, args=(l,), name="t1")
    t2 = threading.Thread(target=consume, args=(l,), name="t2")
    t3 = threading.Thread(target=consume, args=(l,), name="t3")
    t4 = threading.Thread(target=consume, args=(l,), name="t4")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
