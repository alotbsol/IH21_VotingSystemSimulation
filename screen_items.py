from tkinter import *
import matplotlib.pyplot as plt


class General_Button(object):
    def __init__(self, framevar, inputrow, inputcolumn, inputtext, function):
        Button_general = Button(framevar, text=inputtext, command=function)
        Button_general.grid(row=inputrow, column=inputcolumn, sticky=W)


class EnterField(object):
    def __init__(self, framevar, inputrow, inputcolumn, inputtext, basicvalue, type):
        self.framevar = framevar
        self.inputrow = inputrow
        self.inputcolumn = inputcolumn
        self.inputtext = inputtext
        self.var = 0 + basicvalue

        #tzpe 1 is for float
        self.type = type

        self.CreateInputField()
        self.ShowIt()

    def CreateInputField(self):
        self.InputField = Entry(self.framevar)
        self.InputField.bind("<Return>", self.StoreNumber)
        self.InputFieldLabel = Label(self.framevar, text=self.inputtext + ": " + str(self.var))

    def ShowIt(self):
        self.InputField.grid(row=self.inputrow, column=self.inputcolumn, sticky=W)
        self.InputFieldLabel.grid(row=self.inputrow - 1, column=self.inputcolumn, sticky=W)

    def StoreNumber(self, arg):
        if self.type == 1:
            self.var = float(self.InputField.get())
        else:
            self.var = int(self.InputField.get())

        InputFieldLabel = Label(self.framevar, text=self.inputtext + ": " + str(self.var))
        InputFieldLabel.grid(row=self.inputrow - 1, column=self.inputcolumn, sticky=W)

