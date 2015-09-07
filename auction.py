# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 14:26:10 2015

@author: lyc
"""

from winner import GSPWinner
from candidate import GSPCandidate

class Auction:
    ''' 
    This is the base class for auctions.
    Given candidates, output winners.
    '''
    def __init__(self, candidates = []):
        self.candidates = candidates
        self.winners = []
        

class GSPAuction(Auction):
    '''
    This is the most fundamental GSP auction.
    Given the number of winners: n_winners
    1. rank candidates by bid * quality_score
    2. select the top n_winners as winners.
    3. the price of each winner is bid' * quality_score' / quality_score,
       where bid' and quality_score' are for the next candidate.
    '''
    def __init__(self, candidates = [], n_winners = 1):
        Auction.__init__(self, candidates)
        self.n_winners = min(n_winners, len(candidates))
        self.candidates = sorted(self.candidates,\
            key = lambda x: -x['bid'] * x['quality_score'])
        
    def GetWinners(self, extended = False):
        '''
        Attention:
        The last one in the returned winners is not a winner
        if extended is True
        '''
        # Avoid all winners case.
        self.candidates.append(GSPCandidate(0, 0))
        self.candidates.append(GSPCandidate(0, 0))
        for i in range(self.n_winners):
            self.winners.append(GSPWinner(\
                self.candidates[i],\
                self.candidates[i + 1]['quality_score'] *\
                self.candidates[i + 1]['bid']/\
                self.candidates[i]['quality_score']))
                
        ret_winners = self.winners +\
            ([self.candidates[self.n_winners]] if extended else [])
        # remove the additional candidate
        self.candidates = self.candidates[:-2]
        return ret_winners
        
    