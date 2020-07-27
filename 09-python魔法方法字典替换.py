from threading import current_thread


class A:
    def __new__(cls, *args, **kw):
        self = object.__new__(cls)
        setattr(cls, '_local__args', (args, kw))
        return self

    def __init__(self, *args, **kw):
        self.shared_x = kw["shared_x"]
        self.shared_y = kw["shared_y"]

    def substitute(self, d):
        object.__setattr__(self, '__dict__', d)
        cls = type(self)
        if cls.__init__ is not object.__init__:
            print("7---------------")
            args, kw = getattr(self, '_local__args')
            cls.__init__(self, *args, **kw)


a = A(shared_x=111, shared_y=222)
a.y = 3
old_dict = a.__dict__
print("01--", old_dict)
d = {'x': 1}
a.substitute(d)
print("02--", a.__dict__)
a.y = 777
print("03--", a.__dict__)
print("04--", d)
print("06--", old_dict)


class A:
    def substitute(self, d):
        object.__setattr__(self, '__dict__', d)


a = A()
a.y = 3
old_dict = a.__dict__
print(old_dict)
d = {'x': 1}
a.substitute(d)
print(a.__dict__)
a.y = 777
print(a.__dict__)
print(d)
