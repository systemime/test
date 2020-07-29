import threading
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()


@contextmanager
def acquire(*locks):
    # 按对象标识符对锁进行排序
    locks = sorted(locks, key=lambda x: id(x))

    # 确保不违反先前获取的锁的锁顺序
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # 获取所有锁
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]
#
#
# import threading
#
# x_lock = threading.Lock()
# y_lock = threading.Lock()
#
#
# def thread_1():
#     while True:
#         with acquire(x_lock, y_lock):
#             print('Thread-1')
#
#
# def thread_2():
#     while True:
#         with acquire(y_lock, x_lock):
#             print('Thread-2')
#
#
# t1 = threading.Thread(target=thread_1, name="t1")
# t1.daemon = True
# t1.start()
#
# t2 = threading.Thread(target=thread_2, name="t2")
# t2.daemon = True
# t2.start()

import threading
x_lock = threading.Lock()
y_lock = threading.Lock()


def thread_1():

    while True:
        with acquire(x_lock):
            with acquire(y_lock):
                print('Thread-1')


def thread_2():
    while True:
        with acquire(y_lock):
            with acquire(x_lock):
                print('Thread-2')


t1 = threading.Thread(target=thread_1)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()
