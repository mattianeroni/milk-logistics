"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
This file is part of the collaboration between University of Modena and
University of Campania "Luigi Vanvitelli". It is authored by Mattia Neroni and Marta Rinaldi.

The scope is the implementation and validation of several algorithms to optimise the
collection of milk and its delivery to the production plant or cheese factory.

The problem is new in literature, and can be partially associated to the multi-source
vehicle routing problem, with the only difference that the starting and ending depots
are different like in the multi-source team orienteering problem.
For a better description of the problem, please refer to scientific pubblication.


Author: Mattia Neroni, Ph.D., Eng.
Contact: mneroni@unimore.it
Date: January 2022
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import operator
import grasp



def _reset_assignment (node):
    """
    This method reset the assignment of a node to a certain vehicle.
    """
    node.assigned = False
    return node


def _selector (iterable):
    """
    This is just a wrapper around an iterator that filter nodes
    to return only the not assigned ones.
    :param iterable: An iterable set of nodes (i.e., (rate, node)).
    """
    for _, node in iterable:
        if not node.assigned:
            yield node


def mapper (problem, *, bra=False, beta=0.3):
    """
    This method has the objective to assign each customer to a source / vehicle.

    :param problem: The instance of the problem to solve.
    :param bra: True if the biased randomisation is used, False otherwise.
    :param beta: The parameter of the quasi geometric distribution used in the biased randomisation.
    :return: A mapping that assign each each customer to a certain vehicle.
    """
    dists = problem.dists
    sources, nodes, depot = problem.sources, problem.nodes, problem.depot
    vehicles = tuple(v for s in sources for v in s.vehicles)
    n_sources, n_nodes, n_vehicles = len(problem.sources), len(problem.nodes), len(vehicles)

    # Reset the source the nodes belongs to
    nodes = tuple(map(_reset_assignment, nodes))

    # Compute the absolute distances
    abs_dists = np.array(
        [[dists[s.id, n.id] + dists[n.id, depot.id]
          for n in nodes]
         for s in sources for v in s.vehicles]
    ).astype("float32")

    # Compute the marginal distances
    for i, vehicle in enumerate(vehicles):
        marginal_dists = abs_dists[i, :] - np.concatenate((abs_dists[:i, :], abs_dists[i + 1:, :],), axis=0).min(axis=0)
        vehicle.nodes = collections.deque()
        if not bra:
            vehicle.preferences = _selector(iter(sorted(zip(marginal_dists, nodes), key=operator.itemgetter(0))))
        else:
            vehicle.preferences = _selector(grasp.BRA(sorted(zip(marginal_dists, nodes), key=operator.itemgetter(0)), beta=beta))

    """
    # Assign nodes to sources
    # Init the number of nodes already assigned and the mapping matrix
    n_assigned = 0
    mapping = np.zeros((n_sources, n_sources + n_nodes))
    _null_element = object()
    # NOTE: Until nodes are not concluded a source at each turn pick a number of preferred
    # nodes that depend on the number of vehicles it has.
    for source in itertools.islice(itertools.cycle(sources), n_nodes):
        # Consider the preferences of the currently considered source
        preferences = source.preferences
        # Pick a number of preferences that depend on the number of vehicles
        # that start from the source.
        for _ in range(source.vehicles):
            # Pick a node
            picked_node = next(preferences, _null_element)
            # If the generator is exhausted exit the loop
            if picked_node is _null_element:
                break
            # Assign the node to the source
            source.nodes.append(picked_node)
            picked_node.assigned = True
            mapping[source.id, picked_node.id] = 1
            n_assigned += 1

        # If all the nodes have already been assigned we exit the loop
        if n_assigned == n_nodes:
            break
    """



def heuristic (problem, *, bra=False, beta=0.3):
    """
    Implementation of a savings based heuristic inspired by the Clarke & Wright savings.

    :param problem: The instance of the problem to solve.
    :param bra: True if the biased randomisation is used, False otherwise.
    :param beta: The parameter of the quasi geometric distribution used in the biased randomisation.
    """


    #sorted_edges = sorted(problem.edges, key=lambda i: i.savings[], reverse=True)