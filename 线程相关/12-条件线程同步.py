"""
请配合./真实案例/3个线程顺序打印abc
"""
import threading
import time


# 创建条件对象
con = threading.Condition()
# 创建线程变量
sum = threading.local()
num = 1


def produce():
    with con:
        global num
        sum.n = 666
        print('厨师开始做鱼丸了！共计666个鱼丸')
        while 1:
            num += 1
            sum.n -= 1
            if sum.n >= 0 and num < 5:
                print("锅里有{}个鱼丸，库存还剩{}个".format(num, sum.n))
            elif num == 5:
                print("锅里有{}个鱼丸，库存还剩{}个\n可以吃饭了".format(num, sum.n))
                con.notify_all()
                # 超时没有消费者结束线程
                con.wait(timeout=3)
            else:
                print("本店打烊了，吃完赶紧走吧")
                con.notify_all()
                break


def consume():
    sum.n = 0

    while 1:
        with con:
            global num
            if num > 0:
                sum.n += 1
                if sum.n == 5:
                    print("{}吃了一个鱼丸, 火锅里的鱼丸数量为{}个\n{}说：吃饱了不吃了".format(threading.current_thread().name, num, threading.current_thread().name))
                    con.notify_all()
                    break
                num -= 1
                print('{}吃了一个鱼丸，火锅里的鱼丸数量为{}个'.format(threading.current_thread().name, num))
        with con:
            if num <= 0:
                print('{}说：没吃的了，赶紧加鱼丸吧'.format(threading.current_thread().name))
                con.notify_all()
                con.wait()


if __name__ == '__main__':
    import datetime
    start_time = datetime.datetime.now()
    cons = ['吃货1', '吃货2', '吃货3', '吃货4', '吃货5', '吃货6', '吃货7']
    threads = []
    for k, c in enumerate(cons):
        threads.append(threading.Thread(target=consume, name=c))
        threads[k].start()
    p = threading.Thread(target=produce, name="厨师")
    p.start()
    p.join()
    for c in threads:
        c.join()

    end_time = datetime.datetime.now()
    print(start_time, end_time)
