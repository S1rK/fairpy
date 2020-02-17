from agents import *
from allocations import *
from typing import *
from numpy import argmax
from cut_and_choose import asymmetric_protocol
from normal_agent import *

t = PiecewiseConstantAgent([1, 1, 1, 1], "t")

a = PiecewiseConstantAgent([4, 3, 2, 1], "a")
b = PiecewiseConstantAgent([3, 4, 2, 1], "b")
c = PiecewiseConstantAgent([2, 3, 4, 1], "c")
d = PiecewiseConstantAgent([1, 2, 3, 4], "d")

alloc = Allocation([a, b, c, d])


def slice_to_4_continuous(start: float, end: float, slicer: Agent) -> List[Tuple[float, float]]:
    """
    Slice partitions to 4 equals partitions in the eyes of the slicer
    :param start: the start of the piece we want to cut.
    :param end: the end of the piece we want to cut.
    :param slicer: the agent who slice to 4 equal partitions.
    :return: a list of 4 equals slices in the eye of the cutter

    >>> a = PiecewiseConstantAgent([1, 1, 1, 1])
    >>> s = slice_to_4_continuous(0, 4, a)
    >>> s
    [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]
    >>> len(s)
    4
    >>> slice_to_4_continuous(0, 2, a)
    [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
    """
    # make sure they are floats
    start = float(start)
    end = float(end)

    # set start and end such as: 0.0 <= start, end <= 1.0
    start = max(0.0, min(start, end))
    end = max(0.0, min(end, 1.0))

    # the value of a piece
    quarter_val = slicer.eval(start, end) / 4

    # ask the slicer to mark four equal pieces
    second = slicer.mark(start, quarter_val)
    third = slicer.mark(second, quarter_val)
    fourth = slicer.mark(third, quarter_val)

    # return the 4 equal pieces
    return [(start, second), (second, third), (third, fourth), (fourth, end)]


def slice_to_4(partitions: List[Tuple[float, float]], slicer: Agent) -> List[List[Tuple[float, float]]]:
    """
    Slice partitions to 4 equals partitions in the eyes of the slicer
    :param partitions: a list of k slices [(start1, end1), (start2, end2), ...]
    :param slicer: the agent who slice to 4 equal partitions.
    :return: a list of 4 equals partitions
    [[(start1_1, end1_1), (start1_2, end1_2), ...], [(start2_1, end2_1), ..], [(start3_1, end3_1), ...],
                                                                                            [(start4_1, 4_end1), ...]]

    >>> a = PiecewiseConstantAgent([1, 1, 1, 1])
    >>> s = slice_to_4([(0, 4)], a)
    >>> s
    [[(0.0, 1.0)], [(1.0, 2.0)], [(2.0, 3.0)], [(3.0, 4.0)]]
    >>> len(s)
    4
    >>> slice_to_4([(0, 2)], a)
    [[(0.0, 0.5)], [(0.5, 1.0)], [(1.0, 1.5)], [(1.5, 2.0)]]
    """
    # make sure everything is float
    partitions = [(float(s), float(e)) for s, e in partitions]

    # get the value of each final partition
    quarter_val = sum(slicer.eval(*partition) for partition in partitions) / 4

    # the final partitions we will return
    final_slicing = []
    # the index of the partition we finished with at the last partition
    start_index = 0
    # the starting place of the star_index partition
    start_place = 0.0
    # for every final partition
    for time in range(4):
        # the current slices
        curr_slice = []
        # the value of the current partition
        curr_val = 0

        # for every partition in the given partitions list,
        # starting from the last partition that the prev final partition left us
        for i in range(start_index, len(partitions)):
            # the current partition we're looking at
            partition = partitions[i]
            # if we are at the first partition we're looking at
            if i == start_index:
                # fix the starting place
                partition = (start_place, partition[1])

            # get the current partition value
            curr_part_value = slicer.eval(*partition)

            # if with it the current main partition's value is the quarter value
            if curr_val + curr_part_value == quarter_val:
                # add this partition to the main one
                curr_slice.append(partition)

                # if it wasn't the last partition in the partitions list
                if i+1 < len(partitions):
                    # set the next starting index to be the next partition
                    start_index = i+1
                    # set the starting place to be
                    start_place = partitions[i+1][0]
                # end the current main partition search, because his value is the wanted one
                break

            # if with it the current main partition's value is greater than the quarter value
            elif curr_val + curr_part_value > quarter_val:
                # set the next starting index to be this partition
                start_index = i
                # find the place that gives the current main partition the exact value we want
                start_place = slicer.mark(partition[0], quarter_val-curr_val)
                # add this partition (ends at where we want him) to the main one
                curr_slice.append((partition[0], start_place))

                # end the current main partition search, because his value is the wanted one
                break

            else:
                # add this partition to the main one
                curr_slice.append(partition)
                # add this partition's value to the main's value
                curr_val += curr_part_value

        # add the main partition to the list of main partitions
        final_slicing.append(curr_slice)

    # return the 4 main partitions
    return final_slicing


print(slice_to_4([(0, 4)], t))
print(slice_to_4([(0, 2)], t))


def favorite_piece(pieces: List[Tuple[float, float]], agent: Agent) -> Tuple[float, float]:
    """
    :param pieces: a list of tuples of floats that represents a start and end of each piece.
    :param agent: the agent that chooses his favorite piece.
    :return: the agent's favorite piece (tuple of two floats - the start and end of the favorite piece).

    >>> a = PiecewiseConstantAgent([1, 1, 1, 1])
    >>> favorite_piece([(0, 1), (1, 2), (2, 3), (3, 4)], a)
    (0, 1)
    >>> favorite_piece([(0, 1), (2, 3.5), (3.5, 3.75), (3.75, 4)], a)
    (2, 3.5)
    >>> b = PiecewiseConstantAgent([4, 1, 1, 1])
    >>> favorite_piece([(0, 1), (1, 4)], b)
    (0, 1)
    """
    return pieces[int(argmax([agent.eval(*piece) for piece in pieces]))]


