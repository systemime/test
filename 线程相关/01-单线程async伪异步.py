import types
import time


"""
用@asyncio.coroutine装饰的基于生成器的协程将对asyncio.iscoroutinefunction()测试True，而用@types.coroutine装饰的协程将测试False。

此函数可将 generator 函数转换为返回基于生成器的协程的 coroutine function。 
基于生成器的协程仍然属于 generator iterator，但同时又可被视为 coroutine 对象兼 awaitable。 
不过，它没有必要实现 __await__() 方法。

如果 gen_func 是一个生成器函数，它将被原地修改。

如果 gen_func 不是一个生成器函数，则它会被包装。 
如果它返回一个 collections.abc.Generator 的实例，该实例将被包装在一个 awaitable 代理对象中。 所有其他对象类型将被原样返回。

new 3.5
"""
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
