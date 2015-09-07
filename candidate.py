# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 14:13:54 2015

@author: lyc
"""
import random
from strategy import GSP_TruthfulStrategy, GSP_BestResponseStrategy

candidate_id = 0

class AuctionCandidate:
    ''' This is the base class for an auction candidate.'''
    def __init__(self, bid = random.random()):
        global candidate_id
        self.bid = bid
        self.id = candidate_id
        candidate_id += 1

class GSPCandidate(AuctionCandidate):
    ''' 
    The candidate for GSP auction, with quality score.
    Specially, the strategy needs to be set after init function.
    '''
    def __init__(self, bid = random.random(), quality_score = 1,\
        value_profile = []):
        AuctionCandidate.__init__(self, bid)
        self.quality_score = quality_score
        self.value_profile = value_profile
        self.strategy = GSP_TruthfulStrategy(value_profile)
    
    def GetNewBid(self):
        self.bid = self.strategy.GetBid()

    def __getitem__(self, key):
        exec 'value = self.' + key
        return value
    
    def __setitem__(self, key, value):
        exec 'self.%s = %s' % (key, str(value))

if __name__ == '__main__':
    candidate = GSPCandidate()
    candidate['temp'] = 0
    print candidate['bid'], candidate['quality_score'], candidate['temp']