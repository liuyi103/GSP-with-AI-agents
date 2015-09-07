# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 15:14:24 2015

@author: lyc
"""

k_epsilon = 1e-2
class GSP_Strategy:
    '''
    The class for the strategies that are used in GSP auction.
    Strategy is assigned to a candidate by main, because only main can
    get access to all winners.
    '''
    def __init__(self, value_profile, me = ['candidate'] , winners = []):
        self.value_profile = value_profile
        self.me = me
        self.winners = winners

class GSP_TruthfulStrategy(GSP_Strategy):
    ''' report the true top value. '''
    def __init__(self, value_profile):
        GSP_Strategy.__init__(self, value_profile)
    
    def GetBid(self):
        return self.value_profile[0]

class GSP_BestResponseStrategy(GSP_Strategy):
    ''' 
    Try each winning position, the find the best one of them.
    '''
    def __init__(self, value_profile, me, extended_winners):
        GSP_Strategy.__init__(self, value_profile, me, extended_winners)
        
    def GetBid(self):
        prices = []
        self_appear = False
        for k, winner in enumerate(self.winners):
            if winner['id'] != self.me['id']:
                prices.append(winner['bid'] * winner['quality_score'] /\
                    self.me['quality_score'])
            else:
                self_appear = True
        # remove the last one (extended)
        if not self_appear:
            prices = prices[:-1]
        rank_price = zip(range(len(prices)), prices)
        choice = max(rank_price,\
            key = lambda x: self.value_profile[x[0]] - x[1])
        if self.value_profile[choice[0]] - choice[1] < 0:
            return 0
        return choice[1] + k_epsilon
        
        
            
            
    