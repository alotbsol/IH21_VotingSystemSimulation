import itertools


# calculate results based on various voting methods
def x_votes(input_rankings, number_of_votes):
    votes_storage = []
    for i in input_rankings:
        votes_sum = sum(input_rankings[i][0:number_of_votes])
        votes_storage.append(votes_sum)

    winner_votes = max(votes_storage)
    winner = [iii for iii, j in enumerate(votes_storage) if j == winner_votes]
    winner = [x + 1 for x in winner]

    print(number_of_votes, "vote winner is:", winner)
    return winner


def max_utility(input_utility):
    finding_max = []
    for i in input_utility:
        finding_max.append(input_utility[i])

    max_utility_value = max(finding_max)
    winner = [iii for iii, j in enumerate(finding_max) if j == max_utility_value]
    winner = [x + 1 for x in winner]

    print("Max U winner is:", winner)
    return winner


def min_utility(input_utility):
    finding_min = []
    for i in input_utility:
        finding_min.append(input_utility[i])

    min_utility_value = min(finding_min)
    loser = [iii for iii, j in enumerate(finding_min) if j == min_utility_value]
    loser = [x + 1 for x in loser]

    print("Min U candidate is:", loser)
    return loser


def condorcet_calculation(input_utility, number_of_candidates, number_of_voters):
    candidates_list = []
    candidates_pairs_creation = []
    condorcet_calc = []
    results_condorcet_all = []
    every_element = []
    candidate_condorcet_storage = []
    winner = [0]

    for i in range(1, number_of_candidates + 1):
        candidates_list.append(i)

    #creates candidate pairs
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
            results_condorcet_all.append(1)
        elif b > a:
            results_condorcet_all.append(0)
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

    print("Condorcet Winner is:", winner)
    return winner










