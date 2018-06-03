from .Expression import Expression
from .State import State
import re


class Problem(object):
    ''' Defines the problem settings. '''
    def __new__(cls, *args, **kwargs):
        obj = super(Problem, cls).__new__(cls)
        obj.parameters = []
        obj.costs = []
        obj.states = []

        return obj

    @staticmethod
    def _format_name(name):
        '''
        Validates that the name is in the right format
        Only alphabets, numbers and underscores allowed
        Should not start with a number or underscore
        '''
        name = name.replace(' ','_')
        if re.match(r'[a-zA-Z]\w+',name):
            return name
        else:
            raise ValueError("""Invalid problem name specified.
            Only alphabets, numbers and underscores allowed
            Should start with an alphabet""")

    def cost(self, equation='', unit='nd'):
        return self.costs.append(Expression(equation, unit=unit))

    def state(self, var, rate=None, unit='nd', lower_bound=None, upper_bound=None, bits=None):
        return self.states.append(State(var=var, rate=rate, unit=unit, lower_bound=lower_bound, upper_bound=upper_bound, bits=bits))
