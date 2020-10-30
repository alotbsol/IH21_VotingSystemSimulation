import xlsxwriter
from datetime import datetime
import pandas as pd


class Storage:
    def __init__(self, name="Project"):
        self.name = name
        self.start_time = datetime.now()

        self.winners_rounds = {}
        self.statistics = {}

    def one_round(self, data_in):
        pass

    def aggregate_results(self):
        pass

    def export(self):
        writer = pd.ExcelWriter("{0}.xlsx".format(self.name), engine="xlsxwriter")





