from agents import Agent, PiecewiseConstantAgent


class NormalAgent(Agent):
    """
    A decorator class for agent to normalize the length and the total of the cake to 1.0, because it's a convention
    used by some algorithms which makes the algorithm simpler, and it's not hard to adjust each agent to follow these
    rules and keeps the distribution of the agent values of the cake.

    >>> a = NormalAgent(PiecewiseConstantAgent([11, 22, 33, 44]))
    >>> # Eval tests
    >>> a.eval(0.25, 0.75)
    0.5

    >>> # Mark test
    >>> a.mark(0.25, 0.5)
    0.75
    """

    def __init__(self, agent: Agent):
        """

        :param agent: An agent to normalize it's values
        """
        assert agent is not None
        super().__init__(agent.name())
        self.__agent = agent

    def cake_value(self):
        """
        The values are normalized, therefore the value of the whole cake is 1.0
        :return: 1.0
        """
        return 1.0

    def cake_length(self):
        """
        The values are normalized, therefore the length of the whole cake is 1.0
        :return: 1.0
        """
        return 1.0

    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end].
        Note: that the parameters and return value are normalized.

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end], adjusted to the be a normalized value.

        >>> a = NormalAgent(PiecewiseConstantAgent([11, 22, 33, 44]))
        >>> a.eval(0.375, 0.75)
        0.4
        >>> a.eval(0.25, 0.8125)
        0.6
        >>> a.eval(0.375, 0.8125)
        0.5
        >>> a.eval(1.0, 1.0)
        0.0
        >>> a.eval(0.75, 1.75)
        0.4
        >>> a.eval(-0.25, 1.75)
        1.0
        """
        # Make sure start and end are in [0, 1]
        start = min(1.0, max(0.0, start))
        end = min(1.0, max(0.0, end))

        # Adjust the start and the end values to be relative to cake's length of the agent
        adjusted_start = start * self.__agent.cake_length()
        adjusted_end = end * self.__agent.cake_length()

        # Gets the value of the piece and normalize it
        return self.__agent.eval(adjusted_start, adjusted_end) / self.__agent.cake_value()

    def mark(self, start: float, targetValue: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is targetValue.
        Note: that the parameters and return value are normalized.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of targetValue, adjusted to the be a normalized value.

        >>> a = NormalAgent(PiecewiseConstantAgent([11, 22, 33, 44]))
        >>> a.mark(0.375, 0.4)
        0.75
        >>> a.mark(0.25, 0.6)
        0.8125
        >>> a.mark(0.375, 0.5)
        0.8125
        >>> a.mark(0.25, 0.9)
        1.0
        >>> a.mark(0.25, 0.91)
        >>> a.mark(0.25, 0)
        0.25
        """
        # Make sure start and targetValue are in [0, 1]
        start = min(1.0, max(0.0, start))
        targetValue = min(1.0, max(0.0, targetValue))

        # Adjust the start and the targetValue values to be relative to cake's length and value of the agent
        adjusted_start = start * self.__agent.cake_length()
        adjusted_target_value = targetValue * self.__agent.cake_value()

        # Gets the 'end' of the piece and normalize it
        end = self.__agent.mark(adjusted_start, adjusted_target_value)
        return None if end is None else end / self.__agent.cake_length()
