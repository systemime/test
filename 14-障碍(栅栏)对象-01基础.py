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


# 3个线程上线，运行函数open
barrier = threading.Barrier(3, action=open, timeout=None)
# 创建一个需要 parties 个线程的栅栏对象。如果提供了可调用的 action 参数，
# 它会在所有线程被释放时在其中一个线程中自动调用。
# timeout 是默认的超时时间，如果没有在 wait() 方法中指定超时时间的话。


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
                """如果创建栅栏对象时在构造函数中提供了action 参数，它将在其中一个线程释放前被调用。
                如果此调用引发了异常，栅栏对象将进入损坏态。
                ，或重置栅栏时仍有线程等待释放，将会引发 BrokenBarrierError 异常。"""
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
