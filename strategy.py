# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 15:14:24 2015

@author: lyc
"""
import numpy as np
import bisect

k_epsilon = 1e-2
k_step = 1e-1
n_samples = 100

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
    
    def __init__(self, me, extended_winners):
        GSP_Strategy.__init__(self, me.value_profile, me, extended_winners)
        
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
        # individually rational
        if self.value_profile[choice[0]] - choice[1] < 0:
            return 0
        return choice[1] + k_epsilon
        
class GSP_SmallStepStrategy(GSP_Strategy):
    '''
    Each time, one candidate walk a small step to the best response.
    The step length is set to be a fix number which is the k_step.
    '''
    def __init__(self, value_profile, me, extended_winners):
        GSP_Strategy.__init__(self, value_profile, me, extended_winners)
    
    def __init__(self, me, extended_winners):
        GSP_Strategy.__init__(self, me.value_profile, me, extended_winners)
        
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
        # individually rational
        if self.value_profile[choice[0]] - choice[1] < 0:
            return 0
        return self.me['bid'] + k_step if choice[1] > self.me['bid']\
            else max(self.me['bid'] - k_step, 0)
        
class GSP_FictitiousPlayStrategy(GSP_Strategy):
    '''
    This is an approximate implementation of ficitious play strategy.
    Each time when a bidder decides his bid, he will sample 100 times from
    others' bidding history, and select a best solution for the selected 
    bid profiles.
    '''
    def __init__(self, value_profile, me, extended_winners, candidates):
        GSP_Strategy.__init__(self, value_profile, me, extended_winners)
        self.candidates = candidates
    
    def __init__(self, me, extended_winners, candidates):
        GSP_Strategy.__init__(self, me.value_profile, me, extended_winners)
        self.candidates = candidates
        
    def GetBid(self):
        n_winners = len(self.winners) - 1
        # Get the samples.
        if len(self.candidates[0].bid_history) == 0:
            return np.random.choice(self.value_profile)
        samples = []
        for i in range(n_samples):
            sample = []
            for candidate in self.candidates:
                time = np.random.choice(len(candidate.bid_history))
                sample.append(
                    candidate.bid_history[time] *\
                    candidate.quality_score/\
                    me.quality_score)
            samples.append(sorted(sample))
            
        # Try all the choices and select the best one.
        best_bid, best_rev = 0, 0
        for bid in np.r_[0: self.value_profile[0] + k_step: k_step]:
            rev = 0  # revenue
            for sample in samples:
                reverse_sample = sample[::-1]
                k = bisect(reverse_sample, bid)
                if k >= n_winners:
                    continue
                rev += self.value_profile[k] - reverse_sample[k]
            if rev > best_rev:
                best_bid, best_rev = bid, rev
        return best_bid
        
                
            
        
                
            
    