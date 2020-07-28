# -*- coding:utf-8 -*-
import threading
import time
import datetime


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
            print('{0}在等着开门. {1}'.format(self.name, datetime.datetime.now()))
            try:
                barrier.wait(10)
            except threading.BrokenBarrierError:
                print('{}觉得今天好像不开门了，回家. {}'.format(threading.current_thread().name, datetime.datetime.now()))
                continue
            print('{}: 开门了， go go go  {}'.format(threading.current_thread().name, datetime.datetime.now()))


class Manager(threading.Thread):
    def run(self):
        barrier.reset()
        print('老板跟小姨子跑了，不开门了！  {}'.format(datetime.datetime.now()))


if __name__ == "__main__":
    t1 = Customer(name='A')
    t2 = Customer(name='B')
    t3 = Customer(name='C')
    tm = Manager()
    t1.start()
    t2.start()
    tm.start()
    t3.start()
