from dga.Gene import Gene
import numpy as np

a = Gene(bits=2, lower_bound=0, upper_bound=3)
a.encode(0)
a.bitFlip(0)
arr = a.bitarray

def conv(bitsr):
    loc = len(bitsr)
    rev = np.flip(bitsr, axis=0)
    ipow = np.arange(start=0,stop=loc,step=1)
    b10 = sum(rev*(2**ipow))
    # for ii in range(len(bitsr)):
    #     b10 += bitsr[loc]*(2**ii)
    #     loc -= 1

    return b10

print('Original: ' + str(a._b2to10(arr)))
print('New: ' + str(conv(arr)))