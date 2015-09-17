__author__ = 'lyc'

from auction import Auction, GSPAuction
from candidate import GSPCandidate
from strategy import GSP_BestResponseStrategy
import unittest
import copy


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

        candidates_copy = copy.deepcopy(candidates)
        for candidate in candidates:
            candidate.strategy = GSP_BestResponseStrategy(candidate, candidates_copy, ctrs)
            candidate.GetNewBid()
            print candidate.bid

if __name__ == '__main__':
    unittest.main()