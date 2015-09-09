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

class GSPFakeCandidate:
    '''
    A fake candidate is a candidate with everything 0.
    '''
    def __init__(self):
        self.bid = 0
        self.bid_history = [0]
        self.value = 0
        self.quality_score = 1
        self.id = -1
        self.strategy = 0
        
    def __getitem__(self, key):
        exec 'value = self.' + key
        return value

class GSP_Strategy:
    '''
    The class for the strategies that are used in GSP auction.
    Strategy is assigned to a candidate by main, because only main can
    get access to all winners.
    '''
    def __init__(self, me = ['candidate'] , candidates = [], ctrs = [1]):
        '''
        me is the host of the strategy, which is a GSPCandidate
        winners is the winners from the last round.
        ctrs is the click through rates.
        '''
        self.value = me.value
        self.me = me
        self.candidates = candidates
        self.n_winners = min(len(ctrs), len(candidates))
        self.ctrs = ctrs + [0] * len(candidates)

class GSP_TruthfulStrategy(GSP_Strategy):
    ''' report the true top value. '''
    def __init__(self, me):
        GSP_Strategy.__init__(self, me)
    
    def GetBid(self):
        return self.value

class GSP_BestResponseStrategy(GSP_Strategy):
    ''' 
    Try each winning position, the find the best one of them.
    '''
    def __init__(self, me, candidates, ctrs):
        GSP_Strategy.__init__(self, me, candidates, ctrs)
        
    def GetBid(self):
        prices = sorted([x.bid * x.quality_score / self.me.quality_score \
            for x in self.candidates], reverse = True)
        prices.remove(self.me.bid)
        pos_price = zip(range(len(prices)), prices)
        choice = max(pos_price,\
            key = lambda x: self.ctrs[x[0]] * (self.value - x[1]))
        return choice[1] + k_epsilon if self.value - choice[1] > 0\
            else self.value

class GSP_SmallStepStrategy(GSP_Strategy):
    '''
    Each time, one candidate walk a small step to the best response.
    The step length is set to be a fix number which is the k_step.
    '''
    def __init__(self, me, candidates, ctrs):
        GSP_Strategy.__init__(self, me, candidates, ctrs)
        
    def GetBid(self):
        prices = sorted([x.bid * x.quality_score / self.me.quality_score \
            for x in self.candidates], reverse = True)
        prices.remove(self.me.bid)
        pos_price = zip(range(len(prices)), prices)
        choice = max(pos_price,\
            key = lambda x: self.ctrs[x[0]] * (self.value - x[1]))
        # individually rational
        if self.value - choice[1] < 0:
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
    def __init__(self, value, me, candidates, ctrs):
        GSP_Strategy.__init__(self, value, me, ctrs = ctrs)
        self.candidates = candidates
    
    def __init__(self, me, candidates, ctrs):
        GSP_Strategy.__init__(self, me.value, me, ctrs = ctrs)
        self.candidates = candidates
        
    def GetBid(self):
        n_winners = len(ctrs)
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
        
                
            
        
                
            
    