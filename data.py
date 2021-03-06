__author__ = 'quirell'


import os
import re

class TestCase:
    """
    fullname - nazwa przypadku testowego
    testname - nazwa grupy do ktorej przypadek testowy nalezy, wiecej tu: http://anjos.mgi.polymtl.ca/qaplib/inst.html
    value - najlepsza (minimalna) wartosc rozwiazania
    solution - permutacja dla ktorej rozwiazanie przyjmuje najmniejsza wartosc
    distance, flow - wiadomo
    """
    datapath = ""
    solutionspath = ""
    def __init__(self,name):
        self.fullname = name
        self.testname = re.match(r"([a-zA-Z]+).*",name).group(1)
        self.value = self.flow = self.distance = self.solution = None
        self.size = 0

    def load(self):
        with open(TestCase.datapath + "/" + self.fullname + ".dat") as f:
            self.size = int(f.readline())
            line = "\n"
            while line == "\n":
                line = f.readline()
            flow = []
            for _ in xrange(self.size):
                flow.append([int(i) for i in line.split()])
                while len(flow[-1]) != self.size:
                    line = f.readline()
                    flow[-1].extend([int(i) for i in line.split()])
                line = f.readline()
            # line = "\n"
            while line == "\n":
                line = f.readline()
            distance = []
            for _ in xrange(self.size):
                distance.append([int(i) for i in line.split()])
                while len(distance[-1]) != self.size:
                    line = f.readline()
                    distance[-1].extend([int(i) for i in line.split()])
                line = f.readline()

        solution = None
        if os.path.isfile(TestCase.solutionspath + "/" + self.fullname + ".sln"):
            with open(TestCase.solutionspath + "/" + self.fullname + ".sln") as f:
                line = f.readline()
                _, self.value = line.split()
                self.value = int(self.value)
                solution = []
                for line in f:

                    if "," in line:
                        solution.extend([int(i.strip()) for i in line.split(",") if i.strip().isdigit()])
                    else:
                        solution.extend([int(i.strip()) for i in line.split()])
        self.flow = flow
        self.distance = distance
        if solution:
            self.solution = [i-1 for i in solution]

    def solutionavailable(self):
        return self.solution is not None

    def __str__(self):
        return self.fullname + " size: "+self.size+" value: "+self.value




class Data:
    def __init__(self):
        self.datapath = "data"
        self.solutionspath = "solutions"
        TestCase.datapath = self.datapath
        TestCase.solutionspath = self.solutionspath

    def gettestcases(self):
        testcases = []
        for filename in os.listdir(self.datapath):
            testcases.append(TestCase(filename[:-4]))
        return testcases




