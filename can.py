# imports
from math import ceil
from random import random
import numpy as np


class Candidate:
    def __init__(self, voters, max_utility, average_utility, name, hist_bins=10, distribution="R", alpha=1, beta=1):
        self.voters = voters
        self.max_utility = max_utility
        self.average_utility = average_utility
        self.name = name
        self.hist_bins = hist_bins
        self.distribution = distribution
        self.alpha = alpha
        self.beta = beta

        self.utility = []
        self.hist = []
        self.current_average_utility = float(self.average_utility)

        if distribution == "R":
            self.random_distribution()
        elif distribution == "B":
            self.beta_distribution()
        elif distribution == "flat":
            self.flat_distribution()
        else:
            pass

        self.create_hist()

    # create flat utility distribution for all voters
    def flat_distribution(self):
        self.utility = []
        for i in range(0, self.voters):
            self.utility.append(self.average_utility)

    # create random utility distribution for all voters
    def random_distribution(self):
        self.utility = []
        for i in range(0, self.voters):
            self.utility.append(random())

    def beta_distribution(self,):
        self.utility = []
        x = np.random.beta(self.alpha, self.beta, int(self.voters))
        for i in list(x):
            self.utility.append(i)

    # creates histogram from utility distribution
    def create_hist(self):
        one_step = self.max_utility / self.hist_bins
        limits = []
        self.hist = [0] * self.hist_bins

        previous_value = 0
        for i in range(0, self.hist_bins):
            limits.append(round(one_step + previous_value, 3))
            previous_value += one_step

        for i in self.utility:
            x = ceil(i * 10) / 10
            index_hist = limits.index(x)

            self.hist[index_hist] += 1

    # change utility distribution of a candidate
    def change_ut(self, position, change):
        self.utility[position - 1] += change
        self.check_minmax_ut()
        self.update_average_ut()
        self.create_hist()

    # check and adjust utility so it stays between 0 and 1
    def check_minmax_ut(self):
        x = 0
        for i in self.utility:
            if i > self.max_utility:
                self.utility[x] = self.max_utility

            elif i < 0:
                self.utility[x] = 0

            else:
                pass

            x += 1

    # calculates the average utility
    def update_average_ut(self):
        self.current_average_utility = sum(self.utility) / self.voters

    # here should be linspaced? beta....

    def print_info(self):
        print("Candidate" + str(self.name))
        print("utility list:")
        print(self.utility)
        print("histogram:")
        print(self.hist)
        print("current average utility:")
        print(self.current_average_utility)
        print("")



