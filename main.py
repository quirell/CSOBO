
__author__ = 'quirell'

from cso import CSOSolver,Cockroach
from data import Data
import copy

d = Data()
c = d.gettestcases()

for x in c:
    x.load()
    try:
        assert x.size is not None
        if x.solution is not None:
            assert x.value is not None
            assert len(x.solution) == x.size
        assert len(x.flow) == x.size
        assert len(x.distance) == x.size
    except AssertionError:
        x = 1

for x in c:
    x.load()
tc = sorted(c,key = lambda tc:tc.size)[5]

solver = CSOSolver(tc,1)
cr = Cockroach(copy.copy(tc.solution))

solver.globalfitness([cr])
assert cr.value == tc.value


crcpy = copy.deepcopy(cr)
crcpy.solution.reverse()

assert cr.distance(crcpy) == tc.size/2

assert cr.distance(cr) == 0

crcpy = copy.deepcopy(cr)
cr.solution[0],cr.solution[1] = cr.solution[1],cr.solution[0]

assert cr.distance(crcpy) == 1

cr.solution[4],cr.solution[6] = cr.solution[6],cr.solution[4]

assert cr.distance(crcpy) == 2

cr.solution[2],cr.solution[5] = cr.solution[5],cr.solution[2]

assert cr.distance(crcpy) == 3

cr.solution[3],cr.solution[7] = cr.solution[7],cr.solution[3]
cr.solution[4],cr.solution[8] = cr.solution[8],cr.solution[4]

assert cr.distance(crcpy) == 5

cr = crcpy
cr.solution[0],cr.solution[1] = cr.solution[1],cr.solution[0]
cr.movedto = 1
cr.movedfrom = 0
delta = cr.stepdelta(tc)
value = cr.value
solver.globalfitness([cr])
value = value + delta
assert value == cr.value