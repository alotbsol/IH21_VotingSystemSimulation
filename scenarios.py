# imports
from storage import Storage
from can_store import CandidatesStore

from datetime import datetime
from joblib import Parallel, delayed
from multiprocessing import cpu_count


methods_list = ["Plurality", "Run off", "D21+", "D21-", "Approval",
                "Maj judge 3", "Maj judge 5", "Maj judge 10",
                "Borda",
                "Range 3", "Range 5", "Range 10",
                "Max Utility", "Min Utility",
                "Condorcet", "Condorcet_loser",
                "Random"]
for i in range(2, 12):
    methods_list.append("{0}Vote_Fix".format(i))
for i in range(2, 12):
    methods_list.append("{0}Vote_Var".format(i))

Master_storage = Storage(methods_list=methods_list)


def scenario1(iterations, scenario):
    master_dict = {"can_store": [0]}

    Master_storage.create_process(process_no=scenario)

    for i in range(iterations):
        master_dict["can_store"][0] = CandidatesStore(number_of_candidates=3,
                                                   number_of_voters=10, max_utility=1,
                                                   distribution="R")

        master_dict["can_store"][0].results_one_round()
        Master_storage.one_round_process(data_in=master_dict["can_store"][0].temp_results, process_no=scenario)


if __name__ == '__main__':
    print("calculation starts")
    start_time = datetime.now()

    for i in range(3):
        cpu_no = cpu_count()
        Parallel(n_jobs=cpu_no, prefer="threads")(delayed(scenario1)(iterations=100, scenario=i) for i in range(8))

        Master_storage.merge_processes()
        Master_storage.aggregate_results()

    Master_storage.export()

    end_time = datetime.now()
    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)
