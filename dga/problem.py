from .Expression import Expression
from .State import State
import re


class Problem(object):
    ''' Defines the problem settings. '''
    def __init__(self, name, type='direct'):
        # TODO: I think this should use __new__ and not __init__
        # Names the current optimization problem.
        self.name = self._format_name(name)

        # Defines the type of optimization problem. Direct or indirect. Not sure if we need this.
        self.type = type

        # Additional information for the optimization problem
        self.parameters = []
        self.cost = []
        self.state = []
        self.quantity = []
        self.scale = []
        self.constraint = []
        self.baked = False

    def _format_name(self, name):
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

    def Cost(self, equation='', unit='nd'):
        return self.cost.append(Expression(equation, unit=unit))

    def State(self, var, rate=None, unit='nd', lower_bound=None, upper_bound=None, bits=None):
        return self.state.append(State(var=var, rate=rate, unit=unit, lower_bound=lower_bound, upper_bound=upper_bound, bits=bits))

    def Bake(self):
        self.params = []
        for state in self.state:
            self.params.append(state.sym)

        for expression in self.cost:
            if expression.baked is False:
                expression.lambdify(self.params)

        self.baked = True

    def __repr__(self):
        return self.name