# -*- coding: utf-8 -*-
import sys
from functools import reduce

f = lambda x: 2 * x
iterable = [1,2,3,4,4,5,6,7]
v = map(f, iterable)
print v
b = [c * 2 for c in iterable]
print b

def a(x):
    return 2 * x
w = map(a, iterable)
print w

d = lambda x, y: x * y

g = reduce(d, iterable)
print g