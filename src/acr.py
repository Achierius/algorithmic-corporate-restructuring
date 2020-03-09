import inspect
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
    

def avg_eccentricity(subset, dists):
    assert callable(dists)
    total = 0
    for item_a in subset:
        maximum = 0
        for item_b in subset:
            maximum = max(maximum, dists(item_a, item_b))
        total += maximum
    return total / len(subset)

def max_eccentricity(subset, dists):
    assert callable(dists)
    maximum = 0
    for item_a in subset:
        for item_b in subset:
            maximum = max(maximum, dists(item_a, item_b))
    return maximum

def testcostfunc_bias(subset, dists, bias):
    assert callable(dists)
    aci = bias
    for i in subset:
        for j in subset:
            aci += dists(i, j)
    aci /= len(subset)
    return aci

def testcostfunc(bias):
    def newfunc(subset, dists):
        return testcostfunc_bias(subset, dists, bias)
    return newfunc

def cost_ecc(function, dists):
    assert callable(function)
    def new_ecc_func(subset):
        return function(subset, dists)
    return new_ecc_func

def evaluate(solution, cost):
    assert callable(cost)
    total = 0
    for i in solution:
        total += cost(i)
    return total

def euc_dist(a, b):
    return abs(a - b)

def test_main(bias):
    #test_in  = [1, 2, 3, 4, 5, 6, 9, 11, 21]
    test_in = [round(random.random(), 2) for i in range(10)]

    #print ("Input: ", test_in)
    def test_solve (lst, cost_func):
        return solve(min_weighted_set_cover_solver, lst, list_index, list_permute, cost_func)

    #test_out_a = test_solve(test_in, cost_ecc(max_eccentricity, operator.add))
    #test_out_b = test_solve(test_in, cost_ecc(avg_eccentricity, operator.add))
    #print("Max Ecc: ", test_out_a, " w/ cost ", evaluate(test_out_a, cost_ecc(max_eccentricity, euc_dist)))
    #print("Avg Ecc: ", test_out_b, " w/ cost ", evaluate(test_out_b, cost_ecc(avg_eccentricity, euc_dist)))
    return test_solve(test_in, cost_ecc(testcostfunc(bias), euc_dist))

def busops_main(bias, aggregate):
    roles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   #roles = [3, 4, 5, 6, 7, 8, 9]
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
    else:
        r_c[0] = [5]
        r_c[1] = [4, 5]
        r_c[2] = [4, 2.5, 5]
        r_c[3] = [1.5, 3.5, 0, 5]
        r_c[4] = [1, 3, 0, 2.5, 5]
        r_c[5] = [0, 2, 0, 4.5, 2, 5]
        r_c[6] = [0, 3, 0.5, 1.5, 2.5, 3.5, 5]
        r_c[7] = [0, 1.5, 0, 4.5, 3.5, 3.5, 2, 5]
        r_c[8] = [1, 1, 0, 3, 3, 4, 3.5, 3.5, 5]
        r_c[9] = [0, 1, 0, 2.5, 0, 1.5, 1, 3.5, 3, 5]

    def busops_dist(a, b):
        least = min(a, b)
        most = max(b, a)
        return 1 - (r_c[most][least]*0.2)# + random.random()/10
    def parse_group(a):
        return [r_n[i] for i in a]

    result = test_solve(roles, cost_ecc(testcostfunc(bias), busops_dist))
    text_result = list(map(parse_group, result))

    #print (cost_ecc(testcostfunc(bias), busops_dist)([0, 0]))

    return text_result, [cost_ecc(testcostfunc(0), busops_dist)(i) for i in result]

if __name__ == "__main__":
    #entries = {}
    #trials = 25
    #for i in range (50):
    #    total = 0
    #    for j in range(trials):
    #        result = test_main(i / 10)
    #        #print("Fancy Cost Function: ", result, " w/ cost ", round(evaluate(result, cost_ecc(testcostfunc(i / 10), euc_dist)), 2))
    #        total += len(result)
    #    entries[i] = total/trials;
    #for entry in range (len(entries)):
    #    print ("Average # of Groupings w/ bias =  ", entry/10, ": ", entries[entry])
    #result = busops_main(0.1100000000000000074941)
    biases = [1, 1.5, 2, 2.5, 3]

    for bias in biases:
        result, costs = busops_main(bias, False)

        print("Bias: ", bias)
        print("Total Cost: ", round(sum(map(lambda x: round(x, 2), costs)), 3))
        for group, cost in zip(result, map(lambda x: round(x, 2), costs)):
            print(" ", group, " : ", cost)
        print(" ")

