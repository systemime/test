import types
import time

@types.coroutine
def switch():
    yield 5
    time.sleep(1)

async def func1():
    print("func1 start")
    await switch()
    print("func1 e")
    await switch()
    print("func1 end")

async def func2():
    print("func2 start")
    print("func2 a")
    await switch()
    print("func2 b")
    print("func2 c")
    await switch()
    print("func2 end")

def run(task_list):
    coro_list = list(task_list)

    while coro_list:
        for coro in list(coro_list):
            try:
                coro.send(None)
            except StopIteration:
                coro_list.remove(coro)

f1 = func1()
f2 = func2()

run([f1, f2])
