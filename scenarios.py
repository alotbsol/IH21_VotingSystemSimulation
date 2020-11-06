# imports
from storage import Storage
from can_store import CandidatesStore

from datetime import datetime
from joblib import Parallel, delayed
from multiprocessing import cpu_count


methods_list = ["1Vote", "2Vote", "3Vote", "Run off", "Borda", "Max_U", "Min_U", "Condorcet", "Condorcet_loser"]
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
    scenario1(iterations=1000)
    """

    cpu_count = cpu_count()
    Parallel(n_jobs=cpu_count)(delayed(scenario1)(iterations=8) for i in range(100))


    end_time = datetime.now()
    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)
