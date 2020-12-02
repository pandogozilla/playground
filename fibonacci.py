#!/bin/env python3

# 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

def fib(n):
	assert type(n) == int
	c, a, e, s = abs(n), abs(n), (1, 1), (2, 0)
	add = lambda a, b, p, q: ((a*p+5*b*q)//2, (a*q+b*p)//2)
	dbl = lambda a, b, p: (5*b*b+2*p, a*b)
	while c > 0:
		if c % 2 == 1:
			s = add(*e, *s)
		e = dbl(*e, 1 if c < a else -1)
		c = c // 2
	return -s[1] if n < 0 and a%2 == 0 else s[1]

n = 5000000
with open('f%d.txt'%n, 'wt') as f:
	f.write(str(fib(n)))
