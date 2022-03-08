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

class Edge:
    """
    An instance of this class represents an edge connecting two nodes to visit.

    Only edges connecting nodes to visit to each other are instantiated.
    We don't need edges connecting sources to nodes and nodes to depot.
    """
    def __init__(self, inode, jnode, cost):
        """
        Initialise.
        :param inode: The starting node.
        :param jnode: The ending node.
        :param cost: The length of the path from inode to jnode.
        """
        self.inode = inode
        self.jnode = jnode
        self.cost = cost
        self.savings = dict()
