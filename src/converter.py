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
        Tmax = 0
        for route in routes:
            vehicle = route.vehicle
            vehicle.capacity = route.qty 
            Tmax = max( Tmax, route.cost )
            #print("after ", id(vehicle),  vehicle.capacity)
        problem.Tmax = round(Tmax, 2)


        # Export the problem 
        utils.export(problem, "../tests/single/")
        