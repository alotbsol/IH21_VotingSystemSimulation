import methods
from can import Candidate


class CandidatesStore:
    def __init__(self, number_of_candidates, number_of_voters, max_utility, average_utility=0.5,
                 distribution="R", alpha=1, beta=1):

        self.can_dict = {}
        self.number_of_candidates = number_of_candidates
        self.number_of_voters = number_of_voters
        self.max_utility = max_utility
        self.average_utility = average_utility

        self.distribution = distribution
        self.alpha = alpha
        self.beta = beta

        self.voters = {"Utility": {}, "Ranking": {}, "Variable_Ranking": {}}
        self.candidates = {"Utility": {}, "Ranking": {}, "Variable_Ranking": {}}

        self.temp_results = {}

        self.create()

    def create(self):
        for i in range(1, self.number_of_candidates + 1):
            self.can_dict[str(i)] = Candidate(voters=self.number_of_voters,
                                              max_utility=self.max_utility,
                                              average_utility=self.average_utility,
                                              name=str(i),
                                              distribution=self.distribution,
                                              alpha=self.alpha,
                                              beta=self.beta)
        self.voters_preferences()

    def add_one(self):
        self.can_dict[str(self.number_of_candidates + 1)] = Candidate(voters=self.number_of_voters,
                                                                      max_utility=self.max_utility,
                                                                      average_utility=self.average_utility,
                                                                      name=str(self.number_of_candidates + 1),
                                                                      distribution=self.distribution,
                                                                      alpha=self.alpha,
                                                                      beta=self.beta
                                                                      )
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

    def voters_preferences_variable(self):
        minus_votes = [0] * self.number_of_candidates
        deleted_votes = []
        more_than_1vote = 0

        for i in range(1, self.number_of_voters + 1):
            utility_copy = self.voters["Utility"][i]
            to_be_deleted = 0
            for ii in range(utility_copy):
                # THRESHOLD here average utility of specific voter
                if utility_copy[ii] > sum(utility_copy) / len(utility_copy):
                    pass
                else:
                    to_be_deleted += 1

            deleted_votes.append(to_be_deleted)

            if to_be_deleted < self.number_of_candidates - 1:
                more_than_1vote = 1
            else:
                more_than_1vote = 0

            utility_copy = sorted(range(len(utility_copy)), key=lambda k: utility_copy[k])
            utility_copy.reverse()
            utility_copy = [x + 1 for x in utility_copy]

            for ii in range(1, to_be_deleted + 1):
                utility_copy[-ii] = 0

            if more_than_1vote == 1:
                where_is_minus = int(utility_copy.index(min(utility_copy)))
                minus_votes[where_is_minus] += -1
            else:
                pass

            self.voters["Variable_Ranking"] = list(utility_copy)
            utility_copy = []

        # Results - Candidates number of x votes - above
        for i in range(1, self.number_of_candidates + 1):
            CanRankingCopy = []
            for ii in range(1, self.number_of_candidates + 1):
                votecountertwo = 0
                for iii in range(1, self.number_of_voters + 1):
                    votecounter = settings.VoterRankingStorageThresh["VoterR{0}".format(iii)][ii - 1]
                    if i == votecounter:
                        votecountertwo += 1
                CanRankingCopy.append(votecountertwo)

            settings.CandidateRankingStorageThresh["CandidateR{0}".format(i)] = list(CanRankingCopy)

            settings.CandidateRankingStorageThreshMinus["CandidateR{0}".format(i)] = list(CanRankingCopy)

        for j in range(1, 1 + settings.candidate_number):
            settings.CandidateRankingStorageThreshMinus["CandidateR{0}".format(j)][0] += MinusVotes[j - 1]


        self.candidates = {"Utility": {}, "Ranking": {}, "Variable_Ranking": {}}

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

        self.temp_results["Borda"] = methods.borda(input_rankings=self.candidates["Ranking"],
                                                   number_of_candidates=self.number_of_candidates)

        self.temp_results["Run off"] = methods.run_off(input_rankings=self.candidates["Ranking"],
                                                       input_voters_rankings=self.voters["Ranking"],
                                                       number_of_candidates=self.number_of_candidates,
                                                       number_of_voters=self.number_of_voters)

        self.temp_results["Maj judge 3"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                      scale=3,
                                                                      number_of_candidates=self.number_of_candidates)
        self.temp_results["Maj judge 5"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                      scale=5,
                                                                      number_of_candidates=self.number_of_candidates)
        self.temp_results["Maj judge 10"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                       scale=10,
                                                                       number_of_candidates=self.number_of_candidates)

        self.temp_results["Range 3"] = methods.range_voting(input_utility=self.candidates["Utility"],
                                                            scale=3,
                                                            number_of_candidates=self.number_of_candidates)
        self.temp_results["Range 5"] = methods.range_voting(input_utility=self.candidates["Utility"],
                                                            scale=5,
                                                            number_of_candidates=self.number_of_candidates)
        self.temp_results["Range 10"] = methods.range_voting(input_utility=self.candidates["Utility"],
                                                             scale=10,
                                                             number_of_candidates=self.number_of_candidates)

        self.temp_results["Condorcet"] = methods.condorcet_calculation(input_utility=self.voters["Utility"],
                                                                       number_of_candidates=self.number_of_candidates,
                                                                       number_of_voters=self.number_of_voters,
                                                                       con_winner=1, con_loser=0)

        self.temp_results["Condorcet_loser"] = methods.condorcet_calculation(input_utility=self.voters["Utility"],
                                                                             number_of_candidates=self.number_of_candidates,
                                                                             number_of_voters=self.number_of_voters,
                                                                             con_winner=0, con_loser=1)


