# -*- coding:utf-8 -*-
import threading
import time


def open():
    print('人数够了， 开门!')


barrier = threading.Barrier(3, open)


class Customer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = 3

    def run(self):
        while self.n > 0:
            self.n -= 1
            print('{0}在等着开门.'.format(self.name))
            try:
                barrier.wait(10)
            except threading.BrokenBarrierError:
                time.sleep(1)
                print("--->>> {}遭遇了一个破损态\n".format(self.name))
                time.sleep(1)
                continue
            print('开门了， go go go')
            time.sleep(3)


class Manager(threading.Thread):
    def run(self):
        print('前面{}个排队的不算，重新来'.format(barrier.n_waiting))
        # 这里虽然重置了障碍对象中的线程初始状态，但是ab已经走了一次循环，最后c会出现一次单独的破损态
        barrier.reset()
        """重置栅栏为默认的初始态。
        如果栅栏中仍有线程等待释放，这些线程将会收到 BrokenBarrierError 异常。

        注意使用此函数时，如果有某些线程状态未知，则可能需其它的同步来确保线程已被释放。
        如果栅栏进入了破损态，最好废弃它并新建一个栅栏。"""


if __name__ == '__main__':
    t1 = Customer(name='A')
    t2 = Customer(name='B')
    t3 = Customer(name='C')
    tm = Manager()
    t1.start()
    t2.start()
    tm.start()
    t3.start()
