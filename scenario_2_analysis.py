
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.pyplot import cm
from collections import namedtuple
from scipy.spatial import distance
import numpy as np
import random


""" ConvexHull code source: https: // startupnextdoor.com / computing - convex - hull - in -python / """
class ConvexHull(object):
    def __init__(self, graph_color):
        self._points = []
        self._hull_points = []
        self.graph_color = graph_color

    def add(self, point):
        self._points.append(point)

    def _get_orientation(self, origin, p1, p2):
        '''
        Returns the orientation of the Point p1 with regards to Point p2 using origin.
        Negative if p1 is clockwise of p2.
        '''
        difference = (
            ((p2.x - origin.x) * (p1.y - origin.y))
            - ((p1.x - origin.x) * (p2.y - origin.y))
        )

        return difference

    def compute_hull(self):
        '''
        Computes the points that make up the convex hull.
        '''
        points = self._points

        # get leftmost point
        start = points[0]
        min_x = start.x
        for p in points[1:]:
            if p.x < min_x:
                min_x = p.x
                start = p

        point = start
        self._hull_points.append(start)

        far_point = None
        while far_point is not start:
            # get the first point (initial max) to use to compare with others
            p1 = None
            for p in points:
                if p is point:
                    continue
                else:
                    p1 = p
                    break

            far_point = p1

            for p2 in points:
                # ensure we aren't comparing to self or pivot point
                if p2 is point or p2 is p1:
                    continue
                else:
                    direction = self._get_orientation(point, far_point, p2)
                    if direction > 0:
                        far_point = p2


            self._hull_points.append(far_point)
            point = far_point

    def get_hull_points(self):
        if self._points and not self._hull_points:
            self.compute_hull()

        return self._hull_points

    def display(self):
        # all points
        x = [p.x for p in self._points]
        y = [p.y for p in self._points]

        # hull points
        hx = [p.x for p in self._hull_points]
        hy = [p.y for p in self._hull_points]
        plt.plot(hx, hy, c=self.graph_color, linewidth=2, zorder=2, alpha=0.5)


