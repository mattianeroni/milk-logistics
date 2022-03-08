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



class Route:
    """
    An instance of this class represents a Route --i.e., a path
    from the source to the depot made by a vehicle.
    """
    def __init__(self, source, depot, vehicle):
        """
        Initialise.
        :param source: The source of the route.
        :param depot: The depot of the route.
        :param vehicle: The vehicle that will run this route.

        :attr nodes: The nodes part of the route.
        :attr qty: The total delivered quantity of the route.
        :attr cost: The total cost of the route (i.e., its length).
        """
        self.source = source
        self.depot = depot
        self.vehicle = vehicle
        self.nodes = collections.deque()
        self.qty = 0
        self.cost = 0
