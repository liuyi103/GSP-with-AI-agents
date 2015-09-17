__author__ = 'lyc'

from candidate import GSPCandidate
import unittest
import copy

def snapshot(candidates):
    '''
    :param candidates: list of GSPCandidate
    :return:  a copy of these candidates
    '''
    return copy.deepcopy(candidates)

class TestAuctionUtil(unittest.TestCase):
    '''
    Test whether the snapshot works well.
    '''
    def test_snapshot(self):
        candidates = [GSPCandidate() for i in range(2)]
        candidates_copy = snapshot(candidates)
        original_bid = candidates[0]['bid']
        candidates[0]['bid'] = 10
        self.assertEqual(candidates_copy[0]['bid'], original_bid)
        print candidates_copy[0]['bid']
        print candidates[0]['bid']

if __name__ == '__main__':
    unittest.main()