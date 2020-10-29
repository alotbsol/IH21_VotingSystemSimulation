# imports
from math import ceil
from random import random
import methods


class Candidate:
    def __init__(self, voters, max_utility, average_utility, name, hist_bins=10, distribution="random"):
        self.voters = voters
        self.max_utility = max_utility
        self.average_utility = average_utility
        self.name = name
        self.hist_bins = hist_bins

        self.utility = []
        self.hist = []
        self.current_average_utility = float(self.average_utility)

        if distribution == "random":
            self.random_distribution()
        elif distribution == "flat":
            self.flat_distribution()
        else:
            self.beta_distribution()

        self.create_hist()

    # create flat utility distribution for all voters
    def flat_distribution(self):
        for i in range(0, self.voters):
            self.utility.append(self.average_utility)

    # create random utility distribution for all voters
    def random_distribution(self):
        for i in range(0, self.voters):
            self.utility.append(random())

    def beta_distribution(self):
        pass

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


class CandidatesStore:
    def __init__(self, number_of_candidates, number_of_voters, max_utility, average_utility):
        self.can_dict = {}
        self.number_of_candidates = number_of_candidates
        self.number_of_voters = number_of_voters
        self.max_utility = max_utility
        self.average_utility = average_utility

        self.voters = {}
        self.candidate_rankings = {}
        self.create()

    def create(self):
        for i in range(1, self.number_of_candidates + 1):
            self.can_dict[str(i)] = Candidate(voters=self.number_of_voters,
                                              max_utility=self.max_utility,
                                              average_utility=self.average_utility,
                                              name=str(i))
        self.voters_preferences()

    def add_one(self):
        print(self.number_of_candidates)
        self.can_dict[str(self.number_of_candidates + 1)] = Candidate(voters=self.number_of_voters,
                                                                      max_utility=self.max_utility,
                                                                      average_utility=self.average_utility,
                                                                      name=str(self.number_of_candidates + 1))
        self.number_of_candidates += 1
        self.voters_preferences()

    def voters_preferences(self):
        for i in range(1, self.number_of_voters + 1):
            self.voters[i] = {"Utility": [], "Ranking": []}
            for ii in self.can_dict:
                self.voters[i]["Utility"].append(self.can_dict[ii].utility[i - 1])

            rankings = sorted(range(len(self.voters[i]["Utility"])), key=lambda k: self.voters[i]["Utility"][k])
            rankings.reverse()
            rankings = [x + 1 for x in rankings]
            for ii in rankings:
                self.voters[i]["Ranking"].append(ii)

        for i in range(1, self.number_of_candidates + 1):
            self.candidate_rankings[i] = []
            for ii in range(self.number_of_candidates):
                self.candidate_rankings[i].append(0)

            for ii in range(1, self.number_of_voters + 1):
                index_of_candidate = self.voters[ii]["Ranking"].index(i)
                self.candidate_rankings[i][index_of_candidate] += 1


    def print_info(self):
        print(self.can_dict)
        print(self.voters)
        print(self.candidate_rankings)

    def results_one_round(self):
        methods.x_votes(input_rankings=self.candidate_rankings, number_of_votes=1)
        methods.x_votes(input_rankings=self.candidate_rankings, number_of_votes=2)
        methods.x_votes(input_rankings=self.candidate_rankings, number_of_votes=3)
