import numpy as np

from bitarray import bitarray
from numpy.random import randint, rand
from math import floor

from ._gene import _b2to10, _b10to2

class Gene(object):
    '''
    Gene class encoding information of a single variable into a string.
    Uses bitarray as a subclass (lol no it doesn't).
    '''
    def __new__(cls, *args, **kwargs):
        obj = super(Gene, cls).__new__(cls)

        obj.bits = kwargs.get('bits', 4)
        obj.lower_bound = kwargs.get('lower_bound', 0.0)
        obj.upper_bound = kwargs.get('upper_bound', 1.0)
        obj._build_default_bit_array(obj.bits)
        obj._set_coarse()

        return obj

    def bitFlip(self, location):
        self.bitarray[location] = not self.bitarray[location]

    def decode(self):
        ''' Decodes the current gene to the floating point number it represents. '''
        return self.coarse*_b2to10(self.bitarray) + self.lower_bound

    def encode(self, value):
        ''' Encode a specific value into the gene. Note: this isn't needed unless an initial population is provided. '''
        lchrom = self.bits
        temp = (value - self.lower_bound) / self.coarse
        b10 = round(temp)
        gen = _b10to2(b10, self.bits)
        self.bitarray = bitarray(gen)

    def init_random(self):
        self.bitarray = bitarray([randint(2,size=1) for _ in range(self.bits)])

    def mutate(self, Pm):
        for ii in range(len(self.bitarray)):
            coin_toss = rand()
            if coin_toss < Pm:
                self.bitFlip(ii)

    def __getitem__(self, item):
        return self.bitarray[item]

    def _build_default_bit_array(self, bits):
        self.bitarray = bitarray(bits)

    def _set_coarse(self):
        self.coarse = (self.upper_bound - self.lower_bound) / ((2 ** self.bits) - 1)
