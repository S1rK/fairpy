from agents import Agent
from allocations import Allocation
from typing import List
from cut_and_choose import asymmetric_protocol


def main_protocol(agents: List[Agent]):
	# the whole cake
	cake = Allocation(agents)

	# --- Phase One
	# for count = 1 to 4 do
	# run CORE on the current residue with agent 1 as the cutter
	allocations = [core(agents, agents[0], cake, []) for _ in range(4)]

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


def core(all_agents: List[Agent], cutter: Agent, residue: Allocation, excluded: List[Agent]) -> Allocation:
	# TODO: agent k (the cutter) cuts the current residue R (the residue) in for equal valued pieces (according to her)
	new_allocation = residue
	# let S (competitors) = N/({k}∪E) be the set of agents who may compete for pieces
	competitors = [agent for agent in all_agents if agent is not cutter and agent not in excluded]

	# TODO: if there exists j∈S who has no competition in S for her favorite piece then
	if True:
		# TODO: j is allocated her favorite piece and is removed rom S.
		agent = competitors[0]
		piece = [(0, 0.3)]
		new_allocation.set_piece(0, piece)
		competitors.remove(agent)

	# TODO: if every agent in S has a different favorite piece then
	# TODO: everyone gets their favorite piece and the algorithm terminates

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

	# TODO: allocate the prices according to a rightmost rule:
	# if an agent ahs the rightmost mark in two pieces then
		# out of the two partial pieces, considered until the second rightmost mark, she is allocated the one she pereferces

	raise NotImplementedError("shit")


def correction(agent:Agent):
	raise NotImplementedError("shit")