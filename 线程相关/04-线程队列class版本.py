import queue
import threading
import time

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s\n" % (threadName, data))
        else:
            queueLock.release()
        # time.sleep(1)


threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6"]
nameList = ["One", "Two", "Three", "Four", "Five", "six", "server", "eng"]
# 定义锁
queueLock = threading.Lock()
# 10个队列
workQueue = queue.Queue(8)
# 线程列表
threads = []
# 线程id
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 等待线程全部启动，便于观察线程竞争
time.sleep(2)

# 获得锁，操作nameList
queueLock.acquire()
for word in nameList:
    # 写入队列
    workQueue.put(word)
# 释放锁
queueLock.release()

# 等待队列清空
# 如果队列为空，返回True,反之False
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")
