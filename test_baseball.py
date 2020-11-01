# Peter Strimbu and Eduardo Vasquez
# CS3006 Final

import unittest
from autompg2 import AutoMPG
from autompg2 import AutoMPGData


class TestAutoMPG(unittest.TestCase):

    def test_init(self):
        auto = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        self.assertEqual(auto.make, 'ford')
        self.assertEqual(auto.model, 'mustang gl')
        self.assertEqual(auto.year, 1982)
        self.assertEqual(auto.mpg, 27.0)

    def test_repr(self):
        auto = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        self.assertEqual(repr(auto), "AutoMPG('ford', 'mustang gl', 1982, 27.0)")

    def test_str(self):
        auto = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        self.assertEqual(str(auto), "'ford', 'mustang gl', 1982, 27.0")

    def test_eq(self):
        auto1 = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto2 = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto3 = AutoMPG('ford', 'bustang gl', 1982, 27.0)
        self.assertEqual(auto1, auto2)
        self.assertNotEqual(auto1, auto3)

    def test_lt(self):
        auto1 = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto2 = AutoMPG('ford', 'mustang gl', 1982, 27.1)
        auto3 = AutoMPG('ford', 'bustang gl', 1982, 27.1)
        self.assertLess(auto1, auto2)
        self.assertGreater(auto1, auto3)

    def test_hash(self):
        auto1 = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto2 = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto3 = AutoMPG('ford', 'bustang gl', 1982, 27.0)
        hash1 = hash(auto1)
        hash2 = hash(auto2)
        hash3 = hash(auto3)
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)


class TestAutoMPGData(unittest.TestCase):

    def test_init(self):
        auto = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto_list = list()
        auto_list.append(auto)
        autompgdata = AutoMPGData(auto_list)
        self.assertEqual(auto_list, autompgdata.data)

    def test_iter(self):
        auto = AutoMPG('ford', 'mustang gl', 1982, 27.0)
        auto_list = list()
        auto_list.append(auto)
        autompgdata = AutoMPGData(auto_list)
        for x in autompgdata:
            self.assertEqual(auto, x)

    def test_load_data(self):
        # '18.0' '8' '307.0' '130.0' '3504.' '12.0' '1970' '1' 'chevrolet' 'chevelle malibu'
        auto = AutoMPG('chevrolet', 'chevelle malibu', 1970, 18.0)
        autompgdata = AutoMPGData()  # call loaddata()
        self.assertEqual(auto, autompgdata.data[0])

    # testing _clean_data is unnecessary, as it is embedded in test_load_data


if __name__ == '__main__':
    unittest.main()
