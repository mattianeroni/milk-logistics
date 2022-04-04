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
import math
import itertools
import collections
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json

import node
import edge
import vehicle


# Default colors for nodes, source nodes, adn depot
NODES_COLOR = '#FDDD71'
SOURCES_COLORS = ('#8FDDF4', '#8DD631', '#A5A5A5', '#DB35EF', '#8153AB', '#FFCC66', '#ff3399', '#3333ff')
DEPOT_COLOR = '#F78181'
VEHICLES_COLORS = ("40", "50", "60", "70", "80")



def euclidean (inode, jnode):
    """
    The euclidean distance between two nodes.

    :param inode: First node.
    :param jnode: Second node.
    """
    return round(math.sqrt((inode.x - jnode.x)**2 + (inode.y - jnode.y)**2), 3)



class Problem:
    """
    An instance of this class represents a single-source Team Orienteering
    Problem.

    It may also be translated according to different rules in a multi-source
    version of it.

    """

    def __init__(self, name, n_nodes, n_vehicles, Tmax, sources, nodes, depot):
        """
        Initialise.

        :param name: The name of the problem
        :param n_nodes: The number of nodes.
        :param n_vehicles: The number of vehicles / paths.
        :param Tmax: The maximum distance vehicles can run / time budget for paths.
        :param sources: The source nodes.
        :param nodes: The nodes to visit.
        :param depot: The depot.

        :attr dists: The matrix of distances between nodes.
        :attr positions: A dictionary of nodes positions.
        :attr edges: The edges connecting the nodes.
        """
        self.name = name
        self.n_nodes = n_nodes
        self.n_vehicles = n_vehicles
        self.Tmax = Tmax
        self.sources = sources
        self.nodes = nodes
        self.depot = depot

        # Initialise edges list and nodes positions
        edges = collections.deque()
        dists = np.zeros((n_nodes, n_nodes))
        # Calculate the matrix of distances and instantiate the edges
        # and define nodes colors and positions
        source_id = 0
        for node1, node2 in itertools.permutations(itertools.chain(sources, nodes, (depot,)), 2):
            # Calculate the edge cost
            id1, id2 = node1.id, node2.id
            cost = euclidean(node1, node2)
            # Compile the oriented matrix of distances
            dists[id1, id2] = cost

            if node1.isdepot or node1.issource or node2.isdepot or node2.issource:
                continue
            # Create the edge
            edges.append(edge.Edge(node1, node2, cost))

        # Compute savings
        for e in edges:
            id1, id2 = e.inode.id, e.jnode.id
            e.savings = { s.id : dists[s.id, id2] + dists[id1, depot.id] - e.cost for s in sources}

        self.dists = dists
        self.edges = edges


    def __hash__(self):
        return id(self)


    def __repr__(self):
        return f"""
        Problem {self.name}
        ---------------------------------------------
        nodes: {self.n_nodes}
        vehicles: {self.n_vehicles}
        Tmax: {self.Tmax}
        multi-source: {self.multi_source}
        ---------------------------------------------
        """

    @property
    def multi_source (self):
        """ A property that says if the problem is multi-source or not. """
        return len(self.sources) > 1


    def iternodes (self):
        """ A method to iterate over all the nodes of the problem (i.e., sources, customers, depot)"""
        return itertools.chain(self.sources, self.nodes, (self.depot,))



def plot (problem, *, routes=tuple(), mapping=None, figsize=(6,4), title=None):
    """
    This method is used to plot a problem using a graph representation that
    makes it easy-to-read.

    :param figsize: The size of the plot.
    :param title: The title of the plot.
    :param routes: The eventual routes found.
    """
    plt.figure(figsize=figsize)
    if title:
        plt.title(title)

    # Build the graph of nodes
    colors, pos = [], {}
    G = nx.DiGraph()
    source_id = 0
    n_sources = len(problem.sources)

    for node in problem.iternodes():
        # Compile the graph
        pos[node.id] = (node.x, node.y)
        G.add_node(node.id)

        # Define nodes colors
        if node.issource:
            colors.append(SOURCES_COLORS[source_id])
            source_id += 1
        elif node.isdepot:
            colors.append(DEPOT_COLOR)
        else:
            if mapping is None:
                colors.append(NODES_COLOR)
            else:
                n_vehicle = 0
                for i, source in enumerate(problem.sources):
                    for j in range(len(source.vehicles)):
                        n_vehicle += 1
                        if mapping[n_vehicle - 1, node.id] == 1:
                            colors.append(SOURCES_COLORS[i] + VEHICLES_COLORS[j])
                            break

    # Save the routes
    edges = []
    for r in routes:
        # NOTE: Nodes of the route are supposed to always be in the order in which
        # they are stored inside the deque.
        nodes = tuple(r.nodes)
        edges.extend([(r.source.id, nodes[0].id), (nodes[-1].id, r.depot.id)])
        for n1, n2 in zip(nodes[:-1], nodes[1:]):
            edges.append((n1.id, n2.id))

    nx.draw(G, node_color=colors, edgelist=edges, with_labels=True, node_size=100, font_size=6, font_weight="bold")
    plt.show()



