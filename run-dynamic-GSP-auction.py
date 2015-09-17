# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 16:57:08 2015

@author: lyc
"""

from candidate import GSPCandidate
from auction import GSPAuction
from strategy import *
import matplotlib.pyplot as plt
import numpy as np

def plot_trend(n_iterations, bids, strategy = 'BestResponse'):
    plt.plot(range(n_iterations), bids[0], label = '1')
    plt.plot(range(n_iterations), bids[1], label = '2')
    plt.plot(range(n_iterations), bids[2], label = '3')
    plt.xlabel('iteration')
    plt.ylabel('bid')
    plt.title(strategy)
    plt.legend()
    plt.savefig(strategy+'.pdf', dpi = 1200)
    plt.show()

if __name__ == '__main__':
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
    
    n_iterations = 20
    for iteration in range(n_iterations):
        GSPAuction(candidates, n_winners).GetWinners()
        for candidate in candidates:
            candidate.strategy =\
                GSP_SmallStepStrategy(candidate, candidates, ctrs)
            candidate.GetNewBid()
        
        for k, candidate in enumerate(candidates):
            bids[k].append(candidate['bid'])
            
    plot_trend(n_iterations, bids, 'SmallStep')
    
    bids = [[],[],[]]
    
    for iteration in range(n_iterations):
        GSPAuction(candidates, n_winners).GetWinners()
        for candidate in candidates:
            candidate.strategy =\
                GSP_BestResponseStrategy(candidate, candidates, ctrs)
            candidate.GetNewBid()
        
        for k, candidate in enumerate(candidates):
            bids[k].append(candidate['bid'])
            
    plot_trend(n_iterations, bids)
    
    bids = [[],[],[]]
    
    for iteration in range(n_iterations):
        GSPAuction(candidates, n_winners).GetWinners()
        for candidate in candidates:
            candidate.strategy =\
                GSP_FictitiousPlayStrategy(candidate, candidates, ctrs)
            candidate.GetNewBid()
        
        for k, candidate in enumerate(candidates):
            bids[k].append(candidate['bid'])
    
    plot_trend(n_iterations, bids, 'FictitiousPlay')
    
    for candidate in candidates:
        print candidate.bid_history
        