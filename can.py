# imports
from math import ceil

class Candidate:
    def __init__(self, voters, max_utility, average_utility, hist_bins=10):
        self.voters = voters
        self.max_utility = max_utility
        self.average_utility = average_utility
        self.hist_bins = hist_bins

        self.utility = []
        self.hist = []
        self.current_average_utility = float(self.average_utility)

        self.flat_distribution()

    # create flat utility distribution for all voters
    def flat_distribution(self):
        for i in range(0, self.voters):
            self.utility.append(self.average_utility)

    # creates histogram from utility distribution
    def create_hist(self):
        one_step = self.max_utility / self.hist_bins
        limits = []
        self.hist = [0] * self.voters

        previous_value = 0
        for i in range(0, self.hist_bins):
            limits.append(round(one_step + previous_value, 3))
            previous_value += one_step

        for i in self.utility:
            x = ceil(i * 10) / 10
            index_hist = limits.index(x)

            self.hist[index_hist] += 1

    def change_ut(self, position, change):
        self.utility[position] += change
        self.check_ut()

    def check_ut(self):
        x = 0
        for i in self.utility:
            if i > self.max_utility:
                self.utility[x] = self.max_utility

            elif i < 0:
                self.utility[x] = 0

            else:
                pass

            x += 1

    def update_average_ut(self):
        self.current_average_utility = sum(self.utility)/self.voters


    def print_info(self):
        print("utility list:")
        print(self.utility)
        print("histogram:")
        print(self.hist)
