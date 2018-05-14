from dga.problem import Problem
from dga import dga

tolerance = 1e-3

def test_example_quadratic1():
    def J(x):
        return x ** 2

    prob = Problem('quad')
    prob.Cost(J)
    prob.State('x', lower_bound=-2, upper_bound=2, bits=12)
    GA = dga(options=[0, 0.9, None, None, None, None, None, None, None, None, None, None, None, 200])
    xopt = GA(prob)
    assert abs(xopt['xopt'][0]) < tolerance

def test_example_quadratic2():
    def J(x, y):
        return x ** 2 + y ** 2

    prob = Problem('quad')
    prob.Cost(J)
    prob.State('x', lower_bound=-2, upper_bound=2, bits=12)
    prob.State('y', lower_bound=-2, upper_bound=2, bits=12)
    GA = dga(options=[0, 0.9, None, None, None, None, None, None, None, None, None, None, None, 200])
    xopt = GA(prob)
    assert abs(xopt['xopt'][0]) < tolerance
    assert abs(xopt['xopt'][1]) < tolerance

def test_example_quadratic3():
    def J(x, y):
        return x ** 2 + y ** 2

    prob = Problem('quad')
    prob.Cost(J)
    prob.State('x', lower_bound=-2, upper_bound=2, bits=4)
    prob.State('y', lower_bound=-2, upper_bound=2, bits=4)
    GA = dga(options=[0, 0.9, None, None, None, None, None, None, None, None, None, None, None, 200])
    xopt = GA(prob)
    assert abs(xopt['xopt'][0]) - 0.1333 < tolerance
    assert abs(xopt['xopt'][1]) - 0.1333 < tolerance