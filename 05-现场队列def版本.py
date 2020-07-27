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
            print("%s %s processing %s\n" % (threading.current_thread().name, threading.current_thread().ident, data))
            workQueue.task_done()
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

