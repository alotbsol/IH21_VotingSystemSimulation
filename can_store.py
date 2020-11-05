import methods
from can import Candidate

class CandidatesStore:
    def __init__(self, number_of_candidates, number_of_voters, max_utility, average_utility=0.5,
                 distribution="R", alpha=0, beta=0):

        self.can_dict = {}
        self.number_of_candidates = number_of_candidates
        self.number_of_voters = number_of_voters
        self.max_utility = max_utility
        self.average_utility = average_utility

        self.distribution = distribution
        self.alpha = alpha
        self.beta = beta

        self.voters = {"Utility": {}, "Ranking": {}}
        self.candidates = {"Utility": {}, "Ranking": {}}

        self.temp_results = {}

        self.create()

    def create(self):
        for i in range(1, self.number_of_candidates + 1):
            self.can_dict[str(i)] = Candidate(voters=self.number_of_voters,
                                              max_utility=self.max_utility,
                                              average_utility=self.average_utility,
                                              name=str(i),
                                              distribution=self.distribution)
        self.voters_preferences()

    def add_one(self):
        self.can_dict[str(self.number_of_candidates + 1)] = Candidate(voters=self.number_of_voters,
                                                                      max_utility=self.max_utility,
                                                                      average_utility=self.average_utility,
                                                                      name=str(self.number_of_candidates + 1),
                                                                      distribution=self.distribution)
        self.number_of_candidates += 1
        self.voters_preferences()

    def voters_preferences(self):
        for i in range(1, self.number_of_voters + 1):
            self.voters["Utility"][i] = []
            self.voters["Ranking"][i] = []

            for ii in self.can_dict:
                self.voters["Utility"][i].append(self.can_dict[ii].utility[i - 1])

            rankings = sorted(range(len(self.voters["Utility"][i])), key=lambda k: self.voters["Utility"][i][k])
            rankings.reverse()
            rankings = [x + 1 for x in rankings]
            for ii in rankings:
                self.voters["Ranking"][i].append(ii)

        for i in range(1, self.number_of_candidates + 1):
            self.candidates["Ranking"][i] = []
            for ii in range(self.number_of_candidates):
                self.candidates["Ranking"][i].append(0)

            for ii in range(1, self.number_of_voters + 1):
                index_of_candidate = self.voters["Ranking"][ii].index(i)
                self.candidates["Ranking"][i][index_of_candidate] += 1

            self.candidates["Utility"][i] = []
            for ii in self.can_dict[str(i)].utility:
                self.candidates["Utility"][i].append(ii)


    def print_info(self):
        print(self.can_dict)
        print(self.voters)
        print(self.candidates)

    def results_one_round(self):
        self.temp_results = {}
        self.temp_results["1Vote"] = methods.x_votes(input_rankings=self.candidates["Ranking"], number_of_votes=1)
        self.temp_results["2Vote"] = methods.x_votes(input_rankings=self.candidates["Ranking"], number_of_votes=2)
        self.temp_results["3Vote"] = methods.x_votes(input_rankings=self.candidates["Ranking"], number_of_votes=3)
        self.temp_results["Max_U"] = methods.max_utility(input_utility=self.candidates["Utility"])
        self.temp_results["Min_U"] = methods.min_utility(input_utility=self.candidates["Utility"])
        self.temp_results["Condorcet"] = methods.condorcet_calculation(input_utility=self.voters["Utility"],
                                                                       number_of_candidates=self.number_of_candidates,
                                                                       number_of_voters=self.number_of_voters)


