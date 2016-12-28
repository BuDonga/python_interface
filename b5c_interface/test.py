import test


class a:
    def __init__(self):
        print 'a.init'
        self.c = 'nihao'

    def printa(self):
        print 'aaaaa'

    def printb(self):
        print 'bbbb'

class b(test.a):
    def __init__(self):
        test.a.__init__(self)

    def printa(self):
        print 'bbbb'


if __name__ == '__main__':
    d = b()
    d.printa()
    d.printb()
    print d.c
