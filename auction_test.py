__author__ = 'lyc'

from auction import Auction, GSPAuction, VideoPodAuction
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

        winners = VideoPodAuction(candidates, n_winners, max_duration).GetWinners()

        self.assertEqual(len(winners), 2)
        self.assertEqual(set([winner['bid'] for winner in winners]), set([5, 3]), msg = "wrong initial bid")

if __name__ == '__main__':
    unittest.main()