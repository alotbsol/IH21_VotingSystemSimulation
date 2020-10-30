import xlsxwriter
from datetime import datetime
import pandas as pd


class Storage:
    def __init__(self, methods_list, name="Project"):
        self.name = name
        self.start_time = datetime.now()

        self.winners_rounds = {}
        for i in methods_list:
            self.winners_rounds[i] = []

        self.statistics = {}

    def one_round(self, data_in):
        for i in data_in:
            self.winners_rounds[i].append(data_in[i])

        print("showing data")
        print(self.winners_rounds)

    def aggregate_results(self):
        pass

    def export(self):
        writer = pd.ExcelWriter("{0}.xlsx".format(self.name), engine="xlsxwriter")





