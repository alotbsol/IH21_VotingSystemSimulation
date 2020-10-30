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









