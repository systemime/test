"""
事件是线程之间用于通讯的对象。有的线程等待信号，有的线程发出信号。

基本上事件对象都会维护一个内部变量

class threading.Event
实现事件对象的类。事件对象管理一个内部标志，调用 set() 方法可将其设置为true。
调用 clear() 方法可将其设置为false。调用 wait() 方法将进入阻塞直到标志为true。这个标志初始时为false。

在 3.3 版更改: 从工厂函数变为类。

    is_set()
    当且仅当内部旗标为时返回 True。

    set()
    将内部标志设置为true。所有正在等待这个事件的线程将被唤醒。当标志为true时，调用 wait() 方法的线程不会被被阻塞。

    clear()
    将内部标志设置为false。之后调用 wait() 方法的线程将会被阻塞，直到调用 set() 方法将内部标志再次设置为true。

    wait(timeout=None)
    阻塞线程直到内部变量为true。如果调用时内部标志为true，将立即返回。否则将阻塞线程，直到调用 set() 方法将标志设置为true或者发生可选的超时。

    当提供了timeout参数且不是 None 时，它应该是一个浮点数，代表操作的超时时间，以秒为单位（可以为小数）。

    当且仅当内部旗标在等待调用之前或者等待开始之后被设为真值时此方法将返回 True，也就是说，它将总是返回 True 除非设定了超时且操作发生了超时。

在 3.1 版更改: 很明显，方法总是返回 None。
"""
# -*- coding: utf-8 -*-

import time
from threading import Thread, Event
import random

items = []
event = Event()


class consumer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        while True:
            time.sleep(1)
            self.event.wait()
            item = self.items.pop()
            print('Co : %d 已从队列 %s 中移除' % (item, self.name))


class producer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        global item
        for i in range(4):
            time.sleep(1)
            item = random.randint(0, 256)
            self.items.append(item)
            print('Pr : 项目 N° %d 已添加到队列 %s' % (item, self.name))
            self.event.set()
            print('Pr : 设置事件 %s' % self.name)
            self.event.clear()
            print('Pr : 已移除事件 %s' % self.name)


if __name__ == '__main__':
    t1 = producer(items, event)
    t2 = consumer(items, event)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
