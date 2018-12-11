from .Gene import Gene

class Problem(object):
    ''' Defines the problem settings. '''
    def __new__(cls, *args, **kwargs):
        obj = super(Problem, cls).__new__(cls)
        obj.parameters = []
        obj.costs = []
        obj.states = []

        return obj

    def cost(self, equation='', unit='nd'):
        return self.costs.append(Expression(equation, unit=unit))

    def state(self, *args, **kwargs):
        return self.states.append(Gene(*args, **kwargs))