def export (problem, path):
    """
    This method exports the problem into a text file.

    :param problem: The problem to export.
    :param path: The directory where the problem will be saved.
    """
    with open(path + problem.name, 'w') as file:

        file.write(f"n {problem.n_nodes}\n")
        file.write(f"m {problem.n_vehicles}\n")
        file.write(f"tmax {problem.Tmax}\n")

        for node in problem.iternodes():
            capacities = "-".join([str(int(v.capacity)) for v in node.vehicles ]) if node.issource else ""
            file.write(f"{round(node.x, 1)}\t{round(node.y, 1)}\t{node.qty}\t{int(node.issource)}\t{capacities}\n")




def read_real_problem (filename, path="../tests/casestudy/"):
    """
    This method is used to read a real case problem.

    :param filename: The file of delivery quantities to read.
    :param path: The directory where the file and the json of arcs are.
    :retun: A instance of problem.
    """
    problem = None 

    with open(path + filename, 'r') as file:

        # Read problem parameters
        n_nodes = int(next(file).replace('\n','').split(" ")[1])
        n_vehicles = int(next(file).replace('\n','').split(" ")[1])
        Tmax = int(next(file).replace('\n','').split(" ")[1])

        sources, nodes, depot = [], [], None
        vehicle_id = 0

        # Read nodes characteristics
        for i, line in enumerate(file):

            node_info = line.replace('\n', '').split(' ')

            #print(node_info, i, n_nodes - 1)

            # If the node is depot
            if i == n_nodes - 1:
                depot = node.Node(i, 0, 0, int(node_info[1]), isdepot=True)
                continue

            # If the node is source
            if i < n_nodes - 1 and node_info[1] == '0':
                vehicles = []
                for capacity in node_info[2].split("-"):
                    vehicles.append( vehicle.Vehicle( vehicle_id, int(capacity) ) )
                    vehicle_id += 1

                sources.append(node.Node(i, 0, 0, int(node_info[1]), issource=True, vehicles=tuple(vehicles)))
                continue 
            
            nodes.append(node.Node(i, 0, 0, int(node_info[1])))


        # Instantiate the problem
        problem = Problem(filename, n_nodes, n_vehicles, Tmax, tuple(sources), tuple(nodes), depot)


    # Read the distances 
    with open(path + "dists.json", "r") as file:
        d = json.load(file)
        problem.dists = np.asarray(d["dists"])


       
    # Instantiate edges
    edges = collections.deque()

    for node1, node2 in itertools.permutations(itertools.chain(sources, nodes, (depot,)), 2):
        if node1.isdepot or node1.issource or node2.isdepot or node2.issource:
            continue
        edges.append(edge.Edge(node1, node2, problem.dists[node1.id, node2.id] ))

    # Compute savings
    for e in edges:
        id1, id2 = e.inode.id, e.jnode.id
        e.savings = { s.id : problem.dists[s.id, id2] + problem.dists[id1, depot.id] - e.cost for s in sources}

    problem.edges = edges 

    return problem     






def read_benchmark (filename, path="../tests/benchmarks/"):
    """
    This method is used to read a benchmark problem created by
    changing the multi-source team orienteering benchmarks.

    :param filename: The name of the file to read.
    :param path: The path where the file is.
    :return: The problem instance.
    """
    with open(path + filename, 'r') as file:
        # Read problem parametersn_vehicles
        n_nodes = int(next(file).replace('\n','').replace(" ", "\t").split('\t')[1])
        n_vehicles = int(next(file).replace('\n','').replace(" ", "\t").split('\t')[1])
        Tmax = float(next(file).replace('\n','').replace(" ", "\t").split('\t')[1])
        # Initialise nodes lists
        sources, nodes, depot = [], [], None
        vehicle_id = 0
        # Read nodes characteristics
        for i, line in enumerate(file):
            node_info = line.replace('\n', '').split('\t')
            # If the node is depot
            if i == n_nodes - 1:
                depot = node.Node(i, float(node_info[0]), float(node_info[1]), int(node_info[2]), isdepot=True)
                continue
            # If the node is source
            if node_info[3] == '1':
                vehicles = []
                for capacity in node_info[4].split("-"):
                    vehicles.append(vehicle.Vehicle(vehicle_id, int(float(capacity))))
                    vehicle_id += 1

                sources.append(node.Node(i, float(node_info[0]), float(node_info[1]), int(node_info[2]),
                              issource=True, vehicles=tuple(vehicles)))
            else:
                # Add a node to visit
                nodes.append(node.Node(i, float(node_info[0]), float(node_info[1]), int(node_info[2])))

        # Instantiate and return the problem
        return Problem(filename, n_nodes, n_vehicles, Tmax, tuple(sources), tuple(nodes), depot)