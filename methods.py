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






