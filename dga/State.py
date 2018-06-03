class State(object):
    """Defines state information."""

    def __new__(cls, *args, **kwargs):
        """
            Input:
        """
        obj = super(State, cls).__new__(cls)

        obj.lower_bound = kwargs.get('lower_bound', 0)
        obj.upper_bound = kwargs.get('upper_bound', 1)
        obj.bits = kwargs.get('bits', 8)
        obj.polyploid = kwargs.get('polyploid', False)
        obj.polymin = kwargs.get('polymin',1)
        obj.polymax = kwargs.get('polymax',1)

        return obj
