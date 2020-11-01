# Peter Strimbu - individual portion
# CS3006 Final Project

import csv
import os.path
import logging
import requests
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

# create logger
logger = logging.getLogger()
# set the minimum logging level for the logger.  handlers will not go below this level no matter what.
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M'

# create file handler
fh = logging.FileHandler(os.path.join('logs', 'person.log'), mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

# playerID,birthYear,birthMonth,birthDay,birthCountry,birthState,birthCity,deathYear,deathMonth,deathDay,deathCountry,deathState,deathCity,nameFirst,nameLast,nameGiven,weight,height,bats,throws,debut,finalGame,retroID,bbrefID
Record = namedtuple('Record', 'playerID birthYear birthMonth birthDay birthCountry birthState birthCity deathYear deathMonth deathDay deathCountry deathState deathCity nameFirst nameLast nameGiven weight height bats throws debut finalGame retroID bbrefID')


class Player:
    """
    represents the attributes that are available for each record in the data set
    """
    def __init__(self, player_id, first_name, last_name, birth_state, birth_year, height, weight, bats, throws):
        """
        Constructor. Initializes attributes.
        :param player_id: String. 
        :param first_name: String.
        :param last_name: String.
        :param birth_state: String.
        :param birth_year: Integer.
        :param height: String.
        :param weight: String.
        :param bats: String.
        :param throws: String.
        """
        if height == '' or int(height) < 60:
            height = '0'
        if weight == '':
            weight = '0'
        if birth_year == '':
            birth_year = '0'
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_state = birth_state
        self.birth_year = int(birth_year)
        self.height = int(height)
        self.weight = int(weight)
        self.bats = bats
        self.throws = throws
        self.logger = logging.getLogger('Player')

        self.logger.debug('init: ' + str(self))

    def __repr__(self):
        """
        :return: String: the string representation of the object
        """
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        return f"'{self.player_id}', '{self.first_name}', '{self.last_name}', '{self.birth_state}', {self.birth_year}"

    def __eq__(self, other):
        """
        Implements equality comparison between two Player objects, using player_id
        :return: Bool: True if equal, False otherwise
        """
        return self.player_id == other.player_id

    def __lt__(self, other):
        """
        Implements less-than comparison between two Player objects by last_name and first_name
        :return: Bool: True if less, False otherwise
        """
        if self.last_name < other.last_name and self.first_name < other.first_name:
            return True
        return False

    # def __setitem__(self, floor_number, data):
    #     self._floors[floor_number] = data
    #
    # def __getitem__(self, floor_number):
    #     return self._floors[floor_number]

    def __hash__(self):
        """
        returns a hash representing the attributes
        :return: String: the hash
        """
        hash_value = hash(self.player_id)
        self.logger.debug('hash: ' + str(hash_value))
        return hash_value


class PlayerData:
    """
    container the Player data set.
    """
    data = []

    def __init__(self, _data=None):
        """
        Constructor. Initializes attributes.
        :param _data:
        """
        self.logger = logging.getLogger('PlayerData')
        if _data is None:
            self.logger.info('loading data')
            self._load_data()
        else:
            self.logger.info('data already loaded, skipping data load')
            self.data = _data

    def __iter__(self):
        """
        iterates over loaded data set
        :return:
        """
        for x in self.data:
            yield x

    def _load_data(self):
        """
        Method that will read the person file and instantiate Player objects and add them to the data attribute.
        :return: none
        """
        # if the baseball person file doesn't yet exist, have the _read_person_data() method create it
        if not os.path.exists(os.path.join('data', 'baseball.person.csv')):
            self.logger.info('baseball.person.csv file doesnt exist; need to get it.')
            self._get_person_data()

        self.logger.info('reading baseball.person.csv')
        self.data = []
        with open(os.path.join('data', 'baseball.person.csv')) as person_file:
            # skip the header row
            next(person_file)
            reader = csv.reader(person_file, delimiter=',')
            for row in reader:
                record = Record(*row)
                person = Player(record.playerID, record.nameFirst, record.nameLast, record.birthState, record.birthYear, record.height, record.weight, record.bats, record.throws)
                # eliminate data before 1850.. not enough records to get averages
                if person.birth_year >= 1850:
                    self.data.append(person)

    def _get_person_data(self):
        """
        downloads the person data file and saves it in a local file named "person.data.txt"
        """
        self.logger.info('downloading person data')
        response = requests.get('https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/People.csv')

        if response.status_code == 200:
            self.logger.info('writing baseball.person.csv')
            with open(os.path.join('data', 'baseball.person.csv'), 'w') as person_data_file:
                person_data_file.write(response.text)
            self.logger.info('finished writing baseball.person.csv')
        else:
            self.logger.critical('could not get person data')
            raise Exception('could not get person data')

    def sort_by_default(self) -> None:
        """
        Sorts the data list in place by: player_id, birth_state, birth_year.
        """
        self.logger.info('sorting the list by (player_id), birth_state, birth_year')
        self.data.sort()

    def sort_by_birth_state(self) -> None:
        """
        Sorts the data list in place by: birth_state, birth_year.
        """
        self.logger.info('sorting the list by (birth_state), birth_year')
        self.data.sort(key=lambda x: [x.birth_state, x.birth_year])

    def sort_by_birth_year(self) -> None:
        """
        Sorts the data list in place by: birth_year, birth_state.
        """
        self.logger.info('sorting the list by (birth_year), birth_state')
        self.data.sort(key=lambda x: [x.birth_year, x.birth_state])

    def graph_player_height_by_birth_year(self) -> None:
        logger.info('creating player_height_by_birth_year graph')

        x = []
        y = []

        year_height_dict = {}

        for player in self.data:
            if player.birth_year > 0 and player.height > 0:
                x.append(player.birth_year)
                y.append(player.height)

                if player.birth_year not in year_height_dict:
                    year_height_dict[player.birth_year] = []
                year_height_dict[player.birth_year].append(player.height)

        x_mean = []
        y_mean = []
        for k, v in sorted(year_height_dict.items()):
            x_mean.append(k)
            y_mean.append(np.average(year_height_dict[k]))

        fig, ax = plt.subplots()

        # Plot the average line
        ax.plot(x_mean, y_mean, color='Red', label='Avg Height', linestyle='--')

        # Make a legend
        ax.legend(loc='lower right')

        plt.scatter(x, y, alpha=0.05)

        plt.title("Player Height by Birth Year")
        plt.xlabel("Birth Year")
        plt.ylabel("Height (inches)")
        plt.show()

    def graph_bats_by_year(self) -> None:
        logger.info('creating bats_by_year graph')

        player_dict = {}

        for player in self.data:
            if player.bats != "" and player.birth_year > 0:
                if player.birth_year not in player_dict:
                    player_dict[player.birth_year] = []
                if player.bats == "L":
                    player_dict[player.birth_year].append(0)
                if player.bats == "R":
                    player_dict[player.birth_year].append(1)

        x = []
        y = []

        for k, v in sorted(player_dict.items()):
            # eliminate the extreme values
            if np.average(player_dict[k]) < 1 and np.average(player_dict[k]) > 0:
                x.append(k)
                y.append(np.average(player_dict[k]))

        fig, ax = plt.subplots()

        # Plot the average line
        ax.plot(x, y, color='Red', label='Left = 0, Right = 1', linestyle='-')

        # Make a legend
        ax.legend(loc='lower right')

        plt.title("Bats Left/Right by Birth Year")
        plt.xlabel("Birth Year")
        plt.ylabel("AVG Bats Left/Right")
        plt.show()

    def graph_throws_by_year(self) -> None:
        logger.info('creating throws_by_year graph')

        player_dict = {}

        for player in self.data:
            if player.throws != "" and player.birth_year > 0:
                if player.birth_year not in player_dict:
                    player_dict[player.birth_year] = []
                if player.throws == "L":
                    player_dict[player.birth_year].append(0)
                if player.throws == "R":
                    player_dict[player.birth_year].append(1)

        x = []
        y = []

        for k, v in sorted(player_dict.items()):
            # eliminate the extreme values
            if np.average(player_dict[k]) < 1 and np.average(player_dict[k]) > 0:
                x.append(k)
                y.append(np.average(player_dict[k]))

        fig, ax = plt.subplots()

        # Plot the average line
        ax.plot(x, y, color='Red', label='Left = 0, Right = 1', linestyle='-')

        # Make a legend
        ax.legend(loc='lower right')

        plt.title("Throws Left/Right by Birth Year")
        plt.xlabel("Birth Year")
        plt.ylabel("AVG Throws Left/Right")
        plt.show()


def main():
    logger.info('starting player.py')

    person_data = PlayerData()
    person_data.graph_player_height_by_birth_year()
    person_data.graph_bats_by_year()
    person_data.graph_throws_by_year()

    logger.info('finished player.py')


# if not importing, call main
if __name__ == '__main__':
    main()
