from dga import dga

tolerance = 1e-2

def test_example_quadratic1():
    def J(x):
        return x ** 2

    xopt = dga.solve(J, [-2], [2], [12])
    assert abs(xopt['x'][0]) < tolerance

def test_example_quadratic2():
    def J(x, y):
        return x ** 2 + y ** 2

    xopt = dga.solve(J, [-2, -2], [2, 2], [12, 12])
    assert abs(xopt['x'][0]) < tolerance
    assert abs(xopt['x'][1]) < tolerance

def test_example_quadratic3():
    def J(x, y):
        return x ** 2 + y ** 2

    xopt = dga.solve(J, [-2, -2], [2, 2], [4, 4])
    assert abs(xopt['x'][0]) - 0.1333 < tolerance
    assert abs(xopt['x'][1]) - 0.1333 < tolerance