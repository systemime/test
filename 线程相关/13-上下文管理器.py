"""
支持上下文管理器的状态
  - Lock
  - RLock
  - Condition
  - Semaphore
"""

import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


def threading_with(statement):
    with statement:
        logging.debug('%s 通过with获取' % statement)


def threading_not_with(statement):
    statement.acquire()
    try:
        logging.debug('%s 直接获取' % statement)
    finally:
        statement.release()


if __name__ == '__main__':
    # let's create a test battery
    # 创建一个锁
    lock = threading.Lock()
    # 创建一个递归锁
    rlock = threading.RLock()
    # 创建一个条件对象
    condition = threading.Condition()
    # 创建一个信号量对象
    mutex = threading.Semaphore(1)
    # 创建一个线程同步列表
    threading_synchronization_list = [lock, rlock, condition, mutex]
    # in the for cycle we call the threading_with e threading_no_with function
    for statement in threading_synchronization_list:
        t1 = threading.Thread(target=threading_with, args=(statement,))
        t2 = threading.Thread(target=threading_not_with, args=(statement,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
