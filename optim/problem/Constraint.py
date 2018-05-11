from sympy import sympify
from .Expression import Expression

# TODO: Make this work. My idea was that constraints could be their own class and could
# be adjoined to the cost in one of several ways, but I'm currently just adjoining them
# manually with penalty multipliers.

class Constraint(Expression):
    """Defines constraint information. If """
    # NEED TO ADD PATH CONSTRAINT

    def __init__(self, expr='', unit='nd', direction=0, value=0):
        """
        Input: expr (string)
               unit (string)
               direction (integer) : 0 for equality, 1 for expr > value, -1 for expr < value
               value (float) : Number to compare to expr
        """
        self.expr_original = expr
        self.direction = direction
        self.value = value
        if callable(expr):
            if direction == 0:
                augmented_expression = expr - value
            elif direction == 1:
                augmented_expression = expr - value
            elif type == 'inequality' and direction == -1:
                augmented_expression = value - expr
        elif isinstance(expr, str):
            if direction == 0:
                augmented_expression = '(' + str(expr) + ')' + '-' + str(value)
            elif direction == 1:
                augmented_expression = str(value) + '-' + '(' + str(expr) + ')'
            elif direction == -1:
                augmented_expression = '(' + str(expr) + ')' + '-' + str(value)

        super().__init__(expr=augmented_expression,unit=unit)


    def residual(self, *args):
        if self.direction == 0:
            return self.func(*args)
        else:
            temp_eval = self.func(*args)
            return (temp_eval > 0) * temp_eval


    def __repr__(self):
        if self.direction == 0:
            return self.expr_original + ' = ' + str(self.value)
        elif self.direction == 1:
            return self.expr_original + ' > ' + str(self.value)
        elif self.direction == -1:
            return self.expr_original + ' < ' + str(self.value)