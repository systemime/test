"""
栅栏类提供一个简单的同步原语，用于应对固定数量的线程需要彼此相互等待的情况。

线程调用 wait() 方法后将阻塞，直到所有线程都调用了 wait() 方法。此时所有线程将被同时释放。

栅栏对象可以被多次使用，但进程的数量不能改变。
"""
# -*- coding:utf-8 -*-
import threading
import time


def open():
    print('人数够了， 开门!')


barrier = threading.Barrier(3, action=open, timeout=None)


class Customer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = 3

    def run(self):
        while self.n > 0:
            self.n -= 1
            print('{0}在等着开门.'.format(self.name))
            try:
                barrier.wait(2)
            except threading.BrokenBarrierError:
                pass
            print('开门了， go go go')


if __name__ == '__main__':
    t1 = Customer(name='A')
    t2 = Customer(name='B')
    t3 = Customer(name='C')
    t1.start()
    t2.start()
    t3.start()
