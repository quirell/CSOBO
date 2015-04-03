__author__ = 'quirell'


import os

class TestCase:
    datapath = ""
    solutionspath = ""
    def __init__(self,name):
        self.name = name
        self.value = self.flow = self.distance = self.solution = None

    def load(self):
        with open(TestCase.datapath + "/" + self.name + ".dat") as f:
            self.size = int(f.readline())
            line = "\n"
            while line == "\n":
                line = f.readline()
            flow = []
            for _ in xrange(self.size):
                flow.append([int(i) for i in line.split() ])
                line = f.readline()
            line = "\n"
            while line == "\n":
                line = f.readline()
            distance = []
            for _ in xrange(self.size):
                distance.append(line.split())
                line = f.readline()

        solution = None
        if os.path.isfile(TestCase.solutionspath + "/" + self.name + ".sln"):
            with open(TestCase.solutionspath + "/" + self.name + ".sln") as f:
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
        self.solution = solution

    def solutionavailable(self):
        return self.solution is not None

    def __str__(self):
        return self.name + " size: "+self.size+" value: "+self.value




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




