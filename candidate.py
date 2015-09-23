# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 14:13:54 2015

@author: lyc
"""
import random
from strategy import GSP_TruthfulStrategy, GSP_BestResponseStrategy, GetBid

candidate_id = 0

class AuctionCandidate:
    ''' This is the base class for an auction candidate.'''
    def __init__(self, bid = random.random()):
        global candidate_id
        self.bid = bid
        self.id = candidate_id
        candidate_id += 1

    def __getitem__(self, key):
        value = 'something'
        exec 'value = self.' + key
        return value

    def __setitem__(self, key, value):
        exec 'self.%s = %s' % (key, str(value))

class GSPCandidate(AuctionCandidate):
    ''' 
    The candidate for GSP auction, with quality score.
    Specially, the strategy needs to be set after init function.
    '''
    def __init__(self, bid = random.random(), quality_score = 1,\
        value = 0):
        AuctionCandidate.__init__(self, bid)
        self.quality_score = quality_score
        self.value = value
        self.strategy = 'GSP_TruthfulStrategy'
        self.bid_history = []
    
    def GetNewBid(self):
        #  The small residual is for tie-breaking.
        self.bid = round(self.strategy.GetBid(), 3) + self.id * 1e-6
        self.bid_history.append(self.bid)


class VideoPodCandidate(AuctionCandidate):
    '''
    candidate for video pod auction.
    '''
    def __init__(self, bid = random.random(), duration = 15):
        AuctionCandidate.__init__(self, bid)
        self.duration = duration


if __name__ == '__main__':
    candidate = GSPCandidate()
    candidate['temp'] = 0
    print candidate['bid'], candidate['quality_score'], candidate['temp']