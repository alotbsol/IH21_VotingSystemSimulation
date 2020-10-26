#Imports
from tkinter import *

from screen_items import General_Button
from screen_items import EnterField

import can

def random_function():
    print("Random Function")

def create_buttons():
    BE1 = EnterField(framevar=root, inputrow=1, inputcolumn=1, inputtext="Number of candidates", basicvalue=0, type=1)
    BE2 = EnterField(framevar=root, inputrow=1, inputcolumn=2, inputtext="Number of voters", basicvalue=0, type=1)

    B1 = General_Button(framevar=root, inputrow=3, inputcolumn=1, inputtext="Generate environment", function=random_function)



if __name__ == '__main__':
    root = Tk()
    root.geometry("800x600")

    create_buttons()



    root.mainloop()