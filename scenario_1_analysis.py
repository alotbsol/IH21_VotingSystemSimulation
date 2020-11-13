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
                                      candidate_scenarios=9, polarization_scenarios=7,
                                      legend_position="lower right", ):
    df = input_data
    choosing_methods = {"fixedmethods": ["Plurality", "2VoteFix", "3VoteFix", "4VoteFix", "5VoteFix", "6VoteFix", "7VoteFix", "8VoteFix", "9VoteFix", "10VoteFix",],
                        "variablemethods": ["Plurality", "2VoteVar", "3VoteVar", "4VoteVar", "5VoteVar", "6VoteVar", "7VoteVar", "8VoteVar", "9VoteVar", "10VoteVar",  "11VoteVar"],
                        "fixandvar": ["Plurality", "2VoteFix", "3VoteFix", "4VoteFix", "5VoteFix", "6VoteFix", "7VoteFix", "8VoteFix", "9VoteFix", "10VoteFix", "2VoteVar", "3VoteVar", "4VoteVar", "5VoteVar", "6VoteVar", "7VoteVar", "8VoteVar", "9VoteVar", "10VoteVar",  "11VoteVar"],
                        "othermethods": ["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj_Judge3", "Maj_Judge5", "Maj_Judge10", "Borda", "Range3", "Range5", "Range10", "Maximum Utility", "Condorcet"],
                        "othermethodsU": ["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj_Judge3", "Maj_Judge5", "Maj_Judge10", "Borda", "Range3", "Range5", "Range10", "Maximum Utility", ],
                        "othermethodsC": ["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj_Judge3", "Maj_Judge5", "Maj_Judge10", "Borda", "Range3", "Range5", "Range10", "Condorcet"],
                        "allmethods": list(df.index)
                        }

    methods = choosing_methods[input_methods]

    color_number = []
    for i in range(1, len(methods) + 1):
        color_number.append(i)

    colours_list = cm.get_cmap("coolwarm_r", polarization_scenarios + 1)

    plt.figure(figsize=(12, 6))
    plt.ylim((0 - 0.05, 1 + 0.15))
    plt.ylabel(y_description)

    originallabels = []

    for i in range(0, len(methods)):
        originallabels.append(i)
        averages = []

        for j in range(0, polarization_scenarios):
            averages.append([])

        for ii in range(0, candidate_scenarios):
            for iii in range(1, polarization_scenarios + 1):
                the_value = df.loc[methods[i]][((ii) * polarization_scenarios + iii)]

                plt.scatter(-0.4 + i + iii*0.1, the_value, c=[colours_list((iii - 1) / polarization_scenarios)],
                            zorder=3, s=25 + (ii * 20), alpha=0.5)

                averages[iii-1].append(the_value)

        for jj in range(0, polarization_scenarios):
            averages[jj] = np.nanmean(averages[jj])

        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5, pad=0)
        plt.annotate("P:" + str(round(averages[0], 2)) + '\n' +
                     "U:" + str(round(averages[3], 2)) + '\n' +
                     "M:" + str(round(averages[6], 2)),

                     xy=(i, np.nanmax(df.loc[methods[i]]) + 0.02), size=10, ha='center', bbox=props)

    plt.locator_params(axis='y', nbins=10)
    plt.grid(linestyle='-')
    plt.xticks(originallabels, methods)  # set labels manually
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.legend(['Polarized', "", "", "Uniform", "", "", 'Medium'], ncol=1, loc=legend_position)

    plt.savefig('{0}'.format(name), bbox_inches='tight', pad_inches=0.05)
    plt.clf()
    plt.close()



def analyze_scenario_1():
    scatter_bar(input_data=pd.read_excel("21000it_linear_adj.xlsx", sheet_name="con_ran", index_col=0), name="IC_Condorcet",
                y_description="Frequency of selecting Condorcet winner")

    scatter_bar(input_data=pd.read_excel("21000it_linear_adj.xlsx", sheet_name="ut_ran", index_col=0), name="IC_Utility",
                y_description="Frequency of selecting highest utility candidate")


    for i in ["othermethodsU", "fixandvar"]:
        scatter_bar_polarization_coloured(
            input_data=pd.read_excel("21000it_linear_adj.xlsx", sheet_name="con_pol", index_col=0),
            input_methods=i,
            name="1Polarized_Condorcet{0}".format(i),
            y_description="Frequency of selecting Condorcet winner")

    for i in ["othermethodsC", "fixandvar"]:
        scatter_bar_polarization_coloured(
            input_data=pd.read_excel("21000it_linear_adj.xlsx", sheet_name="ut_pol", index_col=0),
            input_methods=i,
            name="1Polarized_Utility{0}".format(i),
            y_description="Frequency of selecting highest utility candidate")

    for i in ["othermethods", "fixandvar"]:
        scatter_bar_polarization_coloured(
            input_data=pd.read_excel("21000it_linear_adj.xlsx", sheet_name="choosing_can1", index_col=0),
            input_methods=i,
            name="1Polarized_Selecting_{0}".format(i),
            legend_position="upper right",
            y_description="Frequency of selecting polarising/medium candidate")


if __name__ == '__main__':
    print("starting analysis")

    analyze_scenario_1()

    print("starting analysis")

