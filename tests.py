from pprint import pprint

__author__ = 'quirell'

from cso import CSOSolver,Cockroach
from data import Data
import copy

d = Data()
c = d.gettestcases()

for x in c:
    x.load()
    assert x.size is not None
    if x.solution is not None:
        assert x.value is not None
        assert len(x.solution) == x.size
    assert len(x.flow) == x.size
    assert len(x.distance) == x.size


for x in c:
    x.load()
tc = sorted(c,key = lambda tc:tc.size)[5]

solver = CSOSolver(tc,1)
cr = Cockroach(copy.copy(tc.solution))

solver.globalfitness([cr])
assert cr.value == tc.value


crcpy = copy.deepcopy(cr)
crcpy.solution.reverse()

assert cr - crcpy == tc.size/2

crcpy = copy.deepcopy(cr)
assert cr - crcpy == 0


cr.solution[0],cr.solution[1] = cr.solution[1],cr.solution[0]

assert cr - crcpy == 1

cr.solution[4],cr.solution[6] = cr.solution[6],cr.solution[4]

assert cr - crcpy == 2

cr.solution[2],cr.solution[5] = cr.solution[5],cr.solution[2]

assert cr - crcpy == 3

cr.solution[3],cr.solution[7] = cr.solution[7],cr.solution[3]
cr.solution[4],cr.solution[8] = cr.solution[8],cr.solution[4]

assert cr - crcpy == 5

cr = crcpy
cr.movedto = 0
cr.movedfrom = 0
delta = cr.stepdelta(tc)
value = cr.value
solver.globalfitness([cr])
value = value + delta
assert value == cr.value

for _ in xrange(100):
    cr = crcpy
    cr.randomstep()
    delta = cr.stepdelta(tc)
    value = cr.value
    solver.globalfitness([cr])
    valuex = value + delta
    assert valuex == cr.value

solver = CSOSolver(tc,50,5)
res = solver.solve(1500)
pprint(res.solution)
print "val: ",res.value
pprint(tc.solution)
print "best val: ",tc.value
v = res.value
res.computevalue(tc)
print v," - ",res.value
assert v == res.value
