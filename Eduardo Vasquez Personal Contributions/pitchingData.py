import csv
import argparse
import matplotlib.pyplot as plt

# parser = argparse.ArgumentParser()
# parser.add_argument("print", help = "print the AutoMPGData")
# args = parser.parse_args()


class BaseballPitcher:
    def __init__(self, player_id, birthState, teamID, era):
        self.player_id = str(player_id)
        self.birthState = str(birthState)
        self.teamID = str(teamID)
        self.era = float(era)

    def __repr__(self):
        return(f'{self.__class__.__name__}('
        f'{self.player_id!r},{self.birthState!r}, {self.teamID!r}, {self.era!r})')

    def __str__(self):
        return '%s %s %s %s' %(self.player_id, self.birthState, self.teamID, self.era)

    def __eq__(self, other):
        if type(self) == type(other):
            return (self.player_id, self.birthState, self.teamID, self.era) == (other.player_id, other.birthState, other.teamID, other.era)
        else:
            return NotImplemented

    def __lt__(self, other):
        if type(self) == type(other):
            return (self.player_id, self.birthState, self.teamID, self.era) < (other.player_id, other.birthState, other.teamID, other.era)
        else:
            return NotImplemented

class PitchingData:

    def __init__(self):
        self._load_and_clean_data()
        self._make_StateERA_dict()


    def __iter__(self):
        return iter(self.data)

    def _load_and_clean_data(self):
        data = []
        player_idDict = {}
        playerStateDict = {}

        #Filters out non US-born players and creates a dictionary for player_ids
        with open('data/People.txt', newline ='') as players:
            playerData = csv.reader(players, delimiter = ',', skipinitialspace = True)

            for row in playerData:
                if row[4] != "USA":
                    continue
                else:
                    player_idDict.update([ (row[0], row[13] + ' ' + row[14]) ])
                    playerStateDict.update([ (row[0], row[5]) ])

        with open('data/Pitching.txt', newline ='') as pitching:
            pitchingData = csv.reader(pitching, delimiter = ',', skipinitialspace = True)

            for row in pitchingData:
                #filters out entries with no ERA entered, 0 era, or players not in the US #filters players with fewer than 10 games played#filters players who did not pitch in the 2010s
                if (row[19] == '' or row[19] == "ERA" or row[0] not in player_idDict.keys() or row[19] == 0.0 or
                int(row[7]) < 10 or row[1] not in ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]):
                    continue
                else:
                    data.append(BaseballPitcher(player_id = row[0], birthState = playerStateDict[row[0]], teamID = row[3], era = row[19]))
        self.data = data

    def _make_StateERA_dict(self):
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
            makeDict[row.birthState] += row.era
            makeCountDict[row.birthState] += 1

        for k in makeDict:
            makeDict[k] = round(makeDict[k]/makeCountDict[k], 2)
        self.state_era_avg = makeDict

def main():

    pitching_data = PitchingData()
    x, y = zip(*sorted(pitching_data.state_era_avg.items()))
    plt.scatter(x, y)
    plt.xticks(x, x, rotation = "vertical")
    plt.vlines(x,ymin = 1, ymax = y)
    plt.suptitle("Average Earned-Run-Average (ERA) by Player Birth State")
    plt.show()


if __name__ == '__main__':
    main()
