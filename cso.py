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

    def distance(self, other):
        return 0

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
        pass




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
                for j in xrange(i+1,self.testcse.size):
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

