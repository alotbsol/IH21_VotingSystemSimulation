# imports
import itertools
import random
from math import ceil
from math import sqrt
from math import floor
from statistics import median_low


# calculate results based on various voting methods
def x_votes(input_rankings, number_of_votes, max_votes=100):
    votes_storage = []

    if max_votes > number_of_votes:
        for i in input_rankings:
            votes_sum = sum(input_rankings[i][0:number_of_votes])
            votes_storage.append(votes_sum)

        winner_votes = max(votes_storage)
        winner = [iii for iii, j in enumerate(votes_storage) if j == winner_votes]
        winner = [x + 1 for x in winner]
    else:
        winner = "nan"

    return winner


def max_utility(input_utility):
    finding_max = []
    for i in input_utility:
        finding_max.append(sum(input_utility[i]))

    max_utility_value = max(finding_max)
    winner = [iii for iii, j in enumerate(finding_max) if j == max_utility_value]
    winner = [x + 1 for x in winner]

    return winner


def min_utility(input_utility):
    finding_min = []
    for i in input_utility:
        finding_min.append(sum(input_utility[i]))

    min_utility_value = min(finding_min)
    loser = [iii for iii, j in enumerate(finding_min) if j == min_utility_value]
    loser = [x + 1 for x in loser]

    return loser


def borda(input_rankings, number_of_candidates):
    borda_results = []
    for i in range(1, number_of_candidates + 1):
        points_for_candidate_total = 0
        for ii in range(1, number_of_candidates + 1):
            points_for_candidate = input_rankings[i][ii-1]
            points_for_candidate_total = points_for_candidate_total + points_for_candidate*(number_of_candidates-ii)
        borda_results.append(points_for_candidate_total)

    winner = max(borda_results)
    winner = [ii for ii, j in enumerate(borda_results) if j == winner]
    winner = [x+1 for x in winner]

    return winner


def run_off(input_rankings, input_voters_rankings, number_of_candidates, number_of_voters):
    first_round_winners = []
    rankings_copy = []

    # first round
    for i in range(1, number_of_candidates + 1):
        rankings_copy.append(input_rankings[i][0])

    for i in range(len(rankings_copy)):
        if rankings_copy[i] == max(rankings_copy):
            first_round_winners.append(i + 1)
        else:
            pass

    if len(first_round_winners) == 2:
        pass
    elif len(first_round_winners) > 2:
        first_round_winners = random.sample(first_round_winners, 2)

    elif len(first_round_winners) < 2:
        local_copy = list(rankings_copy)
        for i in range(len(local_copy)):
            if local_copy[i] == max(rankings_copy):
                local_copy[i] = 0
            else:
                pass

        second_winner = []
        for i in range(len(local_copy)):
            if local_copy[i] == max(local_copy):
                second_winner.append(i + 1)
            else:
                pass

        picked = random.sample(second_winner, 1)
        first_round_winners.append(picked[0])
    else:
        pass

    # second round
    first = 0
    second = 0
    for i in range(1, number_of_voters + 1):
        first_in_round = 0
        second_in_round = 0
        for ii in range(number_of_candidates):
            if input_voters_rankings[i][ii] == first_round_winners[0]:
                first_in_round = int(ii)
            elif input_voters_rankings[i][ii] == first_round_winners[1]:
                second_in_round = int(ii)
            else:
                pass

        if first_in_round < second_in_round:
            first += 1
        elif first_in_round > second_in_round:
            second += 1
        else:
            pass

    winner = 0
    if first > second:
        winner = [first_round_winners[0]]
    elif first < second:
        winner = [first_round_winners[1]]
    elif first == second:
        winner = first_round_winners[0:2]

    return winner


def range_voting(input_utility, scale, number_of_candidates):
    range_results = []
    for i in range(1, number_of_candidates + 1):
        temp_copy = input_utility[i].copy()
        temp_copy = [ceil(k * scale) for k in temp_copy]
        range_results.append(sum(temp_copy))

    winner = [i for i, n in enumerate(range_results) if n == max(range_results)]
    winner = [x + 1 for x in winner]

    return winner


def majority_judgement(input_utility, scale, number_of_candidates):
    winner = []
    losers = set()
    median_score = 0
    end_it = 0

    utility_copy = input_utility.copy()
    for i in range(1, number_of_candidates + 1):
        utility_copy[i] = [ceil(k * scale) for k in utility_copy[i]]

    while len(winner) != 1:
        maj_results = []
        for i in range(1, number_of_candidates + 1):
            try:
                utility_copy[i].remove(median_score)
            except:
                pass

            try:
                maj_results.append(median_low(utility_copy[i]))
            except:
                end_it = 1

        if end_it == 1:
            break
        else:
            median_score = (max(maj_results))
            winner = [i for i, n in enumerate(maj_results) if n == median_score]
            losers_temp = [i for i, n in enumerate(maj_results) if n != median_score]

            winner = [x + 1 for x in winner]
            losers_temp = [x + 1 for x in losers_temp]

            for w in losers_temp:
                losers.add(w)

            for w in losers:
                for ww in range(len(utility_copy[w])):
                    utility_copy[w][ww] = 0

    return winner


