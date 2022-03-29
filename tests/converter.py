import os

import utils
import pjs 



if __name__ == '__main__':


    filenames = os.listdir("../tests/single/")

    for filename in filenames:

        # Read the problem 
        problem = utils.read_single_source(filename, path="../tests/single/")
        print(problem.name)

        # Transform the problem in a problem at infinite capacity
        problem.Tmax = float("inf")
        for source in problem.sources:
            for vehicle in source.vehicles:
                #print("before ", id(vehicle),  vehicle.capacity)
                vehicle.capacity = float("inf")

        # Solve the problem with a deterministic savings based heuristic
        mapping = pjs.mapper(problem)
        routes, cost = pjs.heuristic(problem, mapping)

        # Update problem characteristics
        Tmax, maxcap = 0, 0
        for route in routes:
            maxcap = max(maxcap, route.qty)
            #vehicle.capacity =  99999999999 #route.qty
            Tmax = max( Tmax, route.cost )
            #print("after ", id(vehicle),  vehicle.capacity)
        problem.Tmax = round(Tmax ,  2)
        for route in routes:
            route.vehicle.capacity = maxcap


        #utils.plot(problem, routes=routes, mapping=mapping)

        # Export the problem 
        utils.export(problem, "../tests/single/")
    



    benchmarks = (
        ("g12_4_k.txt","p1.4.k.txt","p2.4.k.txt",""),
        ("g26_2_k.txt","p2.2.k.txt","p6.2.k.txt",""),
        ("g57_2_n.txt","p5.2.n.txt","p7.2.n.txt",""),
        ("g45_2_n.txt","p4.2.n.txt","p5.2.n.txt",""),
        ("g57_4_c.txt","p5.4.c.txt","p7.4.c.txt",""),
        ("g45_4_n.txt","p4.4.n.txt","p5.4.n.txt",""),
        ("g14_4_n.txt","p1.4.n.txt","p4.4.n.txt",""),
        ("g35_2_c.txt","p3.2.c.txt","p5.2.c.txt",""),
        ("g35_4_c.txt","p3.4.c.txt","p5.4.c.txt",""),
        ("g14_4_c.txt","p1.4.c.txt","p4.4.c.txt",""),
        ("g12_2_k.txt","p1.2.k.txt","p2.2.k.txt",""),
        ("g45_2_c.txt","p4.2.c.txt","p5.2.c.txt",""),
        ("g47_2_n.txt","p4.2.n.txt","p7.2.n.txt",""),
        ("g12_2_c.txt","p1.2.c.txt","p2.2.c.txt",""),
        ("g26_2_c.txt","p2.2.c.txt","p6.2.c.txt",""),
        ("g35_4_n.txt","p3.4.n.txt","p5.4.n.txt",""),
        ("g14_2_n.txt","p1.2.n.txt","p4.2.n.txt",""),
        ("g57_2_c.txt","p5.2.c.txt","p7.2.c.txt",""),
        ("g47_4_c.txt","p4.4.c.txt","p7.4.c.txt",""),
        ("g14_2_c.txt","p1.2.c.txt","p4.2.c.txt",""),
        ("g35_2_n.txt","p3.2.n.txt","p5.2.n.txt",""),
        ("g47_2_c.txt","p4.2.c.txt","p7.2.c.txt",""),
        ("g47_4_n.txt","p4.4.n.txt","p7.4.n.txt",""),
        ("g12_4_c.txt","p1.4.c.txt","p2.4.c.txt",""),
        ("g57_4_n.txt","p5.4.n.txt","p7.4.n.txt",""),
        ("g26_4_c.txt","p2.4.c.txt","p6.4.c.txt",""),
        ("g26_4_k.txt","p2.4.k.txt","p6.4.k.txt",""),
        ("g45_4_c.txt","p4.4.c.txt","p5.4.c.txt",""),
        ("g123_4_k.txt","p1.4.k.txt","p2.4.k.txt","p3.4.k.txt"),
        ("g456_2_n.txt","p4.2.n.txt","p5.2.n.txt","p6.2.n.txt"),
        ("g356_4_c.txt","p3.4.c.txt","p5.4.c.txt","p6.4.c.txt"),
        ("g346_2_n.txt","p3.2.n.txt","p4.2.n.txt","p6.2.n.txt"),
        ("g127_4_c.txt","p1.4.c.txt","p2.4.c.txt","p7.4.c.txt"),
        ("g127_4_k.txt","p1.4.k.txt","p2.4.k.txt","p7.4.k.txt"),
        ("g356_4_n.txt","p3.4.n.txt","p5.4.n.txt","p6.4.n.txt"),
        ("g256_2_c.txt","p2.2.c.txt","p5.2.c.txt","p6.2.c.txt"),
        ("g123_2_c.txt","p1.2.c.txt","p2.2.c.txt","p3.2.c.txt"),
        ("g146_4_n.txt","p1.4.n.txt","p4.4.n.txt","p6.4.n.txt"),
        ("g346_4_c.txt","p3.4.c.txt","p4.4.c.txt","p6.4.c.txt"),
        ("g346_4_n.txt","p3.4.n.txt","p4.4.n.txt","p6.4.n.txt"),
        ("g127_2_c.txt","p1.2.c.txt","p2.2.c.txt","p7.2.c.txt"),
        ("g127_2_k.txt","p1.2.k.txt","p2.2.k.txt","p7.2.k.txt"),
        ("g456_4_n.txt","p4.4.n.txt","p5.4.n.txt","p6.4.n.txt"),
        ("g256_2_k.txt","p2.2.k.txt","p5.2.k.txt","p6.2.k.txt"),
        ("g456_4_c.txt","p4.4.c.txt","p5.4.c.txt","p6.4.c.txt"),
        ("g256_4_k.txt","p2.4.k.txt","p5.4.k.txt","p6.4.k.txt"),
        ("g146_2_n.txt","p1.2.n.txt","p4.2.n.txt","p6.2.n.txt"),
        ("g256_4_c.txt","p2.4.c.txt","p5.4.c.txt","p6.4.c.txt"),
        ("g146_2_c.txt","p1.2.c.txt","p4.2.c.txt","p6.2.c.txt"),
        ("g123_4_c.txt","p1.4.c.txt","p2.4.c.txt","p3.4.c.txt"),
        ("g356_2_c.txt","p3.2.c.txt","p5.2.c.txt","p6.2.c.txt"),
        ("g146_4_c.txt","p1.4.c.txt","p4.4.c.txt","p6.4.c.txt"),
        ("g456_2_c.txt","p4.2.c.txt","p5.2.c.txt","p6.2.c.txt"),
        ("g356_2_n.txt","p3.2.n.txt","p5.2.n.txt","p6.2.n.txt"),
        ("g123_2_k.txt","p1.2.k.txt","p2.2.k.txt","p3.2.k.txt"),
        ("g346_2_c.txt","p3.2.c.txt","p4.2.c.txt","p6.2.c.txt")
    )


    for name, *filenames in benchmarks:

        print(name)

        if filenames[2] == "":
            problem1 = utils.read_single_source(filenames[0])
            problem2 = utils.read_single_source(filenames[1])

            problem = utils.merge(problem1, problem2, name=name)
            utils.export(problem, "../tests/multi/")

        else:
            problem1 = utils.read_single_source(filenames[0])
            problem2 = utils.read_single_source(filenames[1])
            problem3 = utils.read_single_source(filenames[2])

            problem = utils.merge(problem1, problem2, problem3, name=name)
            utils.export(problem, "../tests/multi/")

