import methods
from can import Candidate
import random


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
        self.candidates = {"Utility": {}, "Ranking": {}, "Variable_Ranking": {}, "Variable_Ranking_Minus": {}}

        self.current_scenario = ""
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

        self.voters_preferences_variable()

    def voters_preferences_variable(self):
        minus_votes = [0] * self.number_of_candidates
        deleted_votes = []

        for i in range(1, self.number_of_voters + 1):
            utility_copy_temp = self.voters["Utility"][i]
            to_be_deleted = 0
            for ii in range(len(utility_copy_temp)):
                # THRESHOLD here average utility of specific voter
                if utility_copy_temp[ii] > sum(utility_copy_temp) / len(utility_copy_temp):
                    pass
                else:
                    to_be_deleted += 1

            deleted_votes.append(to_be_deleted)
            if 2 > self.number_of_candidates - to_be_deleted:
                pass
            else:
                where_is_minus = int(utility_copy_temp.index(min(utility_copy_temp)))
                minus_votes[where_is_minus] += -1

            utility_copy_temp = sorted(range(len(utility_copy_temp)), key=lambda k: utility_copy_temp[k])
            utility_copy_temp.reverse()
            utility_copy_temp = [x + 1 for x in utility_copy_temp]

            for ii in range(1, to_be_deleted + 1):
                utility_copy_temp[-ii] = 0

            self.voters["Variable_Ranking"][i] = list(utility_copy_temp)
            utility_copy_temp = []

        # Transfer variable voters preferences to candidate rankings
        for i in range(1, self.number_of_candidates + 1):
            can_ranking_temp = []
            for ii in range(1, self.number_of_candidates + 1):
                vote_counter_two = 0
                for iii in range(1, self.number_of_voters + 1):
                    vote_counter = self.voters["Variable_Ranking"][iii][ii - 1]
                    if i == vote_counter:
                        vote_counter_two += 1
                can_ranking_temp.append(vote_counter_two)

            self.candidates["Variable_Ranking"][i] = list(can_ranking_temp)

            self.candidates["Variable_Ranking_Minus"][i] = list(can_ranking_temp)

        if self.number_of_candidates > 3:
            for i in range(1, self.number_of_candidates + 1):
                self.candidates["Variable_Ranking_Minus"][i][0] += minus_votes[i - 1]
        else:
            pass

    def set_current_scenario(self):
        self.current_scenario = ""

        for i in self.can_dict:
            self.current_scenario += self.can_dict[i].distribution + "_" + str(self.can_dict[i].alpha) + "_" + \
                                     str(self.can_dict[i].beta) + "__"

    def print_info(self):
        print(self.can_dict)
        print(self.voters)
        print(self.candidates)

    def results_one_round(self):
        self.temp_results = {}
        self.set_current_scenario()

        self.temp_results["Candidates"] = self.number_of_candidates
        self.temp_results["Voters"] = self.number_of_voters
        self.temp_results["PDF"] = self.current_scenario

        self.temp_results["Plurality"] = methods.x_votes(input_rankings=self.candidates["Ranking"], number_of_votes=1)

        self.temp_results["Run off"] = methods.run_off(input_rankings=self.candidates["Ranking"],
                                                       input_voters_rankings=self.voters["Ranking"],
                                                       number_of_candidates=self.number_of_candidates,
                                                       number_of_voters=self.number_of_voters)

        self.temp_results["D21+"] = methods.x_votes(input_rankings=self.candidates["Variable_Ranking"],
                                                    number_of_votes=methods.d21_votes(self.number_of_candidates))

        self.temp_results["D21-"] = methods.x_votes(input_rankings=self.candidates["Variable_Ranking_Minus"],
                                                    number_of_votes=methods.d21_votes(self.number_of_candidates))

        self.temp_results["Approval"] = methods.x_votes(input_rankings=self.candidates["Variable_Ranking"],
                                                        number_of_votes=self.number_of_candidates)

        self.temp_results["Maj judge 3"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                      scale=3,
                                                                      number_of_candidates=self.number_of_candidates)
        self.temp_results["Maj judge 5"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                      scale=5,
                                                                      number_of_candidates=self.number_of_candidates)
        self.temp_results["Maj judge 10"] = methods.majority_judgement(input_utility=self.candidates["Utility"],
                                                                       scale=10,
                                                                       number_of_candidates=self.number_of_candidates)

        self.temp_results["Borda"] = methods.borda(input_rankings=self.candidates["Ranking"],
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

        self.temp_results["Max Utility"] = methods.max_utility(input_utility=self.candidates["Utility"])
        self.temp_results["Min Utility"] = methods.min_utility(input_utility=self.candidates["Utility"])
        self.temp_results["Random"] = [random.randint(1, self.number_of_candidates)]

        self.temp_results["Condorcet"] = methods.condorcet_calculation(input_utility=self.voters["Utility"],
                                                                       number_of_candidates=self.number_of_candidates,
                                                                       number_of_voters=self.number_of_voters,
                                                                       con_winner=1, con_loser=0)

        self.temp_results["Condorcet_loser"] = methods.condorcet_calculation(input_utility=self.voters["Utility"],
                                                                             number_of_candidates=self.number_of_candidates,
                                                                             number_of_voters=self.number_of_voters,
                                                                             con_winner=0, con_loser=1)

        for i in range(2, self.number_of_candidates):
            self.temp_results["{0}Vote_Fix".format(i)] = methods.x_votes(input_rankings=self.candidates["Ranking"],
                                                                         number_of_votes=i)

        for i in range(2, self.number_of_candidates + 1):
            self.temp_results["{0}Vote_Var".format(i)] = methods.x_votes(input_rankings=self.candidates["Variable_Ranking"],
                                                                         number_of_votes=i)
