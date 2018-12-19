from math import floor

cpdef _b2to10(arr):
    cdef int loc
    b10 = 0
    loc = len(arr) - 1
    for ii in range(len(arr)):
        b10 += arr[loc] * (2 ** ii)
        loc -= 1

    return b10

def _b10to2(value, bits):
    b2 = list()
    for ii in range(bits - 1, -1, -1):
        bit_temp = floor(value / (2 ** ii))
        b2.append(bit_temp)
        value -= bit_temp * (2 ** ii)

    return b2
