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
import numpy as np
import collections
import random
import itertools

import grasp
from route import Route


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

    # Init the assignment of customers to vehicles (i.e., mapping)
    mapping = np.zeros((n_vehicles, n_sources + n_nodes))
    # Until nodes are not concluded a vehicle at each turn pick a node.
    for vehicle in itertools.islice(itertools.cycle(vehicles), n_nodes):
        # Pick a node
        picked_node = next(vehicle.preferences, None)
        # If the generator is exhausted exit the loop
        # NOTE: We should never reach this point
        if picked_node is None:
            break
        # Assign the node to the vehicle
        vehicle.nodes.append(picked_node)
        picked_node.assigned = True
        mapping[vehicle.id, picked_node.id] = 1
    # return the mapping
    return mapping



def heuristic (problem, mapping, *, bra=False, beta=0.3):
    """
    Implementation of a savings based heuristic inspired by the Clarke & Wright savings.

    :param problem: The instance of the problem to solve.
    :param mapping: The mapping obtained.
    :param bra: True if the biased randomisation is used, False otherwise.
    :param beta: The parameter of the quasi geometric distribution used in the biased randomisation.
    :return: The routes and the overall distance made by vehicles.
    """
    depot, edges, dists = problem.depot, problem.edges, problem.dists
    sources, Tmax = problem.sources, problem.Tmax

    # Init the total set of routes an the total cost
    all_routes, total_distance = [], 0

    # For each source a kind of PJS algorithm is done
    for source in sources:

        # Initialise the set of routes starting from the considered source
        # and the inteested customers assigned during the mapping process
        routes, nodes = [], []

        n_vehicles = len(source.vehicles)

        # Initialise the dummy solution
        for vehicle in source.vehicles:
            vehicle.copies = 0
            for node in vehicle.nodes:
                route = Route(source, depot, vehicle)
                route.nodes.append(node)
                node.route = route
                node.link_left = True
                node.link_right = True
                node.from_source = dists[source.id, node.id]
                node.to_depot = dists[node.id, depot.id]
                route.qty = node.qty
                route.cost = node.from_source + node.to_depot
                vehicle.copies += 1
                nodes.append(node)
                routes.append(route)

        nodes = set(nodes)
        # Sort edges that characterise
        sorted_edges = sorted(
            [edge for edge in problem.edges if edge.inode in nodes and edge.jnode in nodes],
            key=lambda i: i.savings[source.id],
            reverse=True
        )

        # Init edges iterator
        edges_iterator = iter(sorted_edges) if not bra else grasp.BRA(sorted_edges, beta=beta)

        # Merging process
        for edge in edges_iterator:
            # Extract interested nodes and routes
            inode, jnode = edge.inode, edge.jnode
            iroute, jroute = inode.route, jnode.route

            # The edge must merge two different routes
            if iroute == jroute:
                continue

            # The second vehicle should not be deleted
            if jroute.vehicle.copies == 1:
                continue

            # First node must be linked to depot and second node to source
            if not inode.link_right or not jnode.link_left:
                continue

            # Check capacity of vehicles
            if iroute.qty + jroute.qty > iroute.vehicle.capacity:
                continue

            # Check length of route
            if iroute.cost + jroute.cost + edge.cost - inode.to_depot - jnode.from_source > Tmax:
                continue

            # Merge the routes
            iroute.qty += jroute.qty
            iroute.cost += edge.cost + jroute.cost - inode.to_depot - jnode.from_source
            iroute.nodes.extend(jroute.nodes)
            jnode.link_left = False
            inode.link_right = False
            jroute.vehicle.copies -= 1
            routes.remove(jroute)
            for node in jroute.nodes:
                node.route = iroute

            # if the number of routes is equal to the number of vehicles exits the merging process
            if len(routes) == n_vehicles:
                all_routes.extend(routes)
                total_distance += sum(r.cost for r in routes)
                break

    # return routes and their cost
    return tuple(all_routes), total_distance



def multistart (problem, *, maxiter=1000, bra=(True, True), betarange = ((0.1, 0.3), (0.1, 0.3))):
    """
    This is a multistart implementatio on the savings based heuristic 
    that makes use of biased randomisation.
    It is possible to implement the BRA both in the mapping as in the 
    savings-based heuristic.

    :param problem: The problem to solve.
    :param maxiter: The numebr of solutions explored.
    :param bra: True if the biased randomisation is used, False otherwise.
    :param betarange: The betaranges for the biased randomisation.

    :return: The mapping, the routes found, and the respective cost.
    """
    # Move useful variables to the stack
    mapping_bra, pjs_bra = bra 
    mapping_range, pjs_range = betarange

    # Initial greedy solution
    bestmapping = mapper(problem)
    bestroutes, bestcost = heuristic(problem, bestmapping)

    for _ in range(maxiter):

        # Randomly generate betas
        betamapper = random.uniform(mapping_range[0], mapping_range[1])
        betasavings = random.uniform(pjs_range[0], pjs_range[1])

        # Generate new solution
        mapping = mapper(problem, bra=mapping_bra, beta=betamapper)
        routes, cost = heuristic(problem, mapping, bra=pjs_bra, beta=betasavings)

        # Eventually update best solution
        if cost < bestcost:
            bestmapping, bestroutes, bestcost = mapping, bestroutes, bestcost
    
    return bestmapping, bestroutes, bestcost


