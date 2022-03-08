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

class Node:
    """
    An instance of this class represents a node to visit or
    a source some vehicles are starting from.
    It is used for the depot too.
    """
    def __init__(self, id, x, y, qty, *, vehicles=tuple(), issource=False, isdepot=False):
        """
        Initialise.

        :param id: The unique id of the node.
        :param x: The x-coordinateof the node.
        :param y: The y-coordinate of the node.
        :param qty: The delivery quantity associated to this node.
        :param issource: A boolean variable that says if the node is a source.
        :param isdepot: A boolean variable that says if the node is the depot.
        :param vehicles: The vehicles starting from this node (if it is a source).
        """
        self.id = id
        self.x = x
        self.y = y
        self.qty = qty
        self.vehicles = vehicles
        self.issource = issource
        self.isdepot = isdepot

        # Attributes used by nearest neighbour
        #self.assigned = False
        #self.preferences = collections.deque()
        #self.nodes = collections.deque()

        # Attributes used by the PJS
        #self.from_source = 0
        #self.to_depot = 0
        #self.route = None
        #self.link_left = False
        #self.link_right = False

    @property
    def n_vehicles (self):
        return len(self.vehicles)

    def __copy__(self):
        obj = Node.__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self):
        return f"Node {self.id}"

    def __hash__(self):
        return self.id
