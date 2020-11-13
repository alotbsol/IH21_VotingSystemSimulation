# imports
import xlsxwriter
from datetime import datetime
import pandas as pd

import fun


class Storage:
    def __init__(self, methods_list, name="Project"):
        self.name = name
        self.start_time = datetime.now()
        self.methods_list = methods_list

        self.data_rounds = {}

        self.statistics = {"Iterations": [],
                           "Candidates": [],
                           "Voters": [],
                           "PDF": [],
                           "PDF_type": [],
                           "Method": [],
                           "Condorcet": [],
                           "Condorcet loser": [],
                           "Max Utility": [],
                           "Min Utility": [],
                           "Condorcet_proportion": [],
                           "Condorcet_within_list": [],
                           "Multiple winners": [],
                           }

    def set_data_rounds(self):
        self.data_rounds = {}
        self.data_rounds["Candidates"] = []
        self.data_rounds["Voters"] = []
        self.data_rounds["PDF"] = []

        for i in self.methods_list:
            self.data_rounds[i] = []

    def create_process(self, process_no=1):
        self.data_rounds[process_no] = {}

        self.data_rounds[process_no]["Candidates"] = []
        self.data_rounds[process_no]["Voters"] = []
        self.data_rounds[process_no]["PDF"] = []

        for i in self.methods_list:
            self.data_rounds[process_no][i] = []

    def one_round_process(self, data_in, process_no=1):
        for i in data_in:
            self.data_rounds[process_no][i].append(data_in[i])

    def merge_processes(self):
        copy_dict = self.data_rounds.copy()
        self.set_data_rounds()

        for i in copy_dict:
            for ii in copy_dict[i]:
                for iii in copy_dict[i][ii]:
                    self.data_rounds[ii].append(iii)

    def aggregate_results(self, specific_pdf_type="na", max_candidates=11):
        for i in self.methods_list:
            self.statistics["Iterations"].append(len(self.data_rounds["Candidates"]))
            self.statistics["Candidates"].append(self.data_rounds["Candidates"][0])
            self.statistics["Voters"].append(self.data_rounds["Voters"][0])
            self.statistics["PDF"].append(self.data_rounds["PDF"][0])
            self.statistics["PDF_type"].append(specific_pdf_type)
            self.statistics["Method"].append(i)

            self.statistics["Condorcet"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                      comparing_to=self.data_rounds["Condorcet"]))
            self.statistics["Condorcet loser"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                            comparing_to=self.data_rounds["Condorcet_loser"]))

            self.statistics["Max Utility"].append(fun.compare(comparing=self.data_rounds[i],
                                                              comparing_to=self.data_rounds["Max Utility"]))

            self.statistics["Min Utility"].append(fun.compare(comparing=self.data_rounds[i],
                                                              comparing_to=self.data_rounds["Min Utility"]))

            self.statistics["Condorcet_proportion"].append(fun.condorcet_compare_proportion(comparing=self.data_rounds[i],
                                                                                            comparing_to=self.data_rounds["Condorcet"]))

            self.statistics["Condorcet_within_list"].append(fun.condorcet_compare_within_list(comparing=self.data_rounds[i],
                                                                                              comparing_to=self.data_rounds["Condorcet"]))

            self.statistics["Multiple winners"].append(fun.multiple_winners(input_list=self.data_rounds[i]))

            for ii in range(0, max_candidates + 1):
                self.statistics.setdefault("C{0}chosen".format(ii), []).append(fun.how_often_chosen(
                    input_list=self.data_rounds[i], unique_value=ii))

        self.data_rounds = {}
        self.set_data_rounds()

    def export(self, start, end):
        writer = pd.ExcelWriter("{0}.xlsx".format(self.name), engine="xlsxwriter")
        df_all = pd.DataFrame.from_dict(self.statistics)
        df_all.to_excel(writer, sheet_name="AllData")

        info_log = pd.DataFrame({'Info:': 'This simulation was created using code available at: '
                                          'https://github.com/alotbsol/IH21_VotingSystemSimulation.',

                                "Start time:": start,
                                "End time:": end,
                                 }, index=[0]).transpose()

        info_log.to_excel(writer, sheet_name="Info_log")

        writer.save()





