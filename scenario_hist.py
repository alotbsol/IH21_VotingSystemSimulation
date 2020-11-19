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
for i in range(2, 11):
    methods_list.append("{0}Vote_Fix".format(i))
for i in range(2, 12):
    methods_list.append("{0}Vote_Var".format(i))

Master_storage = Storage(methods_list=methods_list, name="Scenario_histograms")


def scenario(number_of_iterations, scenario_no, number_of_candidates, number_of_voters,
             distributions, alphas, betas):
    Master_storage.create_process(process_no=scenario_no)

    for rounds in range(number_of_iterations):
        candidate_store = CandidatesStore(number_of_voters=number_of_voters)
        for can in range(number_of_candidates):
            candidate_store.add_candidate(distribution=distributions[can],
                                          alpha=alphas[can],
                                          beta=betas[can])

        candidate_store.voters_preferences()
        candidate_store.results_one_round()
        candidate_store.store_histograms()
        Master_storage.one_round_process(data_in=candidate_store.temp_results, process_no=scenario_no)


if __name__ == '__main__':
    print("calculation starts")
    start_time = datetime.now()

    candidates_scenarios = [3, 4, 5]
    """
    [3, 4, 5, 6, 7, 8, 9, 10, 11]
    """
    voters_scenarios = [100, 101]
    iterations = 10

    cpu_no = cpu_count()
    cpu_no = 1

    for i in candidates_scenarios:
        pdfs = ["B"] * i
        alpha_parameters = [1] * i
        beta_parameters = [1] * i

        for ii in voters_scenarios:
            print("Candidate scenario:", i)
            print("Voters scenario", ii)
            Parallel(n_jobs=cpu_no, require='sharedmem')(delayed(scenario)(
                number_of_iterations=round(iterations/cpu_no),
                number_of_candidates=i,
                number_of_voters=ii,
                distributions=pdfs,
                alphas=alpha_parameters,
                betas=beta_parameters,
                scenario_no=w, ) for w in range(cpu_no))

            Master_storage.merge_processes()
            Master_storage.aggregate_results()

    end_time = datetime.now()

    Master_storage.export(start=start_time, end=end_time)

    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)