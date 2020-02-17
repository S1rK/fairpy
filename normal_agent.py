from agents import Agent


class NormalAgent(Agent):
    """
    A decorator class for agent to normalize the length and the total of the cake to 1.0, because it's a convention
    used by some algorithms which makes the algorithm simpler, and it's not hard to adjust each agent to follow these
    rules and keeps the distribution of the agent values of the cake.
    """

    def __init__(self, agent: Agent):
        """

        :param agent: An agent to normalize it's values
        """
        assert agent is not None
        super().__init__(self.agent.name())
        self.agent = agent

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
        """
        assert 0.0 <= start <= end <= 1.0
        # Adjust the start and the end values to be relative to cake's length of the agent
        adjusted_start = start * self.agent.cake_length()
        adjusted_end = end * self.agent.cake_length()
        # Gets the value of the piece and normalize it
        return self.agent.eval(adjusted_start, adjusted_end) / self.cake_value()

    def mark(self, start: float, targetValue: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is targetValue.
        Note: that the parameters and return value are normalized.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of targetValue, adjusted to the be a normalized value.
        """
        assert 0.0 <= start <= 1.0 and 0 <= targetValue <= 1
        # Adjust the start and the targetValue values to be relative to cake's length and value of the agent
        adjusted_start = start * self.agent.cake_length()
        adjusted_target_value = targetValue * self.agent.cake_value()
        # Gets the 'end' of the piece and normalize it
        return self.mark(adjusted_start, adjusted_target_value) / self.agent.cake_length()
