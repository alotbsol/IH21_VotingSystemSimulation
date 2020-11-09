# imports
from storage import Storage
from can_store import CandidatesStore

from datetime import datetime
from joblib import Parallel, delayed
from multiprocessing import cpu_count


methods_list = ["Plurality", "Run off", "Borda",
                "Maj judge 3", "Maj judge 5", "Maj judge 10",
                "Range 3", "Range 5", "Range 10",
                "Max_U", "Min_U", "Condorcet", "Condorcet_loser"]

for i in range(1, 12):
    methods_list.append("{0}Vote_Fix".format(i))

for i in range(1, 12):
    methods_list.append("{0}Vote_Var".format(i))

for i in range(1, 12):
    methods_list.append("{0}Vote_Var-".format(i))

Master_storage = Storage(methods_list=methods_list)


def scenario1(iterations):
    master_dict = {"can_store": [0]}

    for i in range(iterations):
        master_dict["can_store"][0] = CandidatesStore(number_of_candidates=3,
                                                   number_of_voters=10, max_utility=1,
                                                   distribution="R")

        master_dict["can_store"][0].results_one_round()

        Master_storage.one_round(data_in=master_dict["can_store"][0].temp_results)


if __name__ == '__main__':
    print("calculation starts")
    start_time = datetime.now()

    """
    for i in range(100):
        scenario1(iterations=8)
    """


    cpu_count = cpu_count()
    Parallel(n_jobs=cpu_count)(delayed(scenario1)(iterations=100) for i in range(100))


    end_time = datetime.now()
    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)
