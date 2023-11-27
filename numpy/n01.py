import numpy as np
print(np.__version__)
def python_sum(n):
    a=[i**2 for i in range(n)]
    b=[i**3 for i in range(n)]
    c=[]
    for i in range(n):
        c.append(a[i] + b[i])
    return c
# print(python_sum(200))

def numpy_sum(n):
    a = np.arange(n)**2
    b = np.arange(n)**3
    return a+b
lst = [i*i for i in range(1,101)]
a = [i for i in range(40,56)]
b= [i for i in range(56,90)]
c = [i for i in range(90,130)]
print(a)
print(b)
print(c)