def condorcet_calculation(input_utility, number_of_candidates, number_of_voters, con_winner=1, con_loser=0):
    candidates_list = []
    candidates_pairs_creation = []
    condorcet_calc = []
    results_condorcet_all = []
    every_element = []
    candidate_condorcet_storage = []
    winner = [0]

    for i in range(1, number_of_candidates + 1):
        candidates_list.append(i)

    # creates candidate pairs
    for pairs in itertools.combinations(candidates_list, 2):
        candidates_pairs_creation.append(pairs)

    candidates_pairs_creation = [item for sublist in candidates_pairs_creation for item in sublist]
    number_of_iterations = int(len(candidates_pairs_creation))
    number_of_pairs = number_of_iterations // 2

    for i in range(1, number_of_voters + 1):
        for ii in range(number_of_iterations):
            position_helper = candidates_pairs_creation[ii] - 1
            condorcet_calc.append(input_utility[i][position_helper])

    length_of_calc = len(condorcet_calc)
    half_length_of_calc = int(length_of_calc / 2)

    for i in range(length_of_calc):
        every_element.append(i)
    every_first_element = every_element[::2]
    every_second_element = every_element[1::2]

    for i in range(half_length_of_calc):
        position_a = every_first_element[i]
        position_b = every_second_element[i]
        a = condorcet_calc[position_a]
        b = condorcet_calc[position_b]
        if a > b:
            results_condorcet_all.append(con_winner)
        elif b > a:
            results_condorcet_all.append(con_loser)
        else:
            results_condorcet_all.append(0)

    for i in range(1, number_of_pairs + 1):
        helper = results_condorcet_all[i - 1::number_of_pairs]
        helper = sum(helper)
        if helper > number_of_voters / 2:
            candidate_condorcet_storage.append([1, 0])
        elif helper < number_of_voters / 2:
            candidate_condorcet_storage.append([0, 1])
        else:
            candidate_condorcet_storage.append([0, 0])

    candidate_condorcet_storage = [item for sublist in candidate_condorcet_storage for item in sublist]

    results = {}
    for i in range(1, number_of_candidates + 1):
        results[i] = []

    for i in range(0, number_of_iterations):
        copy_of_candidate = candidates_pairs_creation[i]
        copy_of_result = candidate_condorcet_storage[i]
        results[copy_of_candidate].append(copy_of_result)

    for i in range(1, number_of_candidates + 1):
        a = len(results[i])
        b = sum(results[i])
        if a == b:
            winner[0] = i

    return winner


def d21_votes(number_of_candidates, winners=1):
    ideal_votes = round(2*winners - (winners - 2)*0.618)
    votes_function = int((1/2)*(sqrt((winners - 1) ** 2 + (4 * number_of_candidates)) + winners - 1))

    if number_of_candidates == 3:
        return 2
    else:
        return floor(min(ideal_votes, votes_function))


def irv(input_voters_rankings, number_of_candidates):
    rankings_copy = input_voters_rankings.copy()
    votes_for_candidates = [0] * number_of_candidates
    winner_votes = -1
    winner = 0

    x = 0
    while winner_votes < sum(votes_for_candidates)/2:
        all_votes_storage = []
        for i in rankings_copy:
            all_votes_storage.append(rankings_copy[i][0])

        votes_for_candidates = [0] * (number_of_candidates)
        for i in range(1, number_of_candidates + 1):
            for ii in all_votes_storage:
                if ii == i:
                    votes_for_candidates[i-1] += 1
                else:
                    pass

        winner_votes = max(votes_for_candidates)
        sorted_votes_for_candidates = votes_for_candidates.copy()
        sorted_votes_for_candidates.sort()
        loser_votes = sorted_votes_for_candidates[x]

        deleted_candidates = 0
        if loser_votes == 0:
            loser = [iii for iii, j in enumerate(votes_for_candidates) if j == loser_votes]
            loser = [i + 1 for i in loser]
            for i in loser:
                for ii in range(1, len(rankings_copy) + 1):
                    try:
                        rankings_copy[ii].remove(i)
                        deleted_candidates += 1
                    except ValueError:
                        pass

        else:
            loser = [iii for iii, j in enumerate(votes_for_candidates) if j == loser_votes]
            loser = random.choice(loser)
            loser += 1

            for i in range(1, len(rankings_copy) + 1):
                rankings_copy[i].remove(loser)
                deleted_candidates += 1

        x += int(deleted_candidates/len(rankings_copy))
        winner = [iii for iii, j in enumerate(votes_for_candidates) if j == winner_votes]
        winner = [y + 1 for y in winner]

    return winner
