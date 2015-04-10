__author__ = 'quirell'

import random
import copy
import pprint

class Cockroach():
    def __init__(self,solution):
        self.value = 0.0
        self.bestvisible = None
        self.solution = solution
        self.movedfrom = 0
        self.movedto = 0

    #zamienia self.solution[index] = value na solution[value] = index
    def invert(self):
        rev = [0 for _ in xrange(len(self.solution))]
        for i,v in enumerate(self.solution):
            rev[v] = i
        return rev

    def innerstep(self,sel,selr,oth,func):
        i = 0
        end = len(sel) -1
        while True:
            while i != end and sel[i] == oth[i]:
                i += 1
            if i == end:
                break
            j = selr[oth[i]]
            sel[j],sel[i] = sel[i],sel[j]
            selr[oth[i]], selr[sel[i]] = i,j
            if func(j,i):
                break
            i += 1

    def distance(self, other, endstep=10000000):
        sel = copy.copy(self.solution)
        selr = self.invert()
        oth = other.solution

        class Dist:
            def __init__(self):
                self.dist = 0
            def __call__(self, *args, **kwargs):
                self.dist += 1
                return False

        dist = Dist()
        self.innerstep(sel,selr,oth,dist)
        return dist.dist

    def savestep(self,i,j):
        self.movedfrom = i
        self.movedto = j
        return True

    def step(self, bestinstance):
        self.movedfrom = self.movedto = 0
        if self.bestvisible is not None and self.value != self.bestvisible.value:
            self.innerstep(self.solution,self.invert(),self.bestvisible.solution,self.savestep)
        else:
            self.innerstep(self.solution,self.invert(),bestinstance.solution,self.savestep)

    def randomstep(self):
        self.movedfrom = random.randint(0,len(self.solution)-1)
        self.movedto = random.randint(0,len(self.solution)-1)
        while self.movedto == self.movedfrom:
            self.movedto = random.randint(0,len(self.solution)-1)
        self.solution[self.movedfrom],self.solution[self.movedto] = self.solution[self.movedto],self.solution[self.movedfrom]

    def stepdelta(self,testcase):
        delta = 0
        mtd = self.solution[self.movedto]
        mfd = self.solution[self.movedfrom]
        f = testcase.flow
        d = testcase.distance

        for i in xrange(testcase.size):
            if i != self.movedfrom and i != self.movedto:
                si = self.solution[i]
                delta += f[i][self.movedto]*(d[si][mtd] - d[si][mfd])
                delta += f[self.movedto][i]*(d[mtd][si] - d[mfd][si])
                delta += f[i][self.movedfrom]*(d[si][mfd] - d[si][mtd])
                delta += f[self.movedfrom][i]*(d[mfd][si] - d[mtd][si])

        delta = delta + f[self.movedfrom][self.movedto]*(d[mfd][mtd] - d[mtd][mfd])
        delta = delta + f[self.movedto][self.movedfrom]*(d[mtd][mfd] - d[mfd][mtd])

        return delta

    def updatevalue(self,testcase):
        self.value = self.value + self.stepdelta(testcase)

    #jak updatevalue, ale liczy wartosc od 0 w czasie O(n^2) a nie O(n)
    def computevalue(self,testcase):
        value = 0
        sol = self.solution
        for i in xrange(testcase.size):
            for j in xrange(testcase.size):
                value += testcase.distance[sol[i]][sol[j]]*testcase.flow[i][j]
        self.value = value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __sub__(self, other):
        return self.distance(other)


class CSOSolver():

    def __init__(self,testcase,cockroach_number,horizon=1):
        self.testcase = testcase
        self.crnum = cockroach_number
        self.horizon = horizon

    def genrandomdata(self):
        base = range(self.testcase.size)
        data = []
        for _ in xrange(self.crnum):
            random.shuffle(base)
            data.append(Cockroach(copy.copy(base)))
        return data


    def globalfitness(self,data):
        best = data[0]
        for instance in data:
            instance.computevalue(self.testcase)
            if instance.value < best.value:
                best = instance

        return best

    def updatebestvisible(self,ckrs):
        for i in ckrs:
            for j in ckrs:
                if i - j < self.horizon and j.value < i.value:
                    i.bestvisible = j

    def solve(self,iternum):
        ckrs = self.genrandomdata()
        best = self.globalfitness(ckrs)
        forchoice = range(self.crnum)

        for iteration in xrange(1,iternum+1):

            self.updatebestvisible(ckrs)
            for instance in ckrs:
                instance.step(best)
                instance.updatevalue(self.testcase)

                if instance.value < best.value:
                    best = copy.deepcopy(instance)
                instance.randomstep()
                instance.updatevalue(self.testcase)


            ckrs[random.choice(forchoice)] = copy.deepcopy(best)
            print "iter ",iteration," bestval: ",best.value

        return best

