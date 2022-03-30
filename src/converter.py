import os
import itertools
import collections
import utils 


if __name__ == '__main__':

    filenames = os.listdir("../tests/single/")

    for filename in filenames:
        #print(filename)

        lines = []
        m = 0
        Tmax = 1000
        total_revenue = 0

        with open("../tests/single/" + filename, "r") as infile:

            for i, line in enumerate(infile):
                if i == 1:
                    m = int(line.replace("\n", "").replace(" ", "\t").split("\t")[1])
                

                lines.append(line.replace("\n", "").replace(" ", "\t"))
                if i > 2:
                    revenue = int(line.replace("\n", "").replace(" ", "\t").split("\t")[2])
                    total_revenue += revenue

        revenue = int( (total_revenue / m) * 5 ) + 1
        revstring = "-".join([str(revenue) for _ in range(m)]) 

        with open("../tests/single2/" + filename, "w") as file:

            for i, line in enumerate( lines ):
                
                if i == 2:
                    file.write(f"tmax\t{Tmax}")
                else:
                    file.write(line)
                    if i == 3:
                        file.write(f"\t1\t{revstring}") 
                    
                    elif i > 3:
                        file.write("\t0")
                
                file.write("\n")


    filenames = os.listdir("../tests/single2/")
    clusters = collections.defaultdict(list)
    for filename in filenames:
        clusters[filename[1]].append(filename)

    combinations = []
    for key, lst in clusters.items():
        combinations.append( (f"p{key}.2.a.txt", f"p{key}.4.a.txt",) )

    combinations = sorted(combinations)

    for (p1a, p1b), (p2a, p2b) in itertools.combinations(combinations, 2):
        problem1 = utils.read_single_source(p1a, path="../tests/single2/")
        problem2 = utils.read_single_source(p2a, path="../tests/single2/")
        problem = utils.merge(problem1, problem2, name=f"p{p1a[1]}{p2a[1]}_2.txt")
        utils.export(problem, "../tests/multi/")
        
        problem1 = utils.read_single_source(p1b, path="../tests/single2/")
        problem2 = utils.read_single_source(p2b, path="../tests/single2/")
        problem = utils.merge(problem1, problem2, name=f"p{p1a[1]}{p2a[1]}_4.txt")
        utils.export(problem, "../tests/multi/")
        #utils.plot(problem)


    for (p1a, p1b), (p2a, p2b), (p3a, p3b) in itertools.combinations(combinations, 3):
        problem1 = utils.read_single_source(p1a, path="../tests/single2/")
        problem2 = utils.read_single_source(p2a, path="../tests/single2/")
        problem3 = utils.read_single_source(p3a, path="../tests/single2/")
        problem = utils.merge(problem1, problem2, problem3, name=f"p{p1a[1]}{p2a[1]}{p3a[1]}_2.txt")
        utils.export(problem, "../tests/multi/")
        
        problem1 = utils.read_single_source(p1b, path="../tests/single2/")
        problem2 = utils.read_single_source(p2b, path="../tests/single2/")
        problem3 = utils.read_single_source(p3b, path="../tests/single2/")
        problem = utils.merge(problem1, problem2, problem3, name=f"p{p1a[1]}{p2a[1]}{p3a[1]}_4.txt")
        utils.export(problem, "../tests/multi/")
        #utils.plot(problem)



    """

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
            vehicle.capacity =  9_999_999 #route.qty
            Tmax = max( Tmax, route.cost )
            #print("after ", id(vehicle),  vehicle.capacity)
        problem.Tmax = round(Tmax ,  2)
        #for route in routes:
        #    route.vehicle.capacity = maxcap


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
    """
