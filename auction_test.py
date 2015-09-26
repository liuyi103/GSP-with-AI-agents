__author__ = 'lyc'

from auction import Auction, GSPAuction, VideoPodAuction, VideoPodVCG, VideoPodGroupAuction
from candidate import GSPCandidate, VideoPodCandidate
import unittest


class TestAuction(unittest.TestCase):
    '''
    This is the unittests for auction.py
    '''
    def test_Auction(self):
        foo = Auction()
        self.assertEqual(foo.candidates, [])
        self.assertEqual(foo.winners, [])

    def test_GSPAuction(self):
        '''
        This is a small test case with 3 candidates.
        '''
        candidate1 = GSPCandidate(value = 10, bid = 5)
        candidate2 = GSPCandidate(value = 9, bid = 4)
        candidate3 = GSPCandidate(value = 8, bid = 3)
        candidates = [candidate1, candidate2, candidate3]
        n_winners = 2
        ctrs = [0.1, 0.05]
        bids = [[],[],[]]

        winners = GSPAuction(candidates, n_winners).GetWinners()

        self.assertEqual(len(winners), 2)
        self.assertEqual(set([winner['bid'] for winner in winners]), set([5, 4]), msg = "wrong initial bid")

    def test_VideoPodAuction(self):
        '''
        This is a test for video pod auction
        '''
        candidate1 = VideoPodCandidate(duration = 10, bid = 5)
        candidate2 = VideoPodCandidate(duration = 9, bid = 4)
        candidate3 = VideoPodCandidate(duration = 8, bid = 3)
        candidates = [candidate1, candidate2, candidate3]
        n_winners = 10
        max_duration = 18

        winners, welfare = VideoPodAuction(candidates, n_winners, max_duration).GetOptimalWinners()

        self.assertEqual(welfare, 8)
        self.assertEqual(len(winners), 2)
        self.assertEqual(set([winner['bid'] for winner in winners]), set([5, 3]), msg = "wrong initial bid")

    def test_VideoPodVCG(self):
        '''
        This is a test for video pod auction
        '''
        candidate1 = VideoPodCandidate(duration = 10, bid = 5)
        candidate2 = VideoPodCandidate(duration = 9, bid = 4)
        candidate3 = VideoPodCandidate(duration = 8, bid = 3)
        candidates = [candidate1, candidate2, candidate3]
        n_winners = 10
        max_duration = 18

        winners, welfare = VideoPodVCG(candidates, n_winners, max_duration).GetWinners()

        self.assertEqual(welfare, 8)
        self.assertEqual(len(winners), 2)
        self.assertEqual(set([winner['bid'] for winner in winners]), set([5, 3]), msg = "wrong initial bid")
        self.assertEqual(set([winner['price'] for winner in winners]), set([0, 4]), msg = "wrong price")

    def test_VideoPodGroup(self):
        candidate1 = VideoPodCandidate(duration = 10, bid = 5)
        candidate2 = VideoPodCandidate(duration = 9, bid = 4)
        candidate3 = VideoPodCandidate(duration = 8, bid = 3)
        candidate4 = VideoPodCandidate(duration = 8, bid = 3)
        candidates = [candidate1, candidate2, candidate3, candidate4]
        n_winners = 10
        max_duration = 18

        winners, welfare = VideoPodGroupAuction(candidates, n_winners, max_duration, 2).GetWinners()

        self.assertEqual(welfare, 8)
        self.assertEqual(len(winners), 2)
        print winners[0]['price'], winners[1]['price']
        self.assertAlmostEqual(max([winner['price'] for winner in winners]), 40./9, msg = "wrong price")
        self.assertAlmostEqual(min([winner['price'] for winner in winners]), 3, msg = "wrong price")

if __name__ == '__main__':
    unittest.main()