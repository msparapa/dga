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
        self.func = expr

    def __repr__(self):
        return self.expr
