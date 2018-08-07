class Model(object):
    """
    The model calculates a result given a dividend and a divisor and returns the result.
    """

    def step(self, dividend, divisor):
        """
        Parameters:
            dividend - current period's dividend decision
            divisor - current period's divisor decision
        Returns result of dividing dividend by divisor.
        """
        return dividend / divisor
