
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
    def __init__(self, graphcolor):
        self._points = []
        self._hull_points = []
        self.graphcolor = graphcolor

    def add(self, point):
        self._points.append(point)

    def _get_orientation(self, origin, p1, p2):
        '''
        Returns the orientation of the Point p1 with regards to Point p2 using origin.
        Negative if p1 is clockwise of p2.
        :param p1:
        :param p2:
        :return: integer
        '''
        difference = (
            ((p2.x - origin.x) * (p1.y - origin.y))
            - ((p1.x - origin.x) * (p2.y - origin.y))
        )

        return difference

    def compute_hull(self):
        '''
        Computes the points that make up the convex hull.
        :return:
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
        plt.plot(hx, hy, c=self.graphcolor, linewidth=2, zorder=2, alpha=0.5)


class ClustersAndJarvis():
    def __init__(self, in_con, in_ut, name, scatter_alpha, annotationalpha, second_center_size, limits, colorindexes=[],
                 in_con_all=[], in_ut_all=[], legend_scatter="YES"):

        self.df_con = in_con
        self.df_ut = in_ut

        self.df_con_all = in_con_all
        self.df_ut_all = in_ut_all

        self.legend_scatter = legend_scatter
        self.colorindexes = colorindexes

        self.scenarios = list(self.df_con.keys())
        self.methods = list(self.df_con.index)

        self.variable = []
        self.fixed = []
        self.statistics = []
        self.statistics2 = {}

        self.statistics_export = {}
        self.statistics_export["keys"] = ["Center Condorcet", "Center Utility", "Max dist", "STDEV dist", "Area",
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
        self.annotationalpha = annotationalpha
        self.second_center_size = second_center_size
        self.scatter_alpha = scatter_alpha
        self.limits = limits
        self.pickedmethods = self.methods
        self.colourslist = cm.get_cmap("viridis", len(self.colorindexes) + 1)

        self.colourslist2 = cm.get_cmap("coolwarm")
        self.grey_color = (0.58, 0.58, 0.58, 1.0)

        plt.figure(figsize=(12, 8))
        plt.xlim((0, limits))
        plt.ylim((0, limits))

    def scatteronly(self):
        legendlabels = list(self.df_con.index)
        colornumber = []
        for i in range(1, len(legendlabels)+1):
            colornumber.append(i)

        random_shuffle_scenarios = self.scenarios.copy()
        random.shuffle(random_shuffle_scenarios)
        for ii in random_shuffle_scenarios:
            nocandidates = ii.count("_")
            polcan = ii.count("Ba0.333")
            uncan = ii.count("Ba1b1")
            medcan = ii.count("Ba3b3")

            #assigning right color
            try:
                use_this_color = self.colourslist2(polcan/(polcan+medcan))
            except:
                use_this_color = self.grey_color

            for i in self.pickedmethods:
                plt.scatter(self.df_con.loc[i][ii], self.df_ut.loc[i][ii],
                            c=[use_this_color], s=6 + ((nocandidates-2)*6), alpha=self.scatter_alpha, zorder=1)

        # anotation to sides
        props = dict(boxstyle='square', edgecolor='none', facecolor='white', alpha=0.5)

        for i in self.pickedmethods:
            plt.annotate(i, (min(self.df_con.loc[i]) - 0.015, min(self.df_ut.loc[i]) + 0.015), ha="right", size=10,
                         weight='bold', verticalalignment='bottom', alpha=self.annotationalpha, bbox = props)


        plt.xlabel("Frequency of selecting Condorcet winner")
        plt.ylabel("Frequency of selecting highest utility candidate")
        """
        plt.xlabel("Frequency of existence of Condorcet winner")
        plt.ylabel("Frequency of Condorcet winner equal highest utlity winner")
        """

    def bacground_scatter(self):
        backgroundmethods = ["Condorcet", "Plurality", "Maj_Judge10", "Maj_Judge3", "Maj_Judge5",
                        "Range3", "Range5", "Range10", "D21-", "D21+", "RunOff", "Borda", "Approval", "Max U"]

        for j in self.methods:
            try:
                backgroundmethods.remove(j)
            except:
                pass

        for ii in range(0, len(self.scenarios)):
            x = 0

            for i in backgroundmethods:
                cl = self.colorindexes.index(i)
                plt.scatter(self.df_con_all.loc[i][self.scenarios[ii]], self.df_ut_all.loc[i][self.scenarios[ii]], c=[self.colourslist(cl/len(self.colorindexes))], alpha=0.01, zorder=2, s=50)

                x += 1

    def jarvisfun(self):
        ListOfJarvis = []
        Point = namedtuple('Point', 'x y')

        for i in range(0, len(self.pickedmethods)):
            ListOfJarvis.append(str(i))
            cl = self.colorindexes.index(self.pickedmethods[i])
            ListOfJarvis[i] = ConvexHull(graphcolor="black")
            """self.colourslist(cl/len(self.colorindexes))"""
        for i in range(0, len(self.pickedmethods)):
            for ii in self.scenarios:
                a = float(self.df_con.loc[str(self.pickedmethods[i]), ii])
                b = float(self.df_ut.loc[str(self.pickedmethods[i]), ii])

                ListOfJarvis[i].add(Point(a, b))

            ListOfJarvis[i].get_hull_points()
            ListOfJarvis[i].display()

            temporar_points = pd.concat((self.df_con.loc[self.pickedmethods[i]], self.df_ut.loc[self.pickedmethods[i]]), axis=1)
            temporar_center = self.tellme_center(input_df=temporar_points)

            appending = str(str(self.pickedmethods[i]) + ":     "
                            + "Max dist: " + str(round(self.max_distance(ListOfJarvis[i]._hull_points), 2))
                            + "     "
                            + "STDEV dist: " + str(round(self.STDEV_distance(pts=ListOfJarvis[i]._points, center=temporar_center), 2))
                            + "     "
                            + "Area: " + str(round(self.PolyArea2D(ListOfJarvis[i]._hull_points), 3))
                            )
            self.statistics.append(str(appending))

            self.statistics2[str(self.pickedmethods[i])] = []
            self.statistics2[str(self.pickedmethods[i])].append("   Max dist: " + str(round(self.max_distance(ListOfJarvis[i]._hull_points), 2)))
            self.statistics2[str(self.pickedmethods[i])].append("   STDEV dist: " + str(round(self.STDEV_distance(pts=ListOfJarvis[i]._points, center=temporar_center), 2)))
            self.statistics2[str(self.pickedmethods[i])].append("   Area: " + str(round(self.PolyArea2D(ListOfJarvis[i]._hull_points), 3)))
            self.statistics2[str(self.pickedmethods[i])].append("")

            self.statistics_export[str(self.pickedmethods[i])] = []
            self.statistics_export[str(self.pickedmethods[i])].append(str(round(self.max_distance(ListOfJarvis[i]._hull_points), 2)))
            self.statistics_export[str(self.pickedmethods[i])].append(str(round(self.STDEV_distance(pts=ListOfJarvis[i]._points, center=temporar_center), 2)))
            self.statistics_export[str(self.pickedmethods[i])].append(str(round(self.PolyArea2D(ListOfJarvis[i]._hull_points), 3)))


    def centers(self):
        x = 0
        for i in self.pickedmethods:
            df = pd.concat((self.df_con.loc[i], self.df_ut.loc[i]), axis=1)

            # drop na for variable and fixed votes who do not have all data points
            df.dropna(inplace=True)
            kmeans = KMeans(n_clusters=1)
            kmeans.fit(df)
            centers = kmeans.cluster_centers_

            cl = self.colorindexes.index(i)

            plt.scatter(centers[:, 0], centers[:, 1], c="black", s=200,
                        alpha=1, zorder=3)

            plt.scatter(centers[:, 0], centers[:, 1], c="white", s=self.second_center_size,
                        alpha=1, zorder=4)

            self.statistics2[str(i)].insert(0, "   Center Utility: " + str(round(centers[:, 1][0], 2)))
            self.statistics2[str(i)].insert(0, "   Center Condorcet: " + str(round(centers[:, 0][0], 2)))

            self.statistics_export[str(i)].insert(0, str(round(centers[:, 1][0], 2)))
            self.statistics_export[str(i)].insert(0, str(round(centers[:, 0][0], 2)))

            x += 1

    def centers_candidates(self):
        #finding how many candidate is in each scenario
        list_nocandidates = []
        for i in self.scenarios:
            list_nocandidates.append(i.count("_"))

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

        for i in self.pickedmethods:
            df = pd.concat((self.df_con.loc[i], self.df_ut.loc[i]), axis=1).copy()

            for ii in dict_of_positions:
                df2 = df.iloc[dict_of_positions[ii]].copy()

                centers_temp = self.tellme_center(input_df=df2)

                self.statistics2[str(i)].append("   C" + str(ii) + ":" +
                                                " CC " + str(round(centers_temp[:, 0][0], 2)) +
                                                " CU " + str(round(centers_temp[:, 1][0], 2)) +
                                                " Max " + str(round(self.max_distance(pts=df2), 2)) +
                                                " STDEV " + str(round(self.STDEV_distance(pts=df2, center=centers_temp), 2))
                                                )

                self.statistics_export[str(i)].append(str(round(centers_temp[:, 0][0], 2)))
                self.statistics_export[str(i)].append(str(round(centers_temp[:, 1][0], 2)))
                self.statistics_export[str(i)].append(str(round(self.max_distance(pts=df2), 2)))
                self.statistics_export[str(i)].append(str(round(self.STDEV_distance(pts=df2, center=centers_temp), 2)))

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
        for i in self.statistics2:
            self.statistics2[i].insert(0, str(i) + ":")

            if i == "Condorcet" or i == "Max U":
                pass
            else:
                textstr = '\n'.join(self.statistics2[i])
                masterstring = masterstring + textstr + '\n'

        plt.text(0.02, 1.02, masterstring, fontsize=11, verticalalignment='top', bbox=props)

    def export_statistics2(self):
        df = pd.DataFrame.from_dict(self.statistics_export)
        df.to_excel("Scenario_2_analysis_output.xlsx")

    def saveit(self):
        plt.savefig('{0}'.format(self.name), bbox_inches='tight', pad_inches=0.05)
        plt.clf()
        plt.close()


#figures - all scenarios
def allbyall_comp():
    condorcet = pd.read_excel("21000it_montecarlo_adj.xlsx", sheet_name="all_con", index_col=0)
    utility = pd.read_excel("21000it_montecarlo_adj.xlsx", sheet_name="all_ut", index_col=0)

    x = 1
    for i in [["Plurality", "Max U", "Condorcet"],
              ["RunOff", "Max U", "Condorcet"],
              ["D21+", "Max U", "Condorcet"],
              ["D21-", "Max U", "Condorcet"],
              ["Approval", "Max U", "Condorcet"],
              ["Maj_Judge3", "Max U", "Condorcet"],
              ["Maj_Judge5", "Max U", "Condorcet"],
              ["Maj_Judge10", "Max U", "Condorcet"],
              ["Range3", "Max U", "Condorcet"],
              ["Range5", "Max U", "Condorcet"],
              ["Range10", "Max U", "Condorcet"],
              ["Borda", "Max U", "Condorcet"]
              ]:

        doit = ClustersAndJarvis(in_con=condorcet.loc[i],
                                 in_ut=utility.loc[i],
                                 in_con_all=condorcet,
                                 in_ut_all=utility,
                                 name=str(x),
                                 limits=1.05,
                                 scatter_alpha=0.5,
                                 annotationalpha=1,
                                 second_center_size=25,
                                 colorindexes=["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj_Judge3", "Maj_Judge5", "Maj_Judge10", "Borda", "Range3", "Range5", "Range10", "Condorcet", "Max U"])

        doit.scatteronly()
        doit.jarvisfun()
        doit.centers()
        doit.centers_candidates()
        doit.add_statistics()
        doit.saveit()
        x += 1

    doit.export_statistics2()


def allbyall_comp_con():

    condorcet = pd.read_excel("21000it_montecarlo_adj_forcondorcet.xlsx", sheet_name="all_con", index_col=0)
    utility = pd.read_excel("21000it_montecarlo_adj_forcondorcet.xlsx", sheet_name="all_ut", index_col=0)

    x = 1
    for i in[
             ["c"],
             ]:

        """["Plurality", "Max U", "Condorcet", ],
             ["Condorcet_notadjusted", "Max U", "Condorcet",],"""

        doit = ClustersAndJarvis(in_con=condorcet.loc[i],
                                 in_ut=utility.loc[i],
                                 in_con_all=condorcet,
                                 in_ut_all=utility,
                                 name=str(x),
                                 limits=1.05,
                                 #used to be set on 0.3
                                 scatter_alpha=0.5,
                                 annotationalpha=1,
                                 second_center_size=25,
                                 colorindexes=["Plurality", "RunOff", "D21+", "D21-", "Approval", "Maj_Judge3", "Maj_Judge5", "Maj_Judge10", "Borda", "Range3", "Range5", "Range10", "c", "Condorcet", "Max U"])
        print(x)
        doit.scatteronly()
        doit.jarvisfun()
        doit.centers_candidates()
        doit.saveit()
        x += 1
        print(x)


def analyze_scenario_2():
    allbyall_comp()
    """allbyall_comp_con()"""


if __name__ == '__main__':
    print("starting analysis")

    analyze_scenario_2()

    print("analysis finished")

