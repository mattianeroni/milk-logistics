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
import math
import random


def GRASP (options, n=5):
    """
    This method carry out a GRASP selection over a set of options.
    :param otions: The possible options.
    :param n: The selection is made on first n options.
    :return: The selected option.
    """
    L = len(options)
    _options = list(options)
    for _ in range(L):
        idx = random.randint(0, min(n, len(_options) - 1))
        yield _options.pop(idx)



def BRA (options, beta=0.3):
    """
    This method carry out a biased-randomised selection. The selection is based
    on a quasi-geometric function:

                    f(x) = (1 - beta) ^ x

    and it therefore prioritise the first elements in list.

    :param options: The set of options already sorted from the best to the worst.
    :param beta: The parameter of the quasi-geometric distribution.
    :return: The element picked at each iteration.
    """
    L = len(options)
    _options = list(options)
    for _ in range(L):
        idx = int(math.log(random.random(), 1.0 - beta)) % len(_options)
        yield _options.pop(idx)



def single_BRA (options, beta=0.3):
    """
    This method is a single iteration of the BRA.
    """
    idx = int(math.log(random.random(), 1.0 - beta)) % len(_options)
    return options[idx]



def single_GRASP (options, n=5):
    """
    This method is a single iteration of the GRASP.
    """
    return random.choice(options[:n])