class ClustersAndJarvis:
    def __init__(self, in_con, in_ut, name, scatter_alpha, annotation_alpha, second_center_size, limits, color_indexes=[],
                 in_con_all=[], in_ut_all=[], legend_scatter="YES", labels_x_y={"x": "", "y": ""}, check_random="no"):

        self.df_con = in_con
        self.df_ut = in_ut

        self.df_con_all = in_con_all
        self.df_ut_all = in_ut_all

        self.legend_scatter = legend_scatter
        self.color_indexes = color_indexes

        if check_random == "YES":
            random.Random(12).shuffle(self.color_indexes)
        else:
            pass

        self.scenarios = list(self.df_con.keys())
        self.methods = list(self.df_con.index)

        self.variable = []
        self.fixed = []
        self.statistics = {}
        self.labels_x_y = labels_x_y

        self.statistics_export = {}
        self.statistics_export["keys"] = ["Centre Condorcet", "Centre Utility", "Max dist", "STDEV dist", "Area",
                                           "C3 CC", "C3 CU", "C3 Max", "C3 STDEV",
                                           "C4 CC", "C4 CU", "C4 Max", "C4 STDEV",
                                           "C5 CC", "C5 CU", "C5 Max", "C5 STDEV",
                                           "C6 CC", "C6 CU", "C6 Max", "C6 STDEV",
                                           "C7 CC", "C7 CU", "C7 Max", "C7 STDEV",
                                           "C8 CC", "C8 CU", "C8 Max", "C8 STDEV",
                                           "C9 CC", "C9 CU", "C9 Max", "C9 STDEV",
                                           "C10 CC", "C10 CU", "C10 Max", "C10 STDEV",
                                           "C11 CC", "C11 CU", "C11 Max", "C11 STDEV",
                                          ]

        self.name = name
        self.annotation_alpha = annotation_alpha
        self.second_center_size = second_center_size
        self.scatter_alpha = scatter_alpha
        self.limits = limits
        self.picked_methods = self.methods
        self.colours_list = cm.get_cmap("viridis", len(self.color_indexes) + 1)
        self.colours_list_2 = cm.get_cmap("coolwarm")
        self.grey_color = (0.58, 0.58, 0.58, 1.0)

        plt.figure(figsize=(12, 8))

        if limits == "no":
            pass
        else:
            plt.xlim((0, limits))
            plt.ylim((0, limits))

    def scatter_only(self):
        color_number = []
        for i in range(1, len(list(self.df_con.index))+1):
            color_number.append(i)

        random_shuffle_scenarios = self.scenarios.copy()
        random.shuffle(random_shuffle_scenarios)
        for ii in random_shuffle_scenarios:
            nocandidates = ii.count("__")
            polcan = ii.count("B_0.333")
            uncan = ii.count("B_1")
            medcan = ii.count("B_3")

            #assigning right color
            try:
                use_this_color = self.colours_list_2(polcan / (polcan + medcan))
            except:
                use_this_color = self.grey_color

            for i in self.picked_methods:
                plt.scatter(self.df_con.loc[i][ii], self.df_ut.loc[i][ii],
                            c=[use_this_color], s=6 + ((nocandidates-2)*6), alpha=self.scatter_alpha, zorder=1)

        # anotation to sides
        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5)

        for i in self.picked_methods:
            plt.annotate(i, (min(self.df_con.loc[i]) - 0.015, min(self.df_ut.loc[i]) + 0.015), ha="right", size=10,
                         weight='bold', verticalalignment='bottom', alpha=self.annotation_alpha, bbox = props)

        plt.xlabel(self.labels_x_y["x"])
        plt.ylabel(self.labels_x_y["y"])

    def scatter_only_2(self):
        color_number = []
        for i in range(1, len(list(self.df_con.index)) + 1):
            color_number.append(i)

        for ii in range(0, len(self.scenarios)):
            x = 0
            for i in self.picked_methods:
                plt.scatter(self.df_con.loc[i][self.scenarios[ii]], self.df_ut.loc[i][self.scenarios[ii]],
                            c=[self.colours_list(self.color_indexes.index(i) / len(self.color_indexes))], alpha=self.scatter_alpha, zorder=1)
                x += 1

        plt.xlabel(self.labels_x_y["x"])
        plt.ylabel(self.labels_x_y["y"])

    def jarvis_fun(self, default_color="yes"):
        ListOfJarvis = []
        Point = namedtuple('Point', 'x y')

        for i in range(0, len(self.picked_methods)):
            if self.picked_methods[i] not in ["Condorcet", "Max Utility"]:
                ListOfJarvis.append(str(i))
                cl = self.color_indexes.index(self.picked_methods[i])

                if default_color == "yes":
                    graph_color = "black"
                else:
                    graph_color = self.colours_list(cl / len(self.color_indexes))

                ListOfJarvis[i] = ConvexHull(graph_color=graph_color)
            else:
                pass

        for i in range(0, len(self.picked_methods)):
            if self.picked_methods[i] not in ["Condorcet", "Max Utility"]:
                for ii in self.scenarios:
                    a = float(self.df_con.loc[str(self.picked_methods[i]), ii])
                    b = float(self.df_ut.loc[str(self.picked_methods[i]), ii])

                    ListOfJarvis[i].add(Point(a, b))

                ListOfJarvis[i].get_hull_points()
                ListOfJarvis[i].display()
                temporar_points = pd.concat((self.df_con.loc[self.picked_methods[i]], self.df_ut.loc[self.picked_methods[i]]), axis=1)
                temporar_center = self.tellme_center(input_df=temporar_points)

                self.statistics[str(self.picked_methods[i])] = []
                self.statistics[str(self.picked_methods[i])].append("  Max d: " + str(round(self.max_distance(ListOfJarvis[i]._hull_points), 2)))
                self.statistics[str(self.picked_methods[i])].append("  STDEV d: " + str(round(self.STDEV_distance(pts=ListOfJarvis[i]._points, center=temporar_center), 2)))
                self.statistics[str(self.picked_methods[i])].append("  Area: " + str(round(self.PolyArea2D(ListOfJarvis[i]._hull_points), 3)))
                self.statistics[str(self.picked_methods[i])].append("")

                self.statistics_export[str(self.picked_methods[i])] = []
                self.statistics_export[str(self.picked_methods[i])].append(str(round(self.max_distance(ListOfJarvis[i]._hull_points), 2)))
                self.statistics_export[str(self.picked_methods[i])].append(str(round(self.STDEV_distance(pts=ListOfJarvis[i]._points, center=temporar_center), 2)))
                self.statistics_export[str(self.picked_methods[i])].append(str(round(self.PolyArea2D(ListOfJarvis[i]._hull_points), 3)))

            else:
                pass

    def centers(self, black_outer_center="yes", center_annotation="no", cu="  Centre Utility: ", cc="  Centre Condorcet: ", no_stat="no", y_plus=0):
        x = 0
        for i in self.picked_methods:

            if black_outer_center == "yes":
                outer_center_c = "black"
            else:
                outer_center_c =[self.colours_list(self.color_indexes.index(i) / len(self.color_indexes))]

            df = pd.concat((self.df_con.loc[i], self.df_ut.loc[i]), axis=1)

            # drop na for variable and fixed votes who do not have all data points
            df.dropna(inplace=True)
            kmeans = KMeans(n_clusters=1)
            kmeans.fit(df)
            centers = kmeans.cluster_centers_

            cl = self.color_indexes.index(i)

            plt.scatter(centers[:, 0], centers[:, 1], c=outer_center_c, s=200,
                        alpha=1, zorder=3)

            plt.scatter(centers[:, 0], centers[:, 1], c="white", s=self.second_center_size,
                        alpha=1, zorder=4)

            if no_stat == "yes":
                pass
            else:
                if i not in ["Condorcet", "Max Utility"]:
                    self.statistics[str(i)].insert(0, cu + str(round(centers[:, 1][0], 2)))
                    self.statistics[str(i)].insert(0, cc + str(round(centers[:, 0][0], 2)))

                    self.statistics_export[str(i)].insert(0, str(round(centers[:, 1][0], 2)))
                    self.statistics_export[str(i)].insert(0, str(round(centers[:, 0][0], 2)))
                else:
                    pass

            x += 1

            if center_annotation == "yes":
                props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.25, pad=0)
                plt.text(centers[:, 0] - 0.01, centers[:, 1] + y_plus, i, fontsize=10, weight='bold', ha="right",
                         verticalalignment='bottom', alpha=self.annotation_alpha, bbox=props, zorder=4)
            else:
                pass

    def centers_candidates(self):
        #finding how many candidate is in each scenario
        list_nocandidates = []
        for i in self.scenarios:
            list_nocandidates.append(i.count("__"))

        # finding unique number of candidates
        unique_list = []
        for x in list_nocandidates:
            if x not in unique_list:
                unique_list.append(x)

        #finding positions of candidate scenarios - by number of candidates
        dict_of_positions = {}
        for i in unique_list:
            dict_of_positions[i] = []
            y = 0
            for ii in list_nocandidates:
                if i == ii:
                    dict_of_positions[i].append(y)
                else:
                    pass
                y += 1

        for i in self.picked_methods:
            if i not in ["Condorcet", "Max Utility"]:
                df = pd.concat((self.df_con.loc[i], self.df_ut.loc[i]), axis=1).copy()

                for ii in dict_of_positions:
                    df2 = df.iloc[dict_of_positions[ii]].copy()

                    centers_temp = self.tellme_center(input_df=df2)

                    self.statistics[str(i)].append("   C" + str(ii) + ":" +
                                                    " CC " + str(round(centers_temp[:, 0][0], 2)) +
                                                    " CU " + str(round(centers_temp[:, 1][0], 2)) +
                                                    " Max " + str(round(self.max_distance(pts=df2), 2)) +
                                                    " STDEV " + str(round(self.STDEV_distance(pts=df2, center=centers_temp), 2))
                                                   )

                    self.statistics_export[str(i)].append(str(round(centers_temp[:, 0][0], 2)))
                    self.statistics_export[str(i)].append(str(round(centers_temp[:, 1][0], 2)))
                    self.statistics_export[str(i)].append(str(round(self.max_distance(pts=df2), 2)))
                    self.statistics_export[str(i)].append(str(round(self.STDEV_distance(pts=df2, center=centers_temp), 2)))

            else:
                pass

    def PolyArea2D(self, pts):
        lines = np.hstack([pts, np.roll(pts, -1, axis=0)])
        area = 0.5 * abs(sum(x1 * y2 - x2 * y1 for x1, y1, x2, y2 in lines))
        return area

    def max_distance(self, pts):
        x = distance.cdist(pts, pts, 'euclidean')
        x = x.max()
        return x

    def STDEV_distance(self, pts, center):
        listofdistances = []
        for i in pts:
            y = distance.cdist(pts, center, 'euclidean')
            listofdistances.append(y)

        returnvalue = np.std(listofdistances)
        return returnvalue

    def tellme_center(self, input_df):
        input_df.dropna(inplace=True)
        kmeans = KMeans(n_clusters=1)
        kmeans.fit(input_df)
        return_center = kmeans.cluster_centers_

        return return_center

    def add_statistics(self):
        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5)

        masterstring = ""
        for i in self.statistics:
            self.statistics[i].insert(0, str(i) + ":")

            if i == "Condorcet" or i == "Max Utility":
                pass
            else:
                textstr = '\n'.join(self.statistics[i])
                masterstring = masterstring + textstr + '\n'

        plt.text(0.02, 1.02, masterstring, fontsize=10, verticalalignment='top', bbox=props)

    def add_statistics_2(self):
        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5)

        masterstring = ""
        for i in self.statistics:
            self.statistics[i].insert(0, str(i) + ":")

            if i == "Condorcet" or i == "Max Utility":
                pass
            else:
                textstr = " ".join(self.statistics[i])
                masterstring = masterstring + textstr + '\n'

        plt.text(0.02, 1.02, masterstring, fontsize=11, verticalalignment='top', bbox=props)

    def export_statistics2(self):
        df = pd.DataFrame.from_dict(self.statistics_export)
        df.to_excel("Scenario_2_analysis_output.xlsx")

    def save_it(self):
        plt.savefig('{0}'.format(self.name), bbox_inches='tight', pad_inches=0.05)
        plt.clf()
        plt.close()


