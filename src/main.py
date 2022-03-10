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
import time
import utils

import nearest_neighbour
import pjs
import opt


if __name__ == '__main__':

    problem = utils.read_multi_source('g12_4_k.txt')

    problem.Tmax *= 4
    for source in problem.sources:
        for vehicle in source.vehicles:
            vehicle.capacity *= 4

    _start = time.time()

    routes, cost = nearest_neighbour.heuristic(problem)
    #routes, cost = nearest_neighbour.multistart(problem, maxiter=2000, n=3)

    print("Execution time: ", time.time() - _start)
    print("Total distance: ", cost)

    _start = time.time()

    mapping = pjs.mapper(problem)
    routes, cost = pjs.heuristic(problem, mapping)

    print("Execution time: ", time.time() - _start)
    print("Total distance: ", cost)

    utils.plot(problem, routes=routes)

    #routes, cost = opt.allOPT2(routes, problem.dists)

    #utils.plot(problem, routes=optimized_routes)



    print("Program concluded \u2764\uFE0F")
