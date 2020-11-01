# Peter Strimbu - individual portion
# CS3006 Final Project

import csv
import os.path
import logging
import requests
from collections import namedtuple

# create logger
logger = logging.getLogger()
# set the minimum logging level for the logger.  handlers will not go below this level no matter what.
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M'

# create file handler
fh = logging.FileHandler(os.path.join('logs', 'salary.log'), mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

# playerID,birthYear,birthMonth,birthDay,birthCountry,birthState,birthCity,deathYear,deathMonth,deathDay,deathCountry,deathState,deathCity,nameFirst,nameLast,nameGiven,weight,height,bats,throws,debut,finalGame,retroID,bbrefID
Record = namedtuple('Record', 'yearID teamID lgID playerID salary')


class Salary:
    """
    represents the attributes that are available for each record in the data set
    """
    def __init__(self, player_id, team, league, year, salary):
        """
        Constructor. Initializes attributes.
        :param player_id: String.
        :param team: String.
        :param league: String.
        :param year: String.
        :param salary: String.
        """
        if salary == '':
            birth_year = '0'
        self.player_id = player_id
        self.team = team
        self.league = league
        self.year = int(year)
        self.salary = int(salary)
        self.logger = logging.getLogger('Salary')
        self.logger.debug('init: ' + str(self))

    def __repr__(self):
        """
        :return: String: the string representation of the object
        """
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        return f"'{self.player_id}', '{self.team}', '{self.league}', '{self.year}', {self.salary}"

    def __eq__(self, other):
        """
        Implements equality comparison between two Salary objects, using player_id
        :return: Bool: True if equal, False otherwise
        """
        return self.player_id == other.player_id and self.year == other.year and self.team == other.team

    def __lt__(self, other):
        """
        Implements less-than comparison between two Salary objects by salary
        :return: Bool: True if less, False otherwise
        """
        if self.salary < other.salary:
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
        hash_value = hash(self.player_id) + hash(self.team) + hash(self.year)
        self.logger.debug('hash: ' + str(hash_value))
        return hash_value


class SalaryData:
    """
    container for the Salary data set.
    """
    data = []

    def __init__(self, _data=None):
        """
        Constructor. Initializes attributes.
        :param _data:
        """
        self.logger = logging.getLogger('SalaryData')
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
        Method that will read the salary file and instantiate Salary objects and add them to the data attribute.
        :return: none
        """
        # if the baseball salary file doesn't yet exist, have the _read_salary_data() method create it
        if not os.path.exists(os.path.join('data', 'baseball.salary.csv')):
            self.logger.info('baseball.salary.csv file doesnt exist; need to get it.')
            self._get_salary_data()

        self.logger.info('reading baseball.salary.csv')
        self.data = []
        with open(os.path.join('data', 'baseball.salary.csv')) as salary_file:
            # skip the header row
            next(salary_file)
            reader = csv.reader(salary_file, delimiter=',')
            for row in reader:
                record = Record(*row)
                salary = Salary(record.playerID, record.teamID, record.lgID, record.yearID, record.salary)
                self.data.append(salary)

    def _get_salary_data(self):
        """
        downloads the salary data file and saves it in a local file named "salary.data.txt"
        """
        self.logger.info('downloading salary data')
        response = requests.get('https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Salaries.csv')

        if response.status_code == 200:
            self.logger.info('writing baseball.salary.csv')
            with open(os.path.join('data', 'baseball.salary.csv'), 'w') as salary_data_file:
                salary_data_file.write(response.text)
            self.logger.info('finished writing baseball.salary.csv')
        else:
            self.logger.critical('could not get salary data')
            raise Exception('could not get salary data')

    def sort_by_default(self) -> None:
        """
        Sorts the data list in place by: player_id, birth_state, birth_year.
        """
        self.logger.info('sorting the list by year, league, team, player')
        self.data.sort()

    def sort_by_salary(self) -> None:
        """
        Sorts the data list in place by: salary.
        """
        self.logger.info('sorting the list by salary')
        self.data.sort(key=lambda x: [x.salary])


def main():
    logger.info('starting salary.py')

    salary_data = SalaryData()

    logger.info('finished salary.py')


# if not importing, call main
if __name__ == '__main__':
    main()
