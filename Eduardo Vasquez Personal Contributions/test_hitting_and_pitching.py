import unittest
from pitchingData import BaseballPitcher
from pitchingData import PitchingData
from hittingData import HittingData
from hittingData import BaseballBatter

pitching_data = PitchingData()
class test_pitching_data(unittest.TestCase):
    #Every single one should return true
    def test1(self):
        self.assertIn(BaseballPitcher("yateski01", "HI", "SDN", "1.19"), pitching_data)

    def test2(self):
        self.assertIn(BaseballPitcher("kershcl01", "TX", "LAN", "2.91"), pitching_data)

    def test3(self):
        #Randy Johnson did not pitch in the 2010s (retired in 2009)
        self.assertNotIn(BaseballPitcher("johnsra05", "CA", "SEA", "3.98"), pitching_data)

    def test4(self):
        #Mariano Rivera was not born in the US
        self.assertNotIn(BaseballPitcher("riverma01", "Panama", "NYA", "2.16"), pitching_data)

hitting_data = HittingData()
class test_hitting_data(unittest.TestCase):
    #Every single one should return true
    def test1(self):
        self.assertIn(BaseballBatter("troutmi01", "NJ", "LAA", ".291", "OF"), hitting_data)

    def test2(self):
        #Clayton Kershaw is a pitcher, so should not be in the data
        self.assertNotIn(BaseballBatter("kershcl01","TEX", "LAN", ".207", "P"), hitting_data)

    def test3(self):
        #Hideki Matsui was not born in the US
        self.assertNotIn(BaseballBatter("matsuhi01", "Ishikawa", "NYA", ".287", "OF"), hitting_data)



if __name__ == '__main__':
    unittest.main()
