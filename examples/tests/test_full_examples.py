from dga import dga

tolerance = 1e-2

def test_example_quadratic1():
    def J(x):
        return x ** 2

    xopt = dga(J, [-2], [2], [12], display_flag=0)
    assert abs(xopt['xopt'][0]) < tolerance

def test_example_quadratic2():
    def J(x, y):
        return x ** 2 + y ** 2

    xopt = dga(J, [-2, -2], [2, 2], [12, 12], display_flag=0)
    assert abs(xopt['xopt'][0]) < tolerance
    assert abs(xopt['xopt'][1]) < tolerance

def test_example_quadratic3():
    def J(x, y):
        return x ** 2 + y ** 2

    xopt = dga(J, [-2, -2], [2, 2], [4, 4], display_flag=0)
    assert abs(xopt['xopt'][0]) - 0.1333 < tolerance
    assert abs(xopt['xopt'][1]) - 0.1333 < tolerance