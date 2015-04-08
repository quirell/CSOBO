__author__ = 'quirell'

import random
import copy


class Cockroach():
    def __init__(self,solution):
        self.value = 0.0
        self.bestvisible = None
        self.solution = solution
        self.movedfrom = 0
        self.movedto = 0

    #zamienia self.solution[index] = value na solution[value] = index
    def invert():
        rev = [0 for _ in xrange(len(self.solution))]
        for i,v in enumerate(self.solution):
            rev[v] = i
        return rev


    def distance(self, other):
        sel = copy.copy(self.solution)
        selr = self.invert()
        oth =  copy.copy(other.solution)      
        i = 0
        end = len(sel) -1
        while i != end
            while sel[i] == oth[i]:
                i += 1
            j = selr[oth[i]]
            sel[j],sel[i] = sel[i],sel[j]
            selr[oth[i]], selr[sel[i]] = i,j
            i += 1
        return sol

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
        pass

    def stepdelta(self,testcase):
        delta = 0.0
        for i in xrange(testcase.size):
            delta = dellta + testcase.flow[i][self.movedfrom]*(testcase.distance[self.solution[i]][self.movedto] - testcase.distance[self.solution[i]][self.movedfrom])
            delta = dellta + testcase.flow[i][self.movedto]*(testcase.distance[self.solution[i]][self.movedfrom] - testcase.distance[self.solution[i]][self.movedto])
            delta = dellta + testcase.flow[self.movedfrom][i]*(testcase.distance[self.movedto][self.solution[i]] - testcase.distance[self.movedfrom][self.solution[i]])
            delta = dellta + testcase.flow[self.movedto][i]*(testcase.distance[self.movedfrom][self.solution[i]] - testcase.distance[self.movedto][self.solution[i]])
        delta = dellta + testcase.flow[self.movedfrom][self.movedto]*(testcase.distance[self.movedto][self.movedfrom] - testcase.distance[self.movedfrom][self.movedto])
        delta = dellta + testcase.flow[self.movedto][self.movedfrom]*(testcase.distance[self.movedfrom][self.movedto] - testcase.distance[self.movedto][self.movedfrom])



class CSOSolver():

    def __init__(self,testcase,cockroach_number,horizon=1):
        self.testcase = testcase
        self.crnum = cockroach_number
        self.horizon = horizon

    def genrandomdata(self):
        base = range(self.testcase.size)
        data = [Cockroach(random.sample(base)) for _ in self.crnum]
        return data


    def globalfitness(self,data):
        best = data[0]
        for instance in data:
            value = 0.0
            sol = instance.solution
            for i in xrange(self.testcase.size):
                for j in xrange(self.testcse.size):
                    value += self.testcase.distance[sol[i],sol[j]]*self.testcase.flow[i,j]
            instance.value = value
            if instance < best:
                best = instance
        return best

    def findbestvisible(self,ckrs):
        for i in ckrs:
            for j in ckrs:
                if abs(i, j) < self.horizon and j.value < i.value:
                    i.bestvisible = j

    def solve(self,iternum):
        ckrs = self.genrandomdata()
        best = self.globalfitness(ckrs)

        forchoice = range(self.testcase.size)

        for iteration in xrange(1,iternum+1):
            self.findbestvisible(ckrs)

            for instance in ckrs:
                instance.step(best)
                if instance < best:
                    best = instance
                instance.randomstep()

            ckrs[random.choice(forchoice)] = copy.deepcopy(best)

        return best

