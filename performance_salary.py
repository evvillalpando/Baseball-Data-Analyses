# Peter Strimbu - Eduardo Vasquez-Villalpando Joint Analysis
# CS3006 Final Project

# uses individual files player (Peter), salary (Peter), hittingData (Eduardo), and pitchingData (Eduardo)
# creates new joint analysis of salary by hitting performance data

import os.path
import logging
import numpy as np
import matplotlib.pyplot as plt
from player import PlayerData
from salary import SalaryData
from hittingData import HittingData
from pitchingData import PitchingData

# create logger
logger = logging.getLogger()
# set the minimum logging level for the logger.  handlers will not go below this level no matter what.
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M'

# create file handler
fh = logging.FileHandler(os.path.join('logs', 'performance_salary.log'), mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)


# def graph_bats_by_year(self) -> None:
#     logger.info('creating bats_by_year graph')
#
#     player_dict = {}
#
#     for player in self.data:
#         if player.bats != "" and player.birth_year > 0:
#             if player.birth_year not in player_dict:
#                 player_dict[player.birth_year] = []
#             if player.bats == "L":
#                 player_dict[player.birth_year].append(0)
#             if player.bats == "R":
#                 player_dict[player.birth_year].append(1)
#
#     x = []
#     y = []
#
#     for k, v in sorted(player_dict.items()):
#         # eliminate the extreme values
#         if np.average(player_dict[k]) < 1 and np.average(player_dict[k]) > 0:
#             x.append(k)
#             y.append(np.average(player_dict[k]))
#
#     fig, ax = plt.subplots()
#
#     # Plot the average line
#     ax.plot(x, y, color='Red', label='Left = 0, Right = 1', linestyle='-')
#
#     # Make a legend
#     ax.legend(loc='lower right')
#
#     plt.title("Bats Left/Right by Birth Year")
#     plt.xlabel("Birth Year")
#     plt.ylabel("AVG Bats Left/Right")
#     plt.show()


def main():
    logger.info('starting performance_salary.py')

    player_data = PlayerData()
    salary_data = SalaryData()
    hitting_data = HittingData()
    pitching_data = PitchingData()

    player_salary_hitting = []
    for player in player_data:

        # join salary data to player dict
        player_salary = [p for p in salary_data if p.player_id == player.player_id]

        # join hitting data to player dict
        player_hitting = [p for p in hitting_data if p.player_id == player.player_id]

        # iterate over players to create salary vs batting data
        # only join data if both sources exist
        if len(player_salary) > 0 and len(player_hitting) > 0:
            max_salary = int(max(i.salary for i in player_salary) / 1000)
            batting_avg = int(sum(i.battingAvg for i in player_hitting) / len(player_hitting) * 1000)
            player_salary_hitting.append((batting_avg, max_salary))

            # limit to 100 entries for speed
            if len(player_salary_hitting) == 100:
                break

    plt.scatter(*zip(*player_salary_hitting))

    # # fig, ax = plt.subplots()
    # #
    # # # Plot the average line
    # # ax.plot(x_mean, y_mean, color='Red', label='Avg Height', linestyle='--')
    #
    # # Make a legend
    # ax.legend(loc='lower right')
    #
    # plt.scatter(x, y, alpha=0.05)

    plt.title("Max Salary vs. Batting Avg")
    plt.xlabel("Batting Avg")
    plt.ylabel("Max Salary (in thousands)")
    plt.show()

    logger.info('finished performance_salary.py')

    #Plot #2 showing salary by earned-run average
    player_salary_pitching = []
    for player in player_data:
        # join salary data to player dict
        player_salary = [p for p in salary_data if p.player_id == player.player_id]

        # join hitting data to player dict
        player_pitching = [p for p in pitching_data if p.player_id == player.player_id]

        # iterate over players to create salary vs batting data
        # only join data if both sources exist
        if len(player_salary) > 0 and len(player_pitching) > 0:
            max_salary = int(max(i.salary for i in player_salary) / 1000)
            era = float(sum(i.era for i in player_pitching) / len(player_pitching))
            player_salary_pitching.append((era, max_salary))

            # limit to 100 entries for speed
            if len(player_salary_pitching) == 100:
                break
    #Plot #2
    plt.scatter(*zip(*player_salary_pitching))
    plt.xlabel("Earned Run Average (ERA)")
    plt.ylabel("Max Salary (in thousands)")
    plt.show()

    #Plot #3 showing average pitcher salary by teams in the 2010s—combines data from pitching_data and salary_data
    team_pitching_salary = {'CHN': 0, 'TEX': 0, 'BAL': 0, 'SLN': 0, 'FLO': 0, 'PIT': 0, 'SEA': 0,
    'HOU': 0, 'SDN': 0, 'BOS': 0, 'NYA': 0, 'NYN': 0, 'COL': 0, 'DET': 0, 'MIN': 0, 'TOR': 0, 'ARI': 0, 'ATL': 0,
    'CHA': 0, 'MON': 0, 'ANA': 0, 'CLE': 0, 'KCA': 0, 'OAK': 0, 'PHI': 0, 'SFN': 0, 'MIL': 0,
    'TBA': 0, 'CIN': 0, 'LAN': 0, 'LAA': 0, 'WAS': 0, 'MIA': 0}
    count_dict = {'CHN': 0, 'TEX': 0, 'BAL': 0, 'SLN': 0, 'FLO': 0, 'PIT': 0, 'SEA': 0,
    'HOU': 0, 'SDN': 0, 'BOS': 0, 'NYA': 0, 'NYN': 0, 'COL': 0, 'DET': 0, 'MIN': 0, 'TOR': 0, 'ARI': 0, 'ATL': 0,
    'CHA': 0, 'MON': 0, 'ANA': 0, 'CLE': 0, 'KCA': 0, 'OAK': 0, 'PHI': 0, 'SFN': 0, 'MIL': 0,
    'TBA': 0, 'CIN': 0, 'LAN': 0, 'LAA': 0, 'WAS': 0, 'MIA': 0}

    for player in salary_data:
        if player.player_id in [row.player_id for row in pitching_data]:
            team_pitching_salary[player.team] += player.salary
            count_dict[player.team] += 1
    for k in team_pitching_salary:
        team_pitching_salary[k] = (team_pitching_salary[k] // count_dict[k]) / 1000
    #Plot #3
    x, y = zip(*sorted(team_pitching_salary.items()))
    plt.bar(x,y)
    plt.xlabel("Team Abbreviations")
    plt.ylabel("Avg. Pitcher Salary (in thousands)")
    plt.xticks(x, x, rotation = "vertical")
    plt.suptitle("Average Salary of each MLB Team's Pitchers")
    plt.show()

# if not importing, call main
if __name__ == '__main__':
    main()
