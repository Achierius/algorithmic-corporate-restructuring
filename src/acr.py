import inspect
import sys
import functools
import itertools
import math
import operator
import random

def solve(solver, group, indexer, permuter, cost):
    assert callable(solver)
    assert callable(indexer)
    assert callable(permuter)
    assert callable(cost)
    # TODO: Add annotation support & annotation checking

    return solver(indexer(group), permuter(indexer(group)), cost)

def list_index(lst):
    assert isinstance(lst, list)
    return lst

def list_permute(lst):
    combs = list()
    for i in range(len(lst)):
        combs.extend(itertools.combinations(lst, i))
    return [i for i in combs if len(i) > 0]

def min_weighted_set_cover_solver(elements, subsets, cost):
    uncovered = elements.copy()
    used_subsets = list()

    def intersection(sa, sb):
        return [item for item in sa if item in sb]

    def choose_ratio(subset):
        if not len(intersection(subset, uncovered)):
            return math.inf
        return cost(subset) / len(intersection(subset, uncovered))

    if (len(elements) <= 1):
        return elements

    iterations = 0
    while len(subsets) > 0:
        subsets.sort(key=choose_ratio)
        subset = list(subsets.pop(0))

        new_subsets = list()
        for i in subsets:
            if len(intersection(subset, i)) == 0:
                new_subsets.append(i);
        subsets = new_subsets

        used_subsets.append(subset)
        iterations += 1

    return used_subsets
    
def eccentricity(subset, dists):
    assert callable(dists)
    return [max([dists(i, item) for i in subset]) for item in subset]

def avg_eccentricity(subset, dists):
    assert callable(dists)
    return sum(eccentricity(subset, dists))/len(subset)

def max_eccentricity(subset, dists):
    assert callable(dists)
    return functools.reduce(max, eccentricity(subset, dists))

def cf_avg_dist(subset, dists, bias):
    assert callable(dists)
    aci = bias
    for i in subset:
        for j in subset:
            aci += dists(i, j)
    aci /= len(subset)
    return aci

def c_arg_3(func, arg_3):
    def newfunc(arg_1, arg_2):
        return func(arg_1, arg_2, arg_3)
    return newfunc

def cost_ecc(function, dists):
    assert callable(function)
    def new_ecc_func(subset):
        return function(subset, dists)
    return new_ecc_func

def busops_main(roles, bias, aggregate):
    def test_solve (lst, cost_func):
        return solve(min_weighted_set_cover_solver, lst, list_index, list_permute, cost_func)

    r_n = {} # Names of various responsibilities w/in busops
    r_c = {} # Connectedness of various responsibilities w/in busops (non-transitive!)

    r_n[0] = "Grants"
    r_n[1] = "Sponsors"
    r_n[2] = "B/A/I-C"
    r_n[3] = "Soc. Med"
    r_n[4] = "Demos"
    r_n[5] = "Comms"
    r_n[6] = "Collabs"
    r_n[7] = "PhotVid"
    r_n[8] = "Website"
    r_n[9] = "Graphics"

    # My opinions only
    if not aggregate:
        r_c[0] = [5]
        r_c[1] = [4, 5]
        r_c[2] = [3, 0, 5]
        r_c[3] = [1, 3, 0, 5]
        r_c[4] = [0, 4, 0, 1, 5]
        r_c[5] = [0, 3, 0, 4, 0, 5]
        r_c[6] = [0, 2, 0, 0, 0, 3, 5]
        r_c[7] = [0, 0, 0, 4, 3, 2, 1, 5]
        r_c[8] = [2, 1, 0, 3, 3, 4, 3, 3, 5]
        r_c[9] = [0, 0, 0, 1, 0, 0, 0, 4, 3, 5]
    # Average of all surveyed connectivity opinions
    else:
      #  r_c[0] = [5]
      #  r_c[1] = [4, 5]
      #  r_c[2] = [4, 2.5, 5]
      #  r_c[3] = [1.5, 3.5, 0, 5]
      #  r_c[4] = [1, 3, 0, 2.5, 5]
      #  r_c[5] = [0, 2, 0, 4.5, 2, 5]
      #  r_c[6] = [0, 3, 0.5, 1.5, 2.5, 3.5, 5]
      #  r_c[7] = [0, 1.5, 0, 4.5, 3.5, 3.5, 2, 5]
      #  r_c[8] = [1, 1, 0, 3, 3, 4, 3.5, 3.5, 5]
      #  r_c[9] = [0, 1, 0, 2.5, 0, 1.5, 1, 3.5, 3, 5]
        r_c[0] = [5]
        r_c[1] = [3.7, 5]
        r_c[2] = [4.0, 2.7, 5]
        r_c[3] = [1.0, 2.7, 0.0, 5]
        r_c[4] = [0.7, 2.3, 0.0, 3.0, 5]
        r_c[5] = [0.0, 1.3, 0.0, 3.7, 1.7, 5]
        r_c[6] = [0.0, 2.3, 0.3, 2.0, 3.0, 3.3, 5]
        r_c[7] = [0.0, 1.3, 0.0, 4.0, 3.3, 3.0, 2.3, 5]
        r_c[8] = [1.0, 0.7, 0.0, 3.0, 2.3, 3.3, 3.0, 3.3, 5]
        r_c[9] = [0.0, 1.7, 0.0, 2.7, 0.7, 2.0, 1.3, 3.0, 3, 5]

    def busops_dist(a, b):
        least = min(a, b)
        most = max(b, a)
        return 1 - (r_c[most][least]*0.2)# + random.random()/10

    result = test_solve(roles,
                        cost_ecc(c_arg_3(cf_avg_dist, bias),
                        busops_dist))

    text_result = list(map(lambda x: [r_n[i] for i in x], result))

    return text_result, [cf_avg_dist(i, busops_dist, 0) for i in result]

if __name__ == "__main__":

    roles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    aggregate = True

    # Default: Run through a comfy range of biases and output each result
    if len(sys.argv) < 2:
        biases = [1, 1.5, 2, 2.5, 3]
        for bias in biases:
            result, costs = busops_main(roles, bias, aggregate)

            print("Bias: ", bias)
            print("Total Cost: ",
                  round(sum(map(lambda x: round(x, 2), costs)), 3))
            for group, cost in zip(result, map(lambda x: round(x, 2), costs)):
                print(" ", group, " : ", cost)
            print(" ")
    # Use command line arguments
    else:
        if len(sys.argv) >= 3:
            aggregate = bool(int(sys.argv[2]))
            print(aggregate)
        bias = float(sys.argv[1])
        result, costs = busops_main(roles, bias, aggregate)

        print("Bias: ", bias)
        print("Total Cost: ",
              round(sum(map(lambda x: round(x, 2), costs)), 3))
        for group, cost in zip(result, map(lambda x: round(x, 2), costs)):
            print(" ", group, " : ", cost)
        print(" ")


