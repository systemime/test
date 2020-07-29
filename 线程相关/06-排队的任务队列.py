import queue
import threading


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(item, threading.current_thread().name, "\n")
        q.task_done()
        """
        表示前面排队的任务已经被完成。被队列的消费者线程使用。每个 get() 被用于获取一个任务， 后续调用 task_done() 告诉队列，该任务的处理已经完成。

        如果 join() 当前正在阻塞，在所有条目都被处理后，将解除阻塞(意味着每个 put() 进队列的条目的 task_done() 都被收到)。

        如果被调用的次数多于放入队列中的项目数量，将引发 ValueError 异常 。
        """


q = queue.Queue()
threads = []
lock = threading.Lock()

for i in range(5):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

lock.acquire()
for item in range(5):
    q.put(item)
lock.release()

# block until all tasks are done
q.join()

# stop workers
for i in range(5):
    q.put(None)
for t in threads:
    t.join()
