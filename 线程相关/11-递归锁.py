"""
如果你想让只有拿到锁的线程才能释放该锁，那么应该使用 RLock() 对象。
和 Lock() 对象一样， RLock() 对象有两个方法： acquire() 和 release() 。
当你需要在类外面保证线程安全，又要在类内使用同样方法的时候 RLock() 就很实用了。

（译者注：RLock原作解释的太模糊了，译者在此擅自添加一段。
RLock其实叫做“Reentrant Lock”，就是可以重复进入的锁，也叫做“递归锁”。这种锁对比Lock有是三个特点：

    1. 谁拿到谁释放。如果线程A拿到锁，线程B无法释放这个锁，只有A可以释放；
    2. 同一线程可以多次拿到该锁，即可以acquire多次；
    3. acquire多少次就必须release多少次，只有最后一次release才能改变RLock的状态为unlocked）
"""
import threading
import time


class Box(object):
    lock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.lock.acquire()
        self.total_items += n
        Box.lock.release()

    def add(self):
        Box.lock.acquire()
        self.execute(1)
        print(self.total_items)
        Box.lock.release()

    def remove(self):
        Box.lock.acquire()
        self.execute(-1)
        print(self.total_items)
        Box.lock.release()


# 这两个函数在单独的线程中运行n并调用Box的方法
def adder(box, items):
    while items > 0:
        print("adding 1 item in the box")
        box.add()
        time.sleep(1)
        items -= 1


def remover(box, items):
    while items > 0:
        print("removing 1 item in the box")
        box.remove()
        time.sleep(1)
        items -= 1


# 主程序构建一些线程，并确保它可以工作
if __name__ == "__main__":
    items = 3
    print("putting %s items in the box " % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("\n%s items still remain in the box " % box.total_items)
