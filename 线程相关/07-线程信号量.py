# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import random

# The optional argument gives the initial value for the internal
# counter;
# it defaults to 1.
# If the value given is less than 0, ValueError is raised.
semaphore = threading.Semaphore(0)

# 信号量解锁信号量增加1，获取减少1

# 消费者
def consumer():
    print("consumer is waiting.")
    # Acquire a semaphore
    # 信号量减少
    semaphore.acquire()
    # The consumer have access to the shared resource
    print("Consumer notify : consumed item number %s " % item)


# 生产者
def producer():
    global item
    time.sleep(2)
    # create a random item
    item = random.randint(0, 1000)
    print("pro : 生产者生产内容为 %s" % item)
    # 释放信号量，使内部计数器增加一。
    # 当入口为零时，另一个线程正在等待它再次变得大于零，请唤醒该线程。
    # 提高信号量计数
    semaphore.release()


if __name__ == '__main__':
    for i in range(0, 5):
        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print("program terminated")
