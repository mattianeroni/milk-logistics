"""
This file contains method used to convert classic Multi Source Team Orieteering Problems into
the problem we face instead.

"""
import os
import numpy as np
import math



def _euclidean (inode, jnode):
    x1, y1, _ = inode
    x2, y2, _ = jnode
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)



def _capacities_to_txt (lst):
    return "-".join([str(i) for i in lst])


if __name__ == '__main__':
    filenames = os.listdir("./TOP/")

    for filename in filenames:
        with open(f"./TOP/{filename}", "r") as file:
            # Read problem parameters
            line1 = next(file)
            line2 = next(file)
            _ = next(file)
            n_nodes = int(line1.replace('\n','').split(' ')[1])
            n_vehicles = int(line2.replace('\n','').split(' ')[1])
            #_ = float(line3.replace('\n','').split(' ')[1])

            nodes, total_qty = [], 0
            for line in file:
                node_info = line.split('\t')
                nodes.append((float(node_info[0]), float(node_info[1]), int(node_info[2])))
                total_qty +=  int(node_info[2])

            dists = np.array([[_euclidean(n1,n2) for n2 in nodes] for n1 in nodes])

            # The capacity of the vehicles is calculated to be enough to fulfill
            # all the customers and is randomly assigned to the different vehicles
            _assign = np.random.rand(n_vehicles)
            _assign /= _assign.sum()
            capacity = (_assign * total_qty + 1).astype("int32")
            Tmax = dists.mean().astype("int32") * n_nodes

            with open(f"./single/{filename}", "w") as outfile:
                outfile.write(line1)
                outfile.write(line2)
                outfile.write(f"tmax {Tmax}\n")
                n = nodes[0]
                outfile.write(f"{n[0]}\t{n[1]}\t{n[2]}\t1\t{_capacities_to_txt(capacity.tolist())}\n")
                for n in nodes[1:]:
                    outfile.write(f"{n[0]}\t{n[1]}\t{n[2]}\t0\t\n")
