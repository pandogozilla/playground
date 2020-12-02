#!/bin/env python3

# 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

def fib(n):
	assert type(n) == int
	c, e, s = abs(n), (1 if n > 0 else -1, 1), (2, 0)
	add = lambda a, b, p, q: ((a*p+5*b*q)//2, (a*q+b*p)//2)
	while c > 0:
		if c % 2 == 1:
			s = add(*e, *s)
		e = add(*e, *e)
		c = c // 2
	return s[1]

n = 5000000
with open('f%d.txt'%n, 'wt') as f:
	f.write(str(fib(5000000)))
