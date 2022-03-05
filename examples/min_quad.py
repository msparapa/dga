import dga
import logging

dga.set_logging_level(logging.DEBUG)

def J(x,y):
    return x**2 + y**2

xopt = dga.solve(J, [-2, -2], [2, 2], [8, 8])
print(xopt)
