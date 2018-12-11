from dga.gene import Gene

def test_gene_encode():
    a = Gene(bits=2,lower_bound=0,upper_bound=3)
    a.encode(0)
    assert a.bitarray[0] == False
    assert a.bitarray[1] == False
    a.encode(1)
    assert a.bitarray[0] == False
    assert a.bitarray[1] == True
    a.encode(2)
    assert a.bitarray[0] == True
    assert a.bitarray[1] == False
    a.encode(3)
    assert a.bitarray[0] == True
    assert a.bitarray[1] == True


def test_gene_decode():
    a = Gene(bits=2, lower_bound=0, upper_bound=3)
    a.encode(-0.3)
    assert a.decode() == 0
    a.encode(0.45)
    assert a.decode() == 0
    a.encode(0.55)
    assert a.decode() == 1
    a.encode(1.3)
    assert a.decode() == 1
    a.encode(1.9)
    assert a.decode() == 2
    a.encode(2.2)
    assert a.decode() == 2
    a.encode(2.7)
    assert a.decode() == 3
    a.encode(3.49)
    assert a.decode() == 3


def test_gene_bitflip():
    a = Gene(bits=2, lower_bound=0, upper_bound=3)
    a.encode(3)
    a.bitFlip(0)
    assert a.bitarray[0] == False
    assert a.bitarray[1] == True
    a.bitFlip(1)
    assert a.bitarray[0] == False
    assert a.bitarray[1] == False
    a.bitFlip(1)
    assert a.bitarray[0] == False
    assert a.bitarray[1] == True
    a.bitFlip(0)
    assert a.bitarray[0] == True
    assert a.bitarray[1] == True


