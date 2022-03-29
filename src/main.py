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
import os
import time
import utils

import nearest_neighbour
import pjs
import opt



OUTPUTFILE = "Results.csv"


# clean output file 
open(OUTPUTFILE, "w") 


def save (string):
    with open(OUTPUTFILE, "a") as file:
        file.write(string)



if __name__ == '__main__':


    filenames = sorted(os.listdir("../tests/multi/"), key=lambda i: len(i))


    for filename in filenames:
        print(filename)
        save(f"{filename}, ")

        problem = utils.read_multi_source(filename)



        # NEAREST NEIGHBOUR HEURISTIC
        _start = time.time()
        nn_routes, nn_cost = nearest_neighbour.heuristic(problem)
        nn_duration =  time.time() - _start
        save(f"{int(nn_cost)},{round(nn_duration, 3)},")
        #utils.plot(problem, routes=nn_routes)


        # NEAREST NEIGHBOUR MULTISTART
        _start = time.time()
        nnm_routes, nnm_cost = nearest_neighbour.multistart(problem, maxiter=1000, betarange=(0.1, 0.3))
        nnm_duration =  time.time() - _start
        save(f"{int(nnm_cost)},{round(nnm_duration, 3)},")
        #utils.plot(problem, routes=nnm_routes)


        # NEAREST NEIGHBOUR MULTISTART + 2-OPT
        _start = time.time()
        nnm_opt_routes, nnm_opt_cost = opt.allOPT2(nnm_routes, problem.dists)
        nnm_opt_duration = time.time() - _start + nnm_duration
        save(f"{int(nnm_opt_cost)},{round(nnm_opt_duration, 3)},") 
        #utils.plot(problem, routes=nnm_opt_routes)



        # SAVINGS BASED HEURISTIC 
        _start = time.time()
        mapping = pjs.mapper(problem)
        sv_routes, sv_cost = pjs.heuristic(problem, mapping)
        sv_duration = time.time() - _start
        save(f"{int(sv_cost)},{round(sv_duration, 3)},")
        utils.plot(problem, routes=sv_routes, mapping=mapping)

        

        # SAVINGS BASED MULTISTART 
        _start = time.time()
        mapping, svm_routes, svm_cost = pjs.multistart(problem, maxiter=1000, bra=(True, True), betarange = ((0.7, 0.9), (0.7, 0.9)))
        svm_duration = time.time() - _start
        save(f"{int(svm_cost)},{round(svm_duration, 3)},")
        utils.plot(problem, routes=svm_routes, mapping=mapping)




        # SAVINGS BASED MULTISTART + 2-OPT
        _start = time.time()
        svm_opt_routes, svm_opt_cost = opt.allOPT2(svm_routes, problem.dists)
        svm_opt_duration = time.time() - _start + svm_duration
        save(f"{int(svm_opt_cost)},{round(svm_opt_duration, 3)},")
        #utils.plot(problem, routes=svm_opt_routes, mapping=mapping)
        
        

        save("\n")



    print("Program concluded \u2764\uFE0F")