# figures - all scenarios
def method_by_method_graphs():
    df_all = pd.read_excel("Scenario_2.xlsx", sheet_name="AllData", index_col=0)

    df_condorcet = pd.pivot_table(df_all, values="Condorcet", index="Method", columns=['PDF'],
                                    aggfunc=np.mean)

    df_utility = df_all.copy()
    df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] = \
        df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] / (1 - df_utility.loc[df_utility.Method == "Condorcet", 'C0chosen'])
    df_utility = pd.pivot_table(df_utility, values="Max Utility", index="Method", columns=['PDF'],
                                    aggfunc=np.mean)

    x = 1
    for i in [["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj judge 3", "Maj judge 5", "Maj judge 10", "Range 3", "Range 5", "Range 10", "Borda"],
              ["Plurality", "Max Utility", "Condorcet"],
              ["RunOff", "Max Utility", "Condorcet"],
              ["D21+", "Max Utility", "Condorcet"],
              ["D21-", "Max Utility", "Condorcet"],
              ["Approval", "Max Utility", "Condorcet"],
              ["Maj judge 3", "Max Utility", "Condorcet"],
              ["Maj judge 5", "Max Utility", "Condorcet"],
              ["Maj judge 10", "Max Utility", "Condorcet"],
              ["Range 3", "Max Utility", "Condorcet"],
              ["Range 5", "Max Utility", "Condorcet"],
              ["Range 10", "Max Utility", "Condorcet"],
              ["Borda", "Max Utility", "Condorcet"],
              ]:

        DoIt = ClustersAndJarvis(in_con=df_condorcet.loc[i],
                                 in_ut=df_utility.loc[i],
                                 in_con_all=df_condorcet,
                                 in_ut_all=df_utility,
                                 name=str("Polarization_scenarios_{0}".format(i[0])),
                                 limits=1.05,
                                 scatter_alpha=0.5,
                                 annotation_alpha=1,
                                 second_center_size=25,
                                 color_indexes=["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj judge 3", "Maj judge 5",
                                 "Maj judge 10", "Borda", "Range 3", "Range 5", "Range 10", "Condorcet", "Max Utility"],
                                 labels_x_y={"x": "Frequency of selecting Condorcet winner",
                                             "y": "Frequency of selecting highest utility candidate"})

        DoIt.scatter_only()
        DoIt.jarvis_fun()
        DoIt.centers()
        DoIt.centers_candidates()
        DoIt.add_statistics()
        DoIt.save_it()
        x += 1

    DoIt.export_statistics2()


