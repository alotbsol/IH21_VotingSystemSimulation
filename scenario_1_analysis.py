import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np


# Figures - first part - general
def scatter_bar(input_data, name, y_description):
    df = input_data
    methods = list(df.index)
    scenarios = list(df.keys())

    color_number = []
    for i in range(1, len(methods)+1):
        color_number.append(i)

    colours_list = cm.get_cmap("viridis", len(methods)+1)
    plt.figure(figsize=(12, 6))
    plt.ylim((0 - 0.02, 1 + 0.02))
    plt.ylabel(y_description)

    x = 0
    for i in methods:
        y = 1
        for ii in scenarios:
            plt.scatter(i, df.loc[i][ii], c=[colours_list(x/len(methods))], s=25 + (y*20), alpha=0.5, zorder=3)

            y += 1
        x += 1
        plt.annotate(round(np.mean(df.loc[i]), 2), xy=(i, (np.nanmax(df.loc[i]) + 0.02)), size=9, ha='center')

    plt.legend([i for i in range(3, 12)], ncol=2, loc="lower right")
    plt.locator_params(axis='y', nbins=10)
    plt.grid(linestyle='-')
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig('{0}'.format(name), bbox_inches='tight', pad_inches=0.05)
    plt.clf()
    plt.close()


# figures - polarization - relative values - chapter 4
def scatter_bar_polarization_coloured(input_data, input_methods, name, y_description,
                                      polarization_scenarios=["a_3_pol", "b_2_pol", "c_1_pol", "f_ran", "g_1_med", "h_2_med", "i_3_med"],
                                      min_candidates=3, max_candidates=11,
                                      legend_position="lower right"):

    df = input_data
    methods = input_methods
    color_number = []
    for i in range(1, len(methods) + 1):
        color_number.append(i)

    colours_list = cm.get_cmap("coolwarm_r", len(polarization_scenarios) + 1)

    plt.figure(figsize=(12, 6))
    plt.ylim((0 - 0.05, 1 + 0.15))
    plt.ylabel(y_description)

    original_labels = []

    for i in range(0, len(methods)):
        original_labels.append(i)
        averages = []

        for j in range(0, len(polarization_scenarios)):
            averages.append([])

        dot_size = 0
        for ii in range(min_candidates, max_candidates + 1):
            for iii in range(1, len(polarization_scenarios) + 1):
                the_value = df.loc[methods[i]][ii][polarization_scenarios[iii-1]]

                plt.scatter(-0.4 + i + iii*0.1, the_value, c=[colours_list((iii - 1) / len(polarization_scenarios))],
                            zorder=3, s=25 + (dot_size * 20), alpha=0.5)

                averages[iii-1].append(the_value)
            dot_size += 1

        for jj in range(0, len(polarization_scenarios)):
            averages[jj] = np.nanmean(averages[jj])

        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5, pad=0)
        plt.annotate("P:" + str(round(averages[0], 2)) + '\n' +
                     "U:" + str(round(averages[3], 2)) + '\n' +
                     "M:" + str(round(averages[6], 2)),

                     xy=(i, np.nanmax(df.loc[methods[i]]) + 0.03), size=10, ha='center', bbox=props)

    plt.locator_params(axis='y', nbins=10)
    plt.grid(linestyle='-')
    plt.xticks(original_labels, methods)  # set labels manually
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.legend(['Polarized', "", "", "Uniform", "", "", 'Medium'], ncol=1, loc=legend_position)

    plt.savefig('{0}'.format(name), bbox_inches='tight', pad_inches=0.05)
    plt.clf()
    plt.close()


