from dga import dga

def J(x,y):
    return x**2 + y**2

xopt = dga(J, [-2, -2], [2, 2], [8, 8])
print(xopt)