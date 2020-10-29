#Imports
from tkinter import *

from screen_items import General_Button
from screen_items import EnterField

from can import CandidatesStore

Master_List = ["",]


def generate_environment(number_of_candidates, number_of_voters):
    Master_List[0] = CandidatesStore(number_of_candidates=number_of_candidates, number_of_voters=number_of_voters,
                                 max_utility=1, average_utility=0.5)
    Master_List[0].print_info()


def add_one():
    Master_List[0].add_one()
    Master_List[0].print_info()


def do_results():
    Master_List[0].print_info()
    Master_List[0].results_one_round()




def create_buttons():
    BE1 = EnterField(framevar=root, inputrow=1, inputcolumn=1, inputtext="Number of candidates", basicvalue=3, type=0)
    BE2 = EnterField(framevar=root, inputrow=1, inputcolumn=2, inputtext="Number of voters", basicvalue=10, type=0)

    B1 = General_Button(framevar=root, inputrow=3, inputcolumn=1, inputtext="Generate environment",
                        function=lambda: generate_environment(number_of_candidates=BE1.var, number_of_voters=BE2.var))

    B2 = General_Button(framevar=root, inputrow=4, inputcolumn=1, inputtext="add one candidate",
                        function=lambda: add_one())

    B3 = General_Button(framevar=root, inputrow=5, inputcolumn=1, inputtext="results",
                        function=lambda: do_results())



if __name__ == '__main__':
    root = Tk()
    root.geometry("800x600")

    create_buttons()



    root.mainloop()