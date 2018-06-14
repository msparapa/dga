import numpy as np

from bitarray import bitarray
from numpy.random import randint, rand
from math import floor
from dga.utils import keyboard

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
        obj.polyploid_min = kwargs.get('polyploid_min', 1)
        obj.polyploid_max = kwargs.get('polyploid_max', 1)
        # obj.polyploid_num = kwargs.get('polyploid_num', 1)
        obj._build_default_bit_array(obj.bits, 1)
        obj._set_coarse()

        return obj

    def bitFlip(self, poly, location):
        self.bitarray[poly][location] = not self.bitarray[poly][location]

    def decode(self):
        ''' Decodes the current gene to the floating point number it represents. '''
        return np.array([self.coarse*self._b2to10(arr) + self.lower_bound for arr in self.bitarray])

    def encode(self, value):
        ''' Encode a specific value into the gene. Note: this isn't needed unless an initial population is provided. '''
        lchrom = self.bits
        temp = (value - self.lower_bound) / self.coarse
        b10 = round(temp)
        gen = self._b10to2(b10, self.bits)
        # self.bitarray[poly] = bitarray(gen)
        return bitarray(gen)

    def init_random(self):
        return bitarray([randint(2,size=1) for _ in range(self.bits)])

    def mutate(self, Pm, PPoly):
        for ii in range(len(self.bitarray)):
            for jj in range(len(self.bitarray[ii])):
                coin_toss = rand()
                if coin_toss < Pm:
                    self.bitFlip(ii, jj)
        coin_toss = rand()
        if coin_toss < PPoly:
            coin_toss = rand()
            if coin_toss < 0.5:
                self.polyploid_decrement()
            else:
                self.polyploid_increment()

    def polyploid_decrement(self, *args, **kwargs):
        if len(self.bitarray) > self.polyploid_min:
            d = randint(0,len(self.bitarray))
            del self.bitarray[d]

    def polyploid_increment(self, *args, **kwargs):
        if len(self.bitarray) < self.polyploid_max:
            if len(args) is None or len(args) is 0:
                self.bitarray.append(self.init_random())
            else:
                self.bitarray.append(self.encode(args[0]))
                np.float

    def __getitem__(self, item):
        return self.bitarray[item]

    @staticmethod
    def _b2to10(arr):
        b10 = 0
        loc = len(arr)-1
        for ii in range(len(arr)):
            b10 += arr[loc]*(2**ii)
            loc -= 1

        return b10

    @staticmethod
    def _b10to2(value, bits):
        b2 = list()
        for ii in range(bits-1, -1, -1):
            bit_temp = floor(value/(2**ii))
            b2.append(bit_temp)
            value -= bit_temp*(2**ii)

        return b2

    def _build_default_bit_array(self, bits, poly):
        self.bitarray = [bitarray(bits) for L in range(poly)]

    def _set_coarse(self):
        self.coarse = (self.upper_bound - self.lower_bound) / ((2 ** self.bits) - 1)
