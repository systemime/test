"""
条件指的是应用程序状态的改变。这是另一种同步机制，其中某些线程在等待某一条件发生，其他的线程会在该条件发生的时候进行通知。
一旦条件发生，线程会拿到共享资源的唯一权限。


"""
from threading import Thread, Condition
import time

items = []
condition = Condition()


class consumer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def consume(self):
        global condition
        global items
        condition.acquire()
        if len(items) == 0:
            condition.wait()
            print("Co : 没有内容可以消费")
        items.pop()
        print("Co : 消耗内容： " + str(len(items)))

        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 5):
            time.sleep(2)
            self.consume()


class producer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def produce(self):
        global condition
        global items
        # 取得锁
        condition.acquire()
        if len(items) == 10:
            condition.wait()
            """
            等待直到被通知或发生超时。如果线程在调用此方法时没有获得锁，将会引发 RuntimeError 异常。

            这个方法释放底层锁，然后阻塞，直到在另外一个线程中调用同一个条件变量的 notify() 或 notify_all() 唤醒它，
            或者直到可选的超时发生。一旦被唤醒或者超时，它重新获得锁并返回。
            
            当提供了 timeout 参数且不是 None 时，它应该是一个浮点数，代表操作的超时时间，以秒为单位（可以为小数）。
            
            当底层锁是个 RLock ，不会使用它的 release() 方法释放锁，因为当它被递归多次获取时，实际上可能无法解锁。
            相反，使用了 RLock 类的内部接口，即使多次递归获取它也能解锁它。 然后，在重新获取锁时，使用另一个内部接口来恢复递归级别。
            
            返回 True ，除非提供的 timeout 过期，这种情况下返回 False。
            
            在 3.2 版更改: 很明显，方法总是返回 None。
            """
            print("Pr : 生产内容为： " + str(len(items)))
            print("Pr : 停止生产!!")
        items.append(1)
        print("Pr : 生产总数量 " + str(len(items)))
        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 5):
            time.sleep(1)
            self.produce()


if __name__ == "__main__":
    producer = producer()
    consumer = consumer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
