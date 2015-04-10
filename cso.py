__author__ = 'quirell'

import random
import copy


class Cockroach():
    def __init__(self,solution):
        self.value = 0.0
        self.bestvisible = None
        self.solution = solution # solution[facility] = location
        self.movedfrom = 0
        self.movedto = 0

    #zamienia self.solution[index] = value na solution[value] = index
    def invert(self):
        rev = [0 for _ in xrange(len(self.solution))]
        for i,v in enumerate(self.solution):
            rev[v] = i
        return rev


    def distance(self, other):
        sel = copy.copy(self.solution)
        selr = self.invert()
        oth = copy.copy(other.solution)
        dist = 0
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
            dist += 1
        return dist

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __sub__(self, other):
        return self.distance(other)

    def step(self, bestinstance):
        if self.value != self.bestvisible.value:
            #self.value = krok w kierunku bestvisible
            pass
        else:
            #self.value = krok w kierunku bestinstance
            pass

    def randomstep(self):
        self.movedfrom = random.randint(len(self.solution))
        self.movedto = random.randint(len(self.solution))


    def stepdelta(self,testcase):
        delta = 0
        mtd = self.solution[self.movedto]
        mfd = self.solution[self.movedfrom]
        f = testcase.flow
        d = testcase.distance

        for i in xrange(testcase.size):
            if i == self.movedfrom or i == self.movedto:
                continue
            si = self.solution[i]
            delta += f[i][self.movedto]*(d[si][mtd] - d[si][mfd])
            delta += f[self.movedto][i]*(d[mtd][si] - d[mfd][si])
            delta += f[i][self.movedfrom]*(d[si][mfd] - d[si][mtd])
            delta += f[self.movedfrom][i]*(d[mfd][si] - d[mtd][si])
        delta = delta + f[self.movedfrom][self.movedto]*(d[mfd][mtd] - d[mtd][mfd])
        delta = delta + f[self.movedto][self.movedfrom]*(d[mtd][mfd] - d[mfd][mtd])
        return delta


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
            value = 0
            sol = instance.solution
            for i in xrange(self.testcase.size):
                for j in xrange(self.testcase.size):
                    value += self.testcase.distance[sol[i]][sol[j]]*self.testcase.flow[i][j]
            instance.value = value
            if instance < best:
                best = instance
        return best

    def updatebestvisible(self,ckrs):
        for i in ckrs:
            for j in ckrs:
                if abs(i - j) < self.horizon and j.value < i.value:
                    i.bestvisible = j

    def solve(self,iternum):
        ckrs = self.genrandomdata()
        best = self.globalfitness(ckrs)

        forchoice = range(self.testcase.size)

        for iteration in xrange(1,iternum+1):
            self.updatebestvisible(ckrs)

            for instance in ckrs:
                instance.step(best)
                if instance < best:
                    best = instance
                instance.randomstep()

            ckrs[random.choice(forchoice)] = copy.deepcopy(best)

        return best

