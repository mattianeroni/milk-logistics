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
import itertools
import random

from grasp import GRASP, BRA
from route import Route




def _check_inclusion (problem, node, vehicle, route, dists):
    """
    This method is used to check if a node can be included in the route
    assigned to certain vehicle.

    :param problem: The instance of the problem to solve.
    :param node: The node.
    :param vehicle: The vehicle.
    :param route: The route.
    :param dists: The matrix of distances.
    :return: True if the insertion is possible, False otherwise.
    """
    if node.qty + route.qty > vehicle.capacity:
        return False

    if route.cost + dists[vehicle.cnode, node.id] + dists[node.id, problem.depot.id] > problem.Tmax:
        return False

    return True




def _nearest_node (problem, vehicle, route, nodes, dists, *, bra=False, beta=0.3):
    """
    This method returns the nearest node for a given vehicle.

    :param problem: The instance of the problem to solve.
    :param vehicle: The considered vehicle.
    :param route: The route the vehicle is taking care of.
    :param nodes: The options.
    :param dists: The matrix of distances.
    :param bra: True if a biased randomisation is used.
    :param beta: The parameter of the quasi-geometric function in the biased randomisation.
    :return: The nearest node.
    """
    cnode = vehicle.cnode
    sorted_nodes = sorted(nodes, key=lambda i: dists[cnode, i.id])

    # Greedy selection
    if not bra:
        for node in sorted_nodes:
            if _check_inclusion(problem, node, vehicle, route, dists):
                return node, True

    # BRA selection
    for node in BRA(sorted_nodes, beta):
        if _check_inclusion(problem, node, vehicle, route, dists):
            return node, True

    return None, False




def heuristic (problem, *, bra=False, beta=0.3):
    """
    This method is the heuristic implementation of the nearest neighbour algorithm.

    :param problem: The instance of the problem to solve.
    :param bra: True if the biased randomisation is introduced, False otherwise.
    :param beta: The parameter of the biased randomisation.
    :return: The solution as a tuple of routes, and the total cost of the solution.
    """
    depot, dists, n_vehicles = problem.depot, problem.dists, problem.n_vehicles
    n_nodes = len(problem.nodes)
    Tmax = problem.Tmax

    # Initialise the total cost of the solution
    total_cost = 0

    # Initialise the empty routes
    routes = [Route(source,depot,vehicle) for source in problem.sources for vehicle in source.vehicles]

    # Initialise the nodes to visit
    nodes = list(problem.nodes)

    for i, route in enumerate(itertools.islice(itertools.cycle(routes), n_nodes)):
        vehicle = route.vehicle

        if i < n_vehicles:
            vehicle.cnode = route.source.id

        node, done = _nearest_node(problem, vehicle, route, nodes, dists, bra=bra, beta=beta)

        if done:
            route.nodes.append(node)
            route.qty += node.qty
            cost = dists[vehicle.cnode, node.id]
            route.cost += cost
            total_cost += cost

            vehicle.cnode = node.id
            node.assigned = True
            nodes.remove(node)

    # Update the cost of routes including the travel to the depot
    for route in routes:
        vehicle = route.vehicle
        cost = dists[vehicle.cnode, depot.id]
        route.cost += cost
        total_cost += cost

    # Return the solution and the relative cost
    return tuple(routes), total_cost




def multistart (problem, maxiter=1000, betarange=(0.1, 0.3)):
    """
    This method is a multistart implementation of the nearest neighbour algorithm.

    :param maxiter: The number of solutions explored.
    :param betarange: The range of the beta parameter for the biased randomisation.
    :return: The solution as a tuple of routes, and the total cost of the solution.
    """
    # Generate a starting greedy solution
    routes, cost = heuristic(problem)

    betamin, betamax = betarange

    for _ in range(maxiter):
        # randomly generate a beta in the specified range 
        beta = random.uniform(betamin, betamax)

        # Generate a new solution from scratch using the GRASP randomisation
        newroutes, newcost = heuristic(problem, bra=True, beta=beta)

        # If the new solution is better, the best solution is updated
        if newcost < cost:
            routes, cost = newroutes, newcost

    # Return the best solution found so far
    return routes, cost
