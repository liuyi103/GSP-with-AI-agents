__author__ = 'lyc'

import unittest
from strategy import GetBid
from candidate import GSPCandidate

class StrategyTest(unittest.TestCase):
    '''
    Test cases fpr strategy.py
    '''
    def __init__(self, methodName = 'runTest'):
        unittest.TestCase.__init__(self, methodName)
        candidate1 = GSPCandidate(value = 10, bid = 5)
        candidate2 = GSPCandidate(value = 9, bid = 4)
        candidate3 = GSPCandidate(value = 8, bid = 3)
        self.candidates = [candidate1, candidate2, candidate3]
        self.ctrs = [0.1, 0.05]

    def test_TruthfulBid(self):
        self.assertAlmostEqual(GetBid(self.candidates[0], self.candidates, self.ctrs, "GSP_TruthfulStrategy"), 10,\
                               delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[1], self.candidates, self.ctrs, "GSP_TruthfulStrategy"), 9,\
                                delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[2], self.candidates, self.ctrs, "GSP_TruthfulStrategy"), 8,\
                                delta = 1e-4)

    def test_BestResponse(self):
        self.assertAlmostEquals(GetBid(self.candidates[0], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 4.01, delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[1], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 5.01, delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[2], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 5.01, delta = 1e-4)

    def test_SmallStep(self):
        self.assertAlmostEquals(GetBid(self.candidates[0], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 4.9, delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[1], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 4.11, delta = 1e-4)
        self.assertAlmostEquals(GetBid(self.candidates[2], self.candidates, self.ctrs,\
                                       "GSP_BestResponseStrategy"), 3.1, delta = 1e-4)

if __name__ == '__main__':
    unittest.main()

