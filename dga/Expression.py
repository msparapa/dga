class Expression(object):
    """Defines expression information."""

    def __new__(cls, expr='', unit='nd'):
        """
        Input: expr (string)
               unit (string)
        """
        obj = super(Expression, cls).__new__(cls)

        obj.expr = expr
        obj.unit = unit
        obj.baked = False
        obj.func = expr

        return obj

    def __repr__(self):
        return self.expr
