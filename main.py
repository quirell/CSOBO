import threading
from Tkinter import *
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
from time import sleep
import random
import data
import cso
import csv
from matplotlib import rcParams
import time


rcParams.update({'figure.autolayout': True})
matplotlib.use("TkAgg")


class App(Tk):

    def __init__(self, test_list, testcases):
        Tk.__init__(self)
        
        self.savedImages = 1
        self.testcases = testcases

        self.event = threading.Event()
        self.geometry("1200x750+0+0")
        self.title("Cockroach genetic algorithm")

        self.box = LabelFrame(self, borderwidth=0)
        self.box.grid(row=0, column=1)

        self.input_box = LabelFrame(self, borderwidth=0)
        self.input_box.grid(row=0, column=0)

        self.time = Label(self.input_box, text="Execution time")
        self.time.grid(row=0, column=1)
        
        self.time_value = Label(self.input_box)
        self.time_value.grid(row=0, column=2)
        
        self.best_result_from_file_label = Label(self.input_box, text="Best result")
        self.best_result_from_file_label.grid(row=1, column=1)
        
        self.best_result_from_file_value = Label(self.input_box)
        self.best_result_from_file_value.grid(row=1, column=2)
        
        self.best_result_label = Label(self.input_box, text="Algorithm best result")
        self.best_result_label.grid(row=2, column=1)
        
        self.best_result_value = Label(self.input_box)
        self.best_result_value.grid(row=2, column=2)
        
        self.best_iteration_label = Label(self.input_box, text="Iteration of best result")
        self.best_iteration_label.grid(row=3, column=1)
        
        self.best_iteration_value = Label(self.input_box)
        self.best_iteration_value.grid(row=3, column=2)
           
        self.numberOfCockroaches = Entry(self.input_box, bg="white")
        self.numberOfCockroaches.grid(row=4, column=2)
        self.cockroachesLabel = Label(self.input_box, text="Number of cockroaches")
        self.cockroachesLabel.grid(row=4, column=1)
        self.horizon = Entry(self.input_box, bg="white")
        self.horizon.grid(row=5, column=2)
        self.horizonLabel = Label(self.input_box, text="Horizon")
        self.horizonLabel.grid(row=5, column=1)

        self.numberOfIterations = Entry(self.input_box)
        self.numberOfIterations.grid(row=6, column=2)
        self.iterationsLabel = Label(self.input_box, text="Number of iterations")
        self.iterationsLabel.grid(row=6, column=1)

        self.testLabel = Label(self.input_box, text="Test")
        self.testLabel.grid(row=7, column=1)

        self.box_value_test = StringVar()
        self.combo_box_test = ttk.Combobox(self.input_box, textvariable=self.box_value_test, height=5)
        self.combo_box_test['values'] = test_list
        self.combo_box_test.current(0)
        self.combo_box_test.grid(column=2, row=8)

        self.value1_label = Label(self.input_box, text="Random type")
        self.value1_label.grid(row=8, column=1)

        self.value2_label = Label(self.input_box, text="Step length")
        self.value2_label.grid(row=9, column=1)

        self.numberStepNumber = Entry(self.input_box)
        self.numberStepNumber.grid(row=9, column=2)

        self.var = IntVar()
        self.reshuffle_cbox = Checkbutton(self.input_box, text="Reshuffle", variable=self.var)
        self.reshuffle_cbox.grid(row=10, column=1)

        self.onButton = Button(self.input_box, command=self.startAction, text="Start")
        self.onButton.grid(row=11, column=1)
        self.offButton = Button(self.input_box, text="Stop", command=self.stopAction)
        self.offButton.grid(row=11, column=2)
        
        self.saveButton = Button(self.input_box, text="Save to file", command=self.saveAction)
        self.saveButton.grid(row=13, column=1)

        self.box_value_value1 = StringVar()
        self.combo_box_value1 = ttk.Combobox(self.input_box, textvariable=self.box_value_value1, height=5)
        self.combo_box_value1['values'] = ['Random direction', 'Total reshuffle']
        self.combo_box_value1.current(0)
        self.combo_box_value1.grid(column=2, row=7)


        self.figure = Figure(figsize=(8,7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.box)
        self.canvas.get_tk_widget().grid(row=0)
        self.canvas.show()

        self.iteration = 0
        self.iterationList = []
        self.valueList = []

    def startAction(self):
        self.current = time.clock()
        self.time_value.config(text="")
        self.best = 0
        self.event.clear()
        self.iteration = 0
        self.iterationList = []
        self.valueList = []
        try:
            cockroachNumber = int(self.numberOfCockroaches.get())
            horizon = int(self.horizon.get())
            self.iterations = int(self.numberOfIterations.get())
            stepNumber = int(self.numberStepNumber.get())
            randomType = self.combo_box_value1.current()
            test_number = self.combo_box_test.current()
            reshuffle = self.var.get()
            self.testcases[test_number].load()
            self.best_result_from_file_value.config(text=self.testcases[test_number].value)
            self.t1 = threading.Thread(target=otherFunc, args=(self, test_number, cockroachNumber,
                horizon, self.iterations, stepNumber, randomType + 1, reshuffle, self.event))
            self.t1.start()
        except ValueError:
            print "Cockroaches number and horizon should be numbers"

    def stopAction(self):
        print "Stopped"
        self.current = time.clock() - self.current
        self.time_value.config(text="{:.3f}".format(self.current))
        self.event.set()
        
    def saveAction(self):
        self.figure.savefig(str(self.savedImages) + ".jpg")
        myfile = open(str(self.savedImages) + ".csv", 'wb')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(self.valueList)
        myfile.close()
        print "Saved as " + str(self.savedImages) + ".jpg " + str(self.savedImages) + ".csv" 
        self.savedImages += 1

    def updateInfo(self, value):
        self.iteration += 1
        if self.iteration == 1:
            self.best = value
            self.best_iteration = self.iteration
        if self.iterations == self.iteration:
            self.current = time.clock() - self.current
            self.time_value.config(text="{:.3f}".format(self.current))
        if value < self.best:
            self.best = value
            self.best_iteration = self.iteration
            self.best_result_value.config(text=value)
            self.best_iteration_value.config(text=self.best_iteration)
        self.iterationList.append(self.iteration)
        self.valueList.append(value)
        self.figure.clear()
        self.a = self.figure.add_subplot(111)
        self.a.set_xlabel('Number of iterations')
        self.a.set_ylabel('Best value')
        self.a.margins(tight=True)
        self.a.plot(self.iterationList, self.valueList)
        self.canvas.show();



def otherFunc(app, test_number, cockroaches, horizon, iterations, sN, rT, r, event):
    d = data.Data()
    c = d.gettestcases()
    c[test_number].load()
    solver = cso.CSOSolver(c[test_number], cockroaches, horizon, sN, rT, r, iterations, app, event)
    app.solver = solver
    solver.solve()


if __name__ == '__main__':
    d = data.Data()
    c = d.gettestcases()
    tests = []
    for x in c:
        tests.append(x.fullname)
    app = App(tests, c)
    app.mainloop()

