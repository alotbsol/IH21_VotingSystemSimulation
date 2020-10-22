# imports
from math import ceil

class Candidate():
    def __init__(self, voters, max_utility, average_utility, hist_bins=10):
        self.voters = voters
        self.max_utility = max_utility
        self.average_utility = average_utility
        self.hist_bins = hist_bins

        self.utility = []
        self.hist = []
        self.current_average_utility = float(self.average_utility)

        self.flat_distribution()
        self.create_hist()
        print("done")

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

    # change utility distribution of a candidate
    def change_ut(self, position, change):
        self.utility[position] += change
        self.check_minmax_ut()
        self.update_average_ut()

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
        self.current_average_utility = sum(self.utility)/self.voters

    def print_info(self):
        print("utility list:")
        print(self.utility)
        print("histogram:")
        print(self.hist)
        print("current average utility:")
        print(self.current_average_utility)


class Candidates_store():
    def __init__(self, number_of_candidates, number_of_voters, max_utility, average_utility):
        self.can_dict = {}
        self.candidates = number_of_candidates
        self.voters = number_of_voters
        self.max_utility = max_utility
        self.average_utility = average_utility

    def create(self):
        for i in range(1, self.candidates + 1):
            self.can_dict[str(i)] = Candidate

    def add_one(self):
        pass




