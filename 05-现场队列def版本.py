import queue
import threading
import time

threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6"]
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
    global queueLock
    global exitFlag
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = workQueue.get()
            queueLock.release()
            print("%s %s processing %s\n" % (threading.current_thread().name, threading.current_thread().ident, data))
        else:
            queueLock.release()


for i in threadList:
    t = threading.Thread(target=process_data, name=i)
    print("启动线程：", i)
    t.start()
    threads.append(t)

# 等待线程全部启动
time.sleep(2)

print("写入队列")
# 去除锁观察竞争状态
# queueLock.acquire()
for word in nameList:
    workQueue.put(word)
# queueLock.release()

print("等待队列清空")
while workQueue.empty():
    pass

exitFlag = 0

print("等待线程结束")
for t in threads:
    t.join()

