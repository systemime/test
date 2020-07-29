from threading import Timer


def fun():
    print("OK")


t = Timer(5, fun)

t.start()
