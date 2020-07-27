import queue
import threading


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(item, threading.current_thread().name, "\n")
        q.task_done()


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
