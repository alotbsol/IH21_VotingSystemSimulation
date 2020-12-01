# imports
from storage import Storage
from can_store import CandidatesStore
from scenario_2_analysis import analyze_scenario_2

from datetime import datetime
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from itertools import combinations_with_replacement


methods_list = ["Plurality", "RunOff", "D21+", "D21-", "Approval", "IRV",
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

Master_storage = Storage(methods_list=methods_list, name="Scenario_2")


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
        Master_storage.one_round_process(data_in=candidate_store.temp_results, process_no=scenario_no)


if __name__ == '__main__':
    print("calculation starts")
    start_time = datetime.now()

    candidates_scenarios = [3, 4, 5, 6, 7, 8, 9, 10, 11]
    voters_scenarios = [100, 101]
    iterations = 21000

    combinations_input = [0.333, 1, 3]

    cpu_no = cpu_count()

    for i in candidates_scenarios:
        pdfs = ["B"] * i
        combinations_created = []

        for x in combinations_with_replacement(combinations_input, i):
            combinations_created.append(x)

        for ii in range(len(combinations_created)):
            alpha_parameters = list(combinations_created[ii])
            beta_parameters = list(combinations_created[ii])

            for iii in voters_scenarios:
                print("Candidate scenario:", i)
                print(" Polarization scenario:", ii + 1, "out of", len(combinations_created))
                print("Voters scenario", iii)
                Parallel(n_jobs=cpu_no, require='sharedmem')(delayed(scenario)(
                    number_of_iterations=round(iterations/cpu_no),
                    number_of_candidates=i,
                    number_of_voters=iii,
                    distributions=pdfs,
                    alphas=alpha_parameters,
                    betas=beta_parameters,
                    scenario_no=w, ) for w in range(cpu_no))

                Master_storage.merge_processes()
                Master_storage.aggregate_results(specific_pdf_type=ii + 1)

    end_time = datetime.now()

    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)

    Master_storage.export(start=start_time, end=end_time)
    print("export done")

    analyze_scenario_2()
    print("graphic analysis done")