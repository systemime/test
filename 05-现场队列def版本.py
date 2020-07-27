import queue
import sys
import threading
import time

threadList = ["线程-1", "线程-2", "线程-3", "线程-4", "线程-5", "线程-6"]
nameList = ["One", "Two", "Three", "Four", "Five", "six", "server", "eng"]

exitFlag = 0

# 定义锁
queueLock = threading.Lock()
# 10个队列
workQueue = queue.Queue(8)
# 线程列表
threads = []
# 线程id
threadID = 1


def process_data():
    while True:
        queueLock.acquire()
        # 如果队列为空，返回True,反之False
        if not workQueue.empty():
            data = workQueue.get()
            queueLock.release()
            # None是队列里的信号量，应该使用真正的信号量去处理这个地方
            if data is None:
                break
            # 返回当前对应调用者的控制线程的 Thread 对象。如果调用者的控制线程不是利用 threading 创建，会返回一个功能受限的虚拟线程对象
            print("%s %s processing %s\n" % (threading.current_thread().name, threading.current_thread().ident, data))
            workQueue.task_done()
            """
            表示前面排队的任务已经被完成。被队列的消费者线程使用。每个 get() 被用于获取一个任务， 后续调用 task_done() 告诉队列，该任务的处理已经完成。

            如果 join() 当前正在阻塞，在所有条目都被处理后，将解除阻塞(意味着每个 put() 进队列的条目的 task_done() 都被收到)。

            如果被调用的次数多于放入队列中的项目数量，将引发 ValueError 异常 。
            """
        else:
            queueLock.release()
            pass


for i in threadList:
    t = threading.Thread(target=process_data, name=i)
    print("启动线程：", i)
    t.start()
    threads.append(t)

# 等待线程全部启动
time.sleep(2)

workQueue.join()
"""
阻塞至队列中所有的元素都被接收和处理完毕。

当条目添加到队列的时候，未完成任务的计数就会增加。每当消费者线程调用 task_done() 表示这个条目已经被回收，该条目所有工作已经完成，未完成计数就会减少。当未完成计数降到零的时候， join() 阻塞被解除。
"""

print("写入队列")
# 去除锁观察竞争状态
# queueLock.acquire()
for word in nameList:
    workQueue.put(word)
# queueLock.release()

print("等待队列清空")

for i in range(len(threads)):
    workQueue.put(None)
for t in threads:
    t.join()
print("全部线程退出")

