
def compare(comparing, comparing_to):
    storage = []
    for i in range(0, len(comparing)):
        if comparing[i] == comparing_to[i]:
            storage.append(1)
        else:
            storage.append(0)
    if sum(storage) > 0:
        x = (sum(storage) / len(storage))
    else:
        x = 0

    return x


def condorcet_compare(comparing, comparing_to):
    storage = []
    storage_condorcet = []

    for i in range(0, len(comparing)):
        if comparing[i] == [0]:
            storage.append(0)

        elif comparing[i] == comparing_to[i]:
            storage.append(1)
        else:
            storage.append(0)

    for ii in range(0, len(comparing_to)):
        if comparing_to[ii][0] > 0:
            storage_condorcet.append(1)
        else:
            storage_condorcet.append(0)

    if sum(storage) > 0:
        x = (sum(storage)/sum(storage_condorcet))
    else:
        x = 0

    return x


def condorcet_compare_proportion(comparing, comparing_to):
    storage = []
    storage_condorcet = []

    for i in range(0, len(comparing)):
        for ii in range(0, len(comparing[i])):
            if comparing[i][ii] == 0:
                storage.append(0)
            elif comparing[i][ii] == comparing_to[i][0]:
                storage.append(1/len(comparing[i]))
            else:
                storage.append(0)

    for ii in range(0, len(comparing_to)):
        if comparing_to[ii][0] > 0:
            storage_condorcet.append(1)
        else:
            storage_condorcet.append(0)

    if sum(storage) > 0:
        x = (sum(storage)/sum(storage_condorcet))
    else:
        x = 0

    return x


