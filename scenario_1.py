# imports
from storage import Storage
from can_store import CandidatesStore
from scenario_1_analysis import analyze_scenario_1

from datetime import datetime
from joblib import Parallel, delayed
from multiprocessing import cpu_count


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

Master_storage = Storage(methods_list=methods_list, name="Scenario_1")


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

    can_1_scenarios = {"a_3_pol": [0.333, 0.333], "b_2_pol": [0.5, 0.5], "c_1_pol": [0.667, 0.667],
                    "f_ran": [1, 1],
                    "g_1_med": [1.333, 1.333], "h_2_med": [2, 2], "i_3_med": [3, 3]}

    voters_scenarios = [100, 101]

    iterations = 73000

    cpu_no = cpu_count()
    counter_candidate = 1
    for i in candidates_scenarios:
        pdfs = ["B"] * i
        alpha_parameters = [1] * i
        beta_parameters = [1] * i

        counter_polarization = 1
        for ii in can_1_scenarios:
            alpha_parameters[0] = can_1_scenarios[ii][0]
            beta_parameters[0] = can_1_scenarios[ii][1]

            counter_voter = 1
            for iii in voters_scenarios:
                print("RUNNING:")
                print("   Candidate scenario:", counter_candidate, "of:", len(candidates_scenarios))
                print("   Polarization scenario:", counter_polarization, "of:", len(can_1_scenarios))
                print("   Voters scenario", counter_voter, "of:", len(voters_scenarios))

                Parallel(n_jobs=cpu_no, require='sharedmem')(delayed(scenario)(
                    number_of_iterations=round(iterations/cpu_no),
                    number_of_candidates=i,
                    number_of_voters=iii,
                    distributions=pdfs,
                    alphas=alpha_parameters,
                    betas=beta_parameters,
                    scenario_no=w, ) for w in range(cpu_no))

                Master_storage.merge_processes()
                Master_storage.aggregate_results(specific_pdf_type=ii)

                counter_voter += 1
            counter_polarization += 1
        counter_candidate += 1

    end_time = datetime.now()

    print("calculation ends")
    print("START:", start_time)
    print("END:", end_time)

    Master_storage.export(start=start_time, end=end_time)
    print("export done")

    print("graphic analysis starts")
    analyze_scenario_1()
    print("graphic analysis done")