def condorcet_analysis():
    df_all = pd.read_excel("Scenario_2.xlsx", sheet_name="AllData", index_col=0)

    df_condorcet = df_all.copy()
    df_condorcet["C0chosen"] = 1 - df_condorcet["C0chosen"]
    df_condorcet = pd.pivot_table(df_condorcet, values="C0chosen", index="Method", columns=['PDF'],
                                 aggfunc=np.mean)

    df_utility = df_all.copy()
    df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] = \
        df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] / (1 - df_utility.loc[df_utility.Method == "Condorcet", 'C0chosen'])
    df_utility = pd.pivot_table(df_utility, values="Max Utility", index="Method", columns=['PDF'],
                                    aggfunc=np.mean)

    x = 1
    for i in [["Condorcet"]]:
        DoIt = ClustersAndJarvis(in_con=df_condorcet.loc[i],
                                 in_ut=df_utility.loc[i],
                                 in_con_all=df_condorcet,
                                 in_ut_all=df_utility,
                                 name=str("Condorcet_analysis_{0}".format(x)),
                                 limits="no",
                                 scatter_alpha=0.5,
                                 annotation_alpha=0,
                                 second_center_size=25,
                                 labels_x_y={"x": "Frequency of existence of Condorcet winner",
                                             "y": "Frequency of Condorcet winner equal highest utlity winner"})
        DoIt.scatter_only()
        DoIt.jarvis_fun()
        DoIt.centers_candidates()
        DoIt.save_it()
        x += 1


