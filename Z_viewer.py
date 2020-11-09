#Imports
from tkinter import *

from Z_screen_items import General_Button
from Z_screen_items import EnterField

from storage import Storage
from can_store import CandidatesStore


Master_dict = {"can_store": "", "storage": "",}

""" USED METHODS DEFINITION"""
methods_list = ["Plurality", "Run off", "Borda",
                "Maj judge 3", "Maj judge 5", "Maj judge 10",
                "Range 3", "Range 5", "Range 10",
                "Max_U", "Min_U", "Condorcet", "Condorcet_loser"]

for i in range(1, 4):
    methods_list.append("{0}Vote_Fix".format(i))

for i in range(1, 4):
    methods_list.append("{0}Vote_Var".format(i))

for i in range(1, 4):
    methods_list.append("{0}Vote_Var-".format(i))

""" END USED METHODS DEFINITION"""

Master_dict["storage"] = Storage(methods_list=methods_list)


def generate_environment(number_of_candidates, number_of_voters):
    Master_dict["can_store"] = CandidatesStore(number_of_candidates=number_of_candidates,
                                               number_of_voters=number_of_voters, max_utility=1,
                                               average_utility=0.5, distribution="B", alpha=1, beta=1)
    Master_dict["can_store"].print_info()

def add_one():
    Master_dict["can_store"].add_one()
    Master_dict["can_store"].print_info()


def do_results():
    Master_dict["can_store"].print_info()
    Master_dict["can_store"].results_one_round()

    Master_dict["storage"].one_round(data_in=Master_dict["can_store"].temp_results)


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