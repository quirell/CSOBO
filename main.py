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

matplotlib.use("TkAgg")


class App(Tk):

    def __init__(self, test_list):
        Tk.__init__(self)

        self.event = threading.Event()
        self.geometry("1000x750+0+0")
        self.title("Cockroach genetic algorithm")

        self.box = LabelFrame(self, borderwidth=0)
        self.box.grid(row=0, column=1)

        self.input_box = LabelFrame(self, borderwidth=0)
        self.input_box.grid(row=0, column=0)

        self.numberOfCockroaches = Entry(self.input_box, bg="white")
        self.numberOfCockroaches.grid(row=0, column=2)
        self.cockroachesLabel = Label(self.input_box, text="Cockroaches number")
        self.cockroachesLabel.grid(row=0, column=1)
        self.horizon = Entry(self.input_box, bg="white")
        self.horizon.grid(row=1, column=2)
        self.horizonLabel = Label(self.input_box, text="Horizon size")
        self.horizonLabel.grid(row=1, column=1)

        self.numberOfIterations = Entry(self.input_box)
        self.numberOfIterations.grid(row=2, column=2)
        self.iterationsLabel = Label(self.input_box, text="Number of iterations")
        self.iterationsLabel.grid(row=2, column=1)

        self.testLabel = Label(self.input_box, text="Test")
        self.testLabel.grid(row=3, column=1)

        self.box_value_test = StringVar()
        self.combo_box_test = ttk.Combobox(self.input_box, textvariable=self.box_value_test, height=5)
        self.combo_box_test['values'] = test_list
        self.combo_box_test.current(0)
        self.combo_box_test.grid(column=2, row=3)

        self.value1_label = Label(self.input_box, text="Random type")
        self.value1_label.grid(row=4, column=1)

        self.value2_label = Label(self.input_box, text="Step number")
        self.value2_label.grid(row=5, column=1)

        self.numberStepNumber = Entry(self.input_box)
        self.numberStepNumber.grid(row=5, column=2)

        self.var = IntVar()
        self.reshuffle_cbox = Checkbutton(self.input_box, text="Reshuffle", variable=self.var)
        self.reshuffle_cbox.grid(row=6, column=1)

        self.onButton = Button(self.input_box, command=self.startAction, text="Start")
        self.onButton.grid(row=7, column=1)
        self.offButton = Button(self.input_box, text="Stop", command=self.stopAction)
        self.offButton.grid(row=7, column=2)

        self.box_value_value1 = StringVar()
        self.combo_box_value1 = ttk.Combobox(self.input_box, textvariable=self.box_value_value1, height=5)
        self.combo_box_value1['values'] = [1,2]
        self.combo_box_value1.current(0)
        self.combo_box_value1.grid(column=2, row=4)


        self.figure = Figure(figsize=(8,7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.box)
        self.canvas.get_tk_widget().grid(row=0)
        self.canvas.show()

        self.iteration = 0
        self.iterationList = []
        self.valueList = []

    def startAction(self):
        self.event.clear()
        self.iteration = 0
        self.iterationList = []
        self.valueList = []
        try:
            cockroachNumber = int(self.numberOfCockroaches.get())
            horizon = int(self.horizon.get())
            iterations = int(self.numberOfIterations.get())
            stepNumber = int(self.numberStepNumber.get())
            randomType = int(self.box_value_value1.get())
            test_number = self.combo_box_test.current()
            reshuffle = self.var.get()
            self.t1 = threading.Thread(target=otherFunc, args=(self, test_number, cockroachNumber,
                horizon, iterations, stepNumber, randomType, reshuffle, self.event))
            self.t1.start()
            print cockroachNumber, horizon, iterations, stepNumber, randomType, test_number, reshuffle
        except ValueError:
            print "Cockroaches number and horizon should be numbers"

    def stopAction(self):
        print "Stopped"
        self.event.set()

    def updateInfo(self, value):
        self.iteration += 1
        self.iterationList.append(self.iteration)
        self.valueList.append(value)
        self.figure.clear()
        self.a = self.figure.add_subplot(111)
        self.a.set_xlabel('Number of iterations divided by 10')
        self.a.set_ylabel('Best value')
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
    app = App(tests)
    app.mainloop()