def eleven_candidates():
    df_all = pd.read_excel("Scenario_2.xlsx", sheet_name="AllData", index_col=0)

    df_condorcet = df_all.copy()
    df_condorcet = df_condorcet.loc[df_condorcet.Candidates == 11]
    df_condorcet = pd.pivot_table(df_condorcet, values="Condorcet", index="Method", columns=['PDF'],
                                    aggfunc=np.mean)

    df_utility = df_all.copy()
    df_utility = df_utility.loc[df_utility.Candidates == 11]
    df_utility = pd.pivot_table(df_utility, values="Max Utility", index="Method", columns=['PDF'],
                                    aggfunc=np.mean)

    x = 1
    for i in [["Plurality", "2Vote_Fix", "3Vote_Fix", "4Vote_Fix", "5Vote_Fix", "6Vote_Fix", "7Vote_Fix", "8Vote_Fix", "9Vote_Fix",
               "10Vote_Fix", "Condorcet", "Max Utility"], ["Plurality", "2Vote_Var", "3Vote_Var", "4Vote_Var", "5Vote_Var", "6Vote_Var", "7Vote_Var", "8Vote_Var", "9Vote_Var",
               "10Vote_Var", "11Vote_Var", "Condorcet", "Max Utility"]]:

        DoIt = ClustersAndJarvis(in_con=df_condorcet.loc[i],
                                 in_ut=df_utility.loc[i],
                                 name=str("Eleven_candidates_{0}".format(x)),
                                 limits=1.05,
                                 annotation_alpha=1,
                                 scatter_alpha=0.3,
                                 second_center_size=25,
                                 color_indexes=i,
                                 labels_x_y={"x": "Frequency of selecting Condorcet winner",
                                             "y": "Frequency of selecting highest utility candidate"})

        DoIt.scatter_only_2()
        DoIt.jarvis_fun(default_color="no")
        DoIt.centers(black_outer_center="no", center_annotation="yes", cu="  CU: ", cc="  CC: ", y_plus=+0.005)
        DoIt.add_statistics_2()
        DoIt.save_it()
        x += 1


def scatter_and_centers():
    df_all = pd.read_excel("Scenario_2.xlsx", sheet_name="AllData", index_col=0)

    df_condorcet = pd.pivot_table(df_all, values="Condorcet", index="Method", columns=['PDF'],
                                  aggfunc=np.mean)

    df_utility = df_all.copy()
    df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] = \
        df_utility.loc[df_utility.Method == "Condorcet", 'Max Utility'] / (
                    1 - df_utility.loc[df_utility.Method == "Condorcet", 'C0chosen'])
    df_utility = pd.pivot_table(df_utility, values="Max Utility", index="Method", columns=['PDF'],
                                aggfunc=np.mean)

    for i in [["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj judge 3", "Maj judge 5", "Maj judge 10",
               "Range 3", "Range 5", "Range 10", "Borda", "Condorcet", "Max Utility"]]:
        DoIt = ClustersAndJarvis(in_con=df_condorcet.loc[i],
                                 in_ut=df_utility.loc[i],
                                 name="Scatter_and_centers",
                                 limits=1.05,
                                 annotation_alpha=1,
                                 scatter_alpha=0.075,
                                 second_center_size=25,
                                 color_indexes=i,
                                 labels_x_y={"x": "Frequency of selecting Condorcet winner",
                                             "y": "Frequency of selecting highest utility candidate"},
                                 check_random="YES")

        DoIt.scatter_only_2()
        DoIt.centers(black_outer_center="no", center_annotation="yes", no_stat="yes", y_plus=-0.005)
        DoIt.save_it()


def analyze_scenario_2():
    method_by_method_graphs()
    condorcet_analysis()
    eleven_candidates()
    scatter_and_centers()


if __name__ == '__main__':
    print("starting analysis: scenario 2")

    analyze_scenario_2()

    print("analysis finished")