def core(all_agents: List[Agent], cutter: Agent, residue: List[Tuple[float, float]],
         excluded: List[Agent]) -> Tuple[Allocation, Tuple[float, float]]:
    allocation = Allocation(all_agents)
    # agent k (the cutter) cuts the current residue R (the residue) in for equal valued pieces (according to her)
    new_allocation = slice_to_4(residue, cutter)
    slices = [(new_allocation[i], new_allocation[i + 1]) for i in range(len(new_allocation) - 1)]

    # let S (competitors) = N/({k}∪E) be the set of agents who may compete for pieces
    competitors = [agent for agent in all_agents if agent is not cutter and agent not in excluded]

    # the competitors' favorite pieces
    favorite_pieces = [favorite_piece(slices, agent) for agent in competitors]

    # if there exists j∈S (agent in competitors) who has no competition in S (competitors) for her favorite piece then
    # for every in agent in competitors (j∈S)
    for i in range(0, len(competitors), -1):
        # get the current agent and his favorite piece
        current_agent = competitors[i]
        fav_piece = favorite_pieces[i]
        # if he has no competition over this piece
        if favorite_pieces.count(fav_piece) == 1:
            # the agent (j) is allocated her favorite piece and is removed rom competitors (S).
            competitors.remove(current_agent)
            allocation.set_piece(0, [fav_piece])

    # if every agent in competitors (S) has a different favorite piece then
    if len(competitors) == 0:
        # everyone gets their favorite piece and the algorithm terminates
        return allocation

    # for very agent i∈S do:
    for agent in competitors:
        # if 1) i (agent) has no competition for her second favorite piece p
        #    or
        #    2) i (agent) has exactly one competitor j∈S for p,
        #       j also considers p as her second favorite,
        #       and i,j each have exactly one competitor for their favorite piece
        if 1 in all_agents:
            # i (agent) makes a 2-mark
            pass
        else:
            # i (agent) makes a 3-mark
            pass

    # TODO: complete this shit
    # Allocate the pieces according to a rightmost rule:
    # if an agent has the rightmost mark in two pieces then
    # Out of the two partial pieces, considered until the second rightmost mark (which always exists by
    # Lemma 4 below), she is allocated the one she prefers.
    # The other partial piece is given to the agent who made the second rightmost mark on it.
    # else
    # Each partial piece is allocated—until the second rightmost mark—to the agent who made the
    # rightmost mark on that piece.
    # if any non-cutters were not given a piece yet then
    # Giving priority to any remaining agents in S (but in an otherwise arbitrary order), they choose their
    # favorite unallocated complete piece.
    # The cutter is given the remaining unallocated complete piece.


def correction(agent: Agent):
    raise NotImplementedError("shit")


def main_protocol(agents: List[Agent]):
    # normalize the agents
    agents = [NormalAgent(agent) for agent in agents]

    # the whole cake
    cake = [(0, 1)]

    # --- Phase One
    allocations = []

    residue = cake

    # for count = 1 to 4 do
    for _ in range(4):
        # run CORE on the current residue with agent 1 as the cutter
        allocation, residue = core(agents, agents[0], residue, [])
        allocations.append(allocation)

    # TODO: if the same agent got the insignificant piece in all 4 executions of CORE
    if True:
        # TODO: find A*∈{A1,A2,A3,A4} such that G_A*(i)<= sum([G_A(i) for A != A*]) for all i∈N\{1}

        # TODO: run correction on A*

        pass

    # run CORE on the residue with agent 1 as the cutter
    core(agents, agents[0], cake, [])

    # TODO: if there is some agent E∈N\{1} not dominated by agent 1 then
    if 1 in agents:
        # TODO: run CORE on the residue with agent E as the cutter, excluding agent 1 from competition.
        E = agents[2]
        Es_piece = cake.pieces[agents.index(E)]
        core(agents, E, Es_piece, [agents[0]])
    else:
        # TODO: run the Selfridge-Conway Protocol on the residue for agents 2,3 and 4 and terminate.
        pass

    # now, if the algorithm has not terminated,
    # TODO: some agent A is dominated by two other agents B and C.
    A = agents[0]
    B = agents[1]
    C = agents[3]
    # TODO: Let D be the remaining agent
    D = agents[2]
    Ds_piece = cake.pieces(agents.index(D))
    # TODO: any one from {B,C} who dominates two non-cutters.
    dominates_two_non_cutters = [agent for agent in [B, C] if True]

    # --- Phase Two
    # for count = 1 to 2 do
    # TODO: run CORE on the current residue with agent D as the cutter,
    # TODO: excluding from competition any one from {B,C} who dominates two non-cutters.
    new_allocations = [core(agents, D, Ds_piece, dominates_two_non_cutters) for _ in range(2)]

    # TODO: if B and C are not both dominated by A and D then:
    if True:
        # TODO: let F∈{B,C} be the agent who got insignificant piece in the last two calls of CORE
        F = [B, C][0]
        # TODO: run CORRECTION on the sub-allocation (out of the last two) where G_A(F) was smaller.
        smaller_allocation = min([alloc.pieces(agents.index(F)) for alloc in new_allocations])
        correction(F, smaller_allocation)

    # at this point both A and D dominate both B and C.

    # --- Phase Three
    # TODO: run CUT AND CHOOSE on the current residue for agents B and C
    asymmetric_protocol([B, C])

    raise NotImplementedError("shit")
