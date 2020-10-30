# imports
from storage import Storage
from can_store import CandidatesStore


def scenario1():
    global Master_dict
    global methods_list

    Master_dict = {"can_store": [0], "storage": "", }

    methods_list = ["1Vote", "2Vote", "3Vote"]
    Master_dict["storage"] = Storage(methods_list=methods_list)

    itterations = 10

    for i in range(itterations):
        Master_dict["can_store"][0] = CandidatesStore(number_of_candidates=3,
                                                   number_of_voters=101, max_utility=1,
                                                   distribution="R")
        Master_dict["can_store"][0].print_info()
        Master_dict["can_store"][0].results_one_round()
        Master_dict["storage"].one_round(data_in=Master_dict["can_store"][0].temp_results)

    print(Master_dict["storage"].winners_rounds)


if __name__ == '__main__':
    print("calculation start")

    scenario1()

    print("calculation ends")
