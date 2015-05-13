__author__ = 'quirell'

import random
import copy
import pprint


class NSteps():

    def __init__(self,steps=2):
        self.steps = steps

    def __call__(self, *args, **kwargs):
        self.steps -= 1
        if self.steps == 0:
            return True
        return False

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

    def step(self, bestinstance,customStepsController = None):
        self.movedfrom = self.movedto = 0
        if customStepsController == None:
            customStepsController =self.savestep;
        if self.bestvisible is not None and self.value != self.bestvisible.value:
            self.innerstep(self.solution,self.invert(),self.bestvisible.solution,customStepsController)
        else:
            #to miejsce mnie zastanawia
        #   self.randomstep()
           self.innerstep(self.solution,self.invert(),bestinstance.solution,customStepsController)

    def randomstep(self):
        self.movedfrom = random.randint(0,len(self.solution)-1)
        self.movedto = random.randint(0,len(self.solution)-1)
        while self.movedto == self.movedfrom:
            self.movedto = random.randint(0,len(self.solution)-1)
        self.solution[self.movedfrom],self.solution[self.movedto] = self.solution[self.movedto],self.solution[self.movedfrom]

    def fullrandom(self):
        random.shuffle(self.solution)

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

    def __init__(self,testcase,cockroach_number,horizon,stepnumber, random_type, bonanza_flag,iternum,app, event):
        self.testcase = testcase
        self.crnum = cockroach_number
        self.horizon = horizon
        self.stepnumber = stepnumber
        self.random_type = random_type
        self.bonanza_flag = bonanza_flag
        self.iternum = iternum
        self.app = app
        self.event = event

    def badlookingstop(self):
        self.iternum = 0

    def genrandomdata(self):
        base = range(self.testcase.size)
        data = []
        for _ in xrange(self.crnum):
            random.shuffle(base)
            data.append(Cockroach(copy.copy(base)))
        return data


    def globalfitness(self,data):
        localbest = data[0]
        for instance in data:
            instance.computevalue(self.testcase)
            if instance.value < localbest.value:
                localbest = instance

        return localbest

    def updatebestvisible(self,ckrs):
        for i in ckrs:
            for j in ckrs:
                if i - j < self.horizon and j.value < i.value:
                    i.bestvisible = j

    def solve(self):


        #zaloz gui na wartosc liczbowa
        stepnumber = self.stepnumber
        #zaloz gui na wartosc 1,2
        random_type = self.random_type
        #zaloz gui na reshufflowanie
        bonanza_flag = self.bonanza_flag
        nochange = 0
        ckrs = self.genrandomdata()
        best = self.globalfitness(ckrs)
        rememberbest = ckrs[0]
        forchoice = range(self.crnum)

        for iteration in xrange(1,self.iternum+1):
            if(self.event.is_set()):
                break
            nochange = nochange+1
            initeration = 0
            self.updatebestvisible(ckrs)
            for instance in ckrs:
                initeration = initeration+1
                #movement towards stronger
                # for x in range(1, stepnumber):
                #     instance.step(best);
                #     instance.updatevalue(self.testcase)
                stepController = NSteps(stepnumber);
                instance.step(best,stepController);
                instance.computevalue(self.testcase)

                if instance.value < best.value:
                    best = copy.deepcopy(instance)
                    if best.value  < rememberbest.value:
                        rememberbest = best

                    print "ding!"
                    nochange = 0


                #random movement
                if random_type == 1:
                    for x in range(1, stepnumber):

                        instance.randomstep()
                        instance.updatevalue(self.testcase)

                if random_type == 2:
                    if initeration == 10:
                        instance.fullrandom()
                        instance.computevalue(self.testcase)
                        initeration = 0


                if instance.value < best.value:
                    best = copy.deepcopy(instance)
                    if best.value  < rememberbest.value:
                        rememberbest = best
                    print "dong!"
                    nochange = 0

            #be ruthless
            if iteration % 15==0:
                ckrs[random.choice(forchoice)] = copy.deepcopy(best)

            #shuffle bonanza!
            if bonanza_flag == 1:
                if nochange == self.iternum/4:
                    print "bonanza!"
                    nochange = 0
                    best = ckrs[0]
                    for instance in ckrs:
                        instance.fullrandom()
                        instance.computevalue(self.testcase)

            #if iteration == 1 or iteration % 10==0:
            #narazie komentuje zeby bylo co iteracje
            print "iter ",iteration," bestval: ",rememberbest.value
            self.app.updateInfo(rememberbest.value)
            if(iteration % 5==0):
               random.shuffle(ckrs)

        return best

