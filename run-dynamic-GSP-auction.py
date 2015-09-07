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
    plt.plot(range(n_iterations), np.array(bids).T, label = ['1', '2', '3'])
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
    candidate1 = GSPCandidate(value_profile = [10, 2], bid = 2)
    candidate2 = GSPCandidate(value_profile = [9, 4], bid = 4)
    candidate3 = GSPCandidate(value_profile = [8, 3], bid = 3)
    candidates = [candidate1, candidate2, candidate3]
    
    n_winners = 2
    for winner in winners:
        print winner['id']
    
    bids = [[],[],[]]
    
    n_iterations = 500
    for iteration in range(n_iterations):
        extended_winners = GSPAuction(candidates, n_winners).GetWinners(True)
        for candidate in candidates:
            candidate.strategy =\
                GSP_BestResponseStrategy(candidate['value_profile'],\
                candidate, extended_winners)
            candidate.GetNewBid()
        
        for k, candidate in enumerate(candidates):
            bids[k].append(candidate['bid'])
            
    plot_trend(n_iterations, bids)
    
        