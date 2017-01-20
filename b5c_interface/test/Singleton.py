# -*- coding: utf-8 -*-


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_the_instance'):
            cls._the_instance=object.__new__(cls,*args, **kwargs)
            print 'not init'
        else:
            print 'has init'
        return cls._the_instance


class A(Singleton):
    print 'init before'

    def __init__(self):
        print 'i am __init__'

    def f(self):
        print 'i am f'

a=A()
b=A()
a.f()
print 'done'

