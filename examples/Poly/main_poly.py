import dga
from dga import dga as algo
import numpy as np

def J(x):
    if len(x) > 0:
        return np.sum(x)
    else:
        return 0

prob = dga.Problem()

prob.cost(J)
prob.state(lower_bound=1, upper_bound=3, bits=4, polyploid_min=0, polyploid_max=2)
# prob.state(lower_bound=-3, upper_bound=3, bits=4, polyploid_min=1, polyploid_max=1)

algo = dga.dga(max_generations=200)
out = algo(prob)
print(out['xopt'])

# a = dga.Gene(lower_bound=0, upper_bound=2, bits=2, polyploid_min=1, polyploid_max=2)
# b = dga.Gene(lower_bound=0, upper_bound=2, bits=2, polyploid_min=1, polyploid_max=2)
# a.polyploid_increment()
# # b.polyploid_increment()
# print(a.bitarray)
# print(b.bitarray)
# c, d = algo.generate_offspring([a],[b])
# print(c[0].bitarray)
# print(d[0].bitarray)
# # print(algo.generate_offspring(a, b))
