from sympy import sympify, lambdify, Symbol
from sympy.core.function import AppliedUndef
class Expression(object):
    """Defines expression information."""

    def __init__(self, expr='', unit='nd'):
        """
        Input: expr (string)
               unit (string)
        """
        self.expr = expr
        self.unit = unit
        self.baked = False
        # TODO: This sorta hardcodes in custom functions. There's a way to lambdify custom functions, but IDK how to do it at the moment. Doing this will allow us to mix and match custom funcs with string expressions.
        if callable(expr):
            self.func = expr
            self.baked = True
        else:
            self.sym = sympify(expr)
        # self.func = lambdify(self.sym.free_symbols, self.sym)
        # params = self._dummify_undefined_functions(self.sym)
        # params = [dummify_undefined_functions(x) for x in [t, s, s.diff(t)]]
        # expr = dummify_undefined_functions(b)
        # fb = sympy.lambdify(params, expr)

    def bake(self, params):
        if type(self.expr) is str:
            self.func = lambdify(params,self.expr)
        elif callable(self.expr):
            self.func = self.expr

    def lambdify(self, params):
        new_params = [self._dummify_undefined_functions(param) for param in params]
        unknown_funcs = [self._dummify_undefined_functions(expr) for expr in self.sym.atoms(AppliedUndef)]
        new_params.append(unknown_funcs)
        new_expr = self._dummify_undefined_functions(self.sym)
        self.func = lambdify(params, self.sym)
        self.baked = True

    def __repr__(self):
        return self.expr

    @staticmethod
    def _dummify_undefined_functions(expr):
        '''
        Some code used to properly lambdify expressions containing arbitrary functions.
        Retrieved from: http://stackoverflow.com/questions/29920641/lambdify-a-sympy-expression-that-contains-a-derivative-of-undefinedfunction
        '''
        mapping = {}

        # # replace all Derivative terms
        # for der in expr.atoms(sympy.Derivative):
        #     f_name = der.expr.func.__name__
        #     var_names = [var.name for var in der.variables]
        #     name = "d%s_d%s" % (f_name, 'd'.join(var_names))
        #     mapping[der] = sympy.Symbol(name)

        # replace undefined functions
        for f in expr.atoms(AppliedUndef):
            f_name = f.func.__name__
            mapping[f] = Symbol(f_name)

        return expr.subs(mapping)