def analyze_scenario_1():
    methods_for_condorcet = ["Plurality", "Run off", "D21+", "D21-", "Approval", "Maj judge 3", "Maj judge 5", "Maj judge 10", "Borda", "Range 3", "Range 5", "Range 10", "Max Utility"]
    methods_for_utility = ["Plurality", "Run off", "D21+", "D21-", "Approval", "Maj judge 3", "Maj judge 5", "Maj judge 10", "Borda", "Range 3", "Range 5", "Range 10", "Condorcet"]

    methods_fix_and_var = ["2Vote_Fix", "3Vote_Fix", "4Vote_Fix", "5Vote_Fix", "6Vote_Fix", "7Vote_Fix", "8Vote_Fix", "9Vote_Fix", "10Vote_Fix",
                    "2Vote_Var", "3Vote_Var", "4Vote_Var", "5Vote_Var", "6Vote_Var", "7Vote_Var", "8Vote_Var", "9Vote_Var", "10Vote_Var", "11Vote_Var"]

    methods_fix_and_var_p = ["Plurality", "2Vote_Fix", "3Vote_Fix", "4Vote_Fix", "5Vote_Fix", "6Vote_Fix", "7Vote_Fix", "8Vote_Fix", "9Vote_Fix", "10Vote_Fix",
                    "2Vote_Var", "3Vote_Var", "4Vote_Var", "5Vote_Var", "6Vote_Var", "7Vote_Var", "8Vote_Var", "9Vote_Var", "10Vote_Var", "11Vote_Var"]

    all_data = pd.read_excel("Scenario_1.xlsx", sheet_name="AllData", index_col=0)

    # recalculate selected Condorcet data to show percentages only when Condorcet candidate exists
    for i in ['Max Utility', "C1chosen"]:
        all_data.loc[all_data.Method == "Condorcet", i] = \
            all_data.loc[all_data.Method == "Condorcet", i] / (1 - all_data.loc[all_data.Method == "Condorcet", 'C0chosen'])

    # GRAPH IC_Condorcet
    used_methods = methods_for_condorcet + methods_fix_and_var
    selected_data = all_data.loc[all_data['PDF_type'] == "f_ran"]
    selected_data = selected_data.loc[selected_data['Method'].isin(used_methods)]

    for_graph_data = pd.pivot_table(selected_data, values="Condorcet", index="Method", columns=['Candidates'],
                                    aggfunc=np.mean)
    for_graph_data = for_graph_data.reindex(used_methods)

    scatter_bar(input_data=for_graph_data, name="IC_Condorcet",
                y_description="Frequency of selecting Condorcet winner")

    # GRAPH IC_Utility
    used_methods = methods_for_utility + methods_fix_and_var
    selected_data = all_data.loc[all_data['PDF_type'] == "f_ran"]
    selected_data = selected_data.loc[selected_data['Method'].isin(used_methods)]
    for_graph_data = pd.pivot_table(selected_data, values="Max Utility", index="Method", columns=['Candidates'],
                                    aggfunc=np.mean)
    for_graph_data = for_graph_data.reindex(used_methods)

    scatter_bar(input_data=for_graph_data, name="IC_Utility",
                y_description="Frequency of selecting highest utility candidate")

    # GRAPH Polarized Condorcet
    for_graph_data = pd.pivot_table(all_data, values="Condorcet", index="Method", columns=['Candidates', "PDF_type"],
                                    aggfunc=np.mean)

    x = 0
    for i in [methods_for_condorcet, methods_fix_and_var_p]:
        names_list = ["", "fix_and_var"]

        scatter_bar_polarization_coloured(
            input_data=for_graph_data,
            input_methods=i,
            name="1Polarized_Condorcet{0}".format(names_list[x]),
            y_description="Frequency of selecting Condorcet winner")

        x += 1

    # GRAPH Polarized Utility
    for_graph_data = pd.pivot_table(all_data, values="Max Utility", index="Method", columns=['Candidates', "PDF_type"],
                                    aggfunc=np.mean)

    x = 0
    for i in [methods_for_utility, methods_fix_and_var_p]:
        names_list = ["", "fix_and_var"]

        scatter_bar_polarization_coloured(
            input_data=for_graph_data,
            input_methods=i,
            name="1Polarized_Utility{0}".format(names_list[x]),
            y_description="Frequency of selecting highest utility candidate")

        x += 1

    # GRAPH Selecting candidate 1
    for_graph_data = pd.pivot_table(all_data, values="C1chosen", index="Method", columns=['Candidates', "PDF_type"],
                                    aggfunc=np.mean)

    x = 0
    for i in [methods_for_condorcet, methods_fix_and_var_p]:
        names_list = ["", "fix_and_var"]

        scatter_bar_polarization_coloured(
            input_data=for_graph_data,
            input_methods=i,
            name="1Polarized_Selecting_{0}".format(names_list[x]),
            legend_position="upper right",
            y_description="Frequency of selecting polarising/medium candidate")

        x += 1


if __name__ == '__main__':
    print("starting analysis")

    analyze_scenario_1()

    print("analysis finished")


