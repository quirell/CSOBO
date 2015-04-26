import threading
from Tkinter import *
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
from time import sleep
import random
matplotlib.use("TkAgg")


class App(Tk):

    def __init__(self, test_list, value1_list, value2_list):
        Tk.__init__(self)
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

        self.value1_label = Label(self.input_box, text="Value1")
        self.value1_label.grid(row=4, column=1)

        self.value2_label = Label(self.input_box, text="Value2")
        self.value2_label.grid(row=5, column=1)

        self.onButton = Button(self.input_box, command=self.startAction, text="Start")
        self.onButton.grid(row=6, column=1)
        self.offButton = Button(self.input_box, text="Stop", command=self.stopAction)
        self.offButton.grid(row=6, column=2)

        self.box_value_value1 = StringVar()
        self.combo_box_value1 = ttk.Combobox(self.input_box, textvariable=self.box_value_value1, height=5)
        self.combo_box_value1['values'] = value1_list
        self.combo_box_value1.current(0)
        self.combo_box_value1.grid(column=2, row=4)

        self.box_value_value2 = StringVar()
        self.combo_box_value2 = ttk.Combobox(self.input_box, textvariable=self.box_value_value2, height=5)
        self.combo_box_value2['values'] = value2_list
        self.combo_box_value2.current(0)
        self.combo_box_value2.grid(column=2, row=5)

        self.figure = Figure(figsize=(7,7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.box)
        self.canvas.get_tk_widget().grid(row=0)
        self.canvas.show()

        self.iteration = 0
        self.iterationList = [0]
        self.valueList = [0]

    def startAction(self):
        try:
            cockroachNumber = int(self.numberOfCockroaches.get())
            horizon = int(self.horizon.get())
            iterations = int(self.numberOfIterations.get())
            test = self.box_value_test.get()
            test1 = self.box_value_value1.get()
            test2 = self.box_value_value2.get()
            self.t1_stop = threading.Event()
            self.t1 = threading.Thread(target=otherFunc, args=(self, self.t1_stop))
            self.t1.start()
            print cockroachNumber, horizon, iterations, test, test1, test2
        except ValueError:
            print "Cockroaches number and horizon should be numbers"

    def stopAction(self):
        self.t1_stop.set()
        self.figure.clear()
        self.iteration = 0
        self.iterationList = [0]
        self.valueList = [0]

    def updateInfo(self, value):
        self.iteration += 1
        self.iterationList.append(self.iteration)
        self.valueList.append(value)
        self.figure.clear()
        self.a = self.figure.add_subplot(111)
        self.a.plot(self.iterationList, self.valueList)
        self.canvas.show();



def otherFunc(app, stop):
    while (not stop.is_set()):
        app.updateInfo(random.randint(0,100))
        sleep(2)



if __name__ == '__main__':
    tests = ('a1', 'b2', 'c3', 'd4', 'e5', 'f6', 'g7')
    app = App(tests, tests, tests)
    app.mainloop()
