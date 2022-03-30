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
import collections
import time 


def _get_cost (route, solution, dists):
    """
    This method is used to calculate the total distance
    associated to a route, once the sequence of its nodes
    has been changed using the 2-OPT algorithm.

    :param route: The interested route.
    :param solution: The nodesin the order in which they are visited.
    :param dists: The matrix of distances between nodes.
    :return: The total distance.
    """
    cnode, cost = route.source.id, 0
    for node in solution:
        cost += dists[cnode, node.id]
        cnode = node.id
    cost += dists[cnode, route.depot.id]
    return cost


def _fast_get_cost (swap, route, solution, current_cost, dists):
    """
    Fastest way to get the cost of a solution after a 2-opt swap.
    NOTE: This works only if the matrix of distances is symmetric.

    :param swap: The ids of positions swapped.
    :param route: The route to optimize.
    :param solution: The nodes in the order in which they are visited.
    :param current_cost: The cost of the current solution.
    :param dists: The matrix of distances.
    :return: The cost after swapping the positions indicated in swap.
    """
    sol = [route.source] + solution + [route.depot]
    i, j = swap
    A, B, C, D = sol[i].id, sol[i + 1].id, sol[j].id, sol[j + 1].id
    return current_cost - dists[A, B] - dists[C, D] + dists[A, C] + dists[B, D]


def OPT2 (route, dists, maxtime=float("inf")):
    """
    This method is an implementation of the 2-OPT algorithm.

    :param route: The route made by a single vehicle on which the optimisation is made.
    :param dists: The matrix of distances between nodes.
    :param maxtime: The maximum time the optimization can go on.
    :return: The route optimised, and the new overall distance.
    """
    # time control 
    _start = time.time()
    _ctime = time.time()

    # useful variables
    solution, cost = list(route.nodes), route.cost
    L = len(solution)
    i = 0
    while i < L - 1:
        j = i + 2
        while j < L + 1:
            #_new_solution = solution[:i] + list(reversed(solution[i:j])) + solution[j:]
            #_new_cost =_get_cost(route, _new_solution, dists)
            # No need to generate in this moment the new solution
            new_cost = _fast_get_cost((i,j), route, solution, cost, dists)

            if new_cost < cost:
                solution = solution[:i] + list(reversed(solution[i:j])) + solution[j:]
                cost = new_cost
                i, j = 0, 1
            
            # If maxtime is exceeded set the condition to exit the optimization
            _ctime = time.time()
            if _ctime - _start > maxtime:
                i, j = L, L 
            
            j += 1
        i += 1

    route.nodes = collections.deque(solution)
    route.cost = cost
    return route, cost


def allOPT2 (routes, dists, maxtime=float("inf")):
    """
    A simpler way to make the 2-OPT optimization on all
    the provided routes.

    :param routes: The routes to optimize.
    :param dists: The matrix of distances. 
    :param maxtime: The maximum time the optimization can go on.
    :return: The optimised routes and the overall respective cost.
    """
    optimized_routes = [None] * len(routes)
    total_cost = 0
    for i, route in enumerate(routes):
        oproute, cost = OPT2(route, dists, maxtime)
        optimized_routes[i] = oproute
        total_cost += cost
    return optimized_routes, total_cost
