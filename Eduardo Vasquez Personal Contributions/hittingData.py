import csv
from collections import namedtuple
import argparse
import matplotlib.pyplot as plt


# parser = argparse.ArgumentParser()
# parser.add_argument("print", help = "print the hitting data")
# parser.add_argument('-p','--plot', action = 'store', default = None, type = str, choices = ['bypos',  'bystate'])
# args = parser.parse_args()


class BaseballBatter:
    def __init__(self, player_id, birthState, teamID, battingAvg, position):
        self.player_id = str(player_id)
        self.birthState = str(birthState)
        self.teamID = str(teamID)
        self.battingAvg = float(battingAvg)
        self.position = str(position)

    def __repr__(self):
        return(f'{self.__class__.__name__}('
        f'{self.player_id!r},{self.birthState!r}, {self.teamID!r}, {self.battingAvg!r}, {self.position!r})')

    def __str__(self):
        return '%s %s %s %s' %(self.player_id, self.birthState, self.teamID, self.battingAvg, self.position)

    def __eq__(self, other):
        if type(self) == type(other):
            return (self.player_id, self.birthState, self.teamID, self.battingAvg, self.position) == (other.player_id, other.birthState, other.teamID, other.battingAvg, other.position)
        else:
            return NotImplemented

    def __lt__(self, other):
        if type(self) == type(other):
            return (self.player_id, self.birthState, self.teamID, self.battingAvg, self.position) < (other.player_id, other.birthState, other.teamID, other.battingAvg, other.position)
        else:
            return NotImplemented

class HittingData:

    def __init__(self):
        self._load_and_clean_data()
        self._make_StatebattingAvg_dict()
        self._make_AvgByPosition_dict()

    def __iter__(self):
        return iter(self.data)

    def _load_and_clean_data(self):
        data = []
        player_idDict = {}
        playerStateDict = {}
        playerPositionDict = {}

        #Filters out Pitchers, whom aren't expected to be good hitters, and American League pitchers don't hit unless playing interleague games.
        with open('data/Fielding.txt', newline ='') as playerPositions:
            positionData = csv.reader(playerPositions, delimiter = ',', skipinitialspace = True)
            for row in positionData:
                if row[5] == "P":
                    continue
                else:
                    playerPositionDict.update([ (row[0], row[5]) ])

        #Filters out non US-born players and creates a dictionary to allow for linking a player_id to a player's full name
        with open('data/People.txt', newline ='') as players:
            playerData = csv.reader(players, delimiter = ',', skipinitialspace = True)

            for row in playerData:
                if row[4] != "USA":
                    continue
                else:
                    player_idDict.update([ (row[0], row[13] + ' ' + row[14]) ])
                    playerStateDict.update([ (row[0], row[5]) ])

        with open('data/Batting.txt', newline ='') as batting:
            battingData = csv.reader(batting, delimiter = ',', skipinitialspace = True)
            for row in battingData:

                #filters out entries with less than 100 At Bats
                if row[6] <= '100' or row[0] not in player_idDict.keys() or row[0] not in playerPositionDict.keys():
                    continue
                else:
                    data.append(BaseballBatter(row[0], birthState = playerStateDict[row[0]],
                    teamID = row[3], battingAvg = round(float(row[8])/float(row[6]), 3), position = playerPositionDict[row[0]]))
        self.data = data

    def _make_StatebattingAvg_dict(self):
        states = []
        makeDict = {}
        makeCountDict = {}
        for row in self.data:
            if row.birthState not in states:
                states.append(row.birthState)

        for state in states:
            makeDict[state] = 0
            makeCountDict[state] = 0

        for row in self.data:
            makeDict[row.birthState] += row.battingAvg
            makeCountDict[row.birthState] += 1

        for k in makeDict:
            makeDict[k] = round(makeDict[k]/makeCountDict[k], 3)
        self.state_batting_avg = makeDict

    def _make_AvgByPosition_dict(self):
        positions = []
        makeDict = {}
        makeCountDict = {}
        for row in self.data:
            if row.position not in positions:
                positions.append(row.position)

        for position in positions:
            makeDict[position] = 0
            makeCountDict[position] = 0

        for row in self.data:
            makeDict[row.position] += row.battingAvg
            makeCountDict[row.position] += 1

        for k in makeDict:
            makeDict[k] = round(makeDict[k]/makeCountDict[k], 3)
        self.batting_avg_by_position = makeDict

def main():
    hitting_data = HittingData()
    # if args.plot == "bystate":
    x, y = zip(*sorted(hitting_data.state_batting_avg.items()))
    plt.scatter(x, y)
    plt.xticks(x, x, rotation = "vertical")
    plt.vlines(x, ymin = 0, ymax = y)
    plt.suptitle("Batting Average by Player Birth State (Excluding Pitchers and Players < 100 At-Bats)")
    plt.show()

    # if args.plot == "bypos":
    x, y = zip(*sorted(hitting_data.batting_avg_by_position.items()))
    plt.bar(x, y)
    plt.xticks(x, x, rotation = "vertical")
    plt.suptitle("Batting Average by Player Position (Excluding Pitchers and Players < 100 At-Bats)")
    plt.show()

# if not importing, call main
if __name__ == '__main__':
    main()
