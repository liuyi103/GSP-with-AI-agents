# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 14:26:10 2015

@author: lyc
"""

from winner import GSPWinner, VideoPodWinner
from candidate import GSPCandidate, VideoPodCandidate, VideoPodGroupCandidate
import pulp as pp
import copy

class Auction:
    ''' 
    This is the base class for auctions.
    Given candidates, output winners.
    '''

    def __init__(self, candidates=[]):
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

    def __init__(self, candidates=[], n_winners=1):
        Auction.__init__(self, candidates)
        self.n_winners = min(n_winners, len(candidates))
        self.candidates = sorted(self.candidates, \
                                 key=lambda x: -x['bid'] * x['quality_score'])

    def GetWinners(self, extended=False):
        '''
        Attention:
        The last one in the returned winners is not a winner
        if extended is True
        '''
        # Avoid all winners case.
        self.candidates.append(GSPCandidate(0, 0))
        self.candidates.append(GSPCandidate(0, 0))
        for i in range(self.n_winners):
            self.winners.append(GSPWinner( \
                self.candidates[i], \
                self.candidates[i + 1]['quality_score'] * \
                self.candidates[i + 1]['bid'] / \
                self.candidates[i]['quality_score']))

        ret_winners = self.winners + \
                      ([self.candidates[self.n_winners]] if extended else [])
        # remove the additional candidate
        self.candidates = self.candidates[:-2]
        return ret_winners


class VideoPodAuction(Auction):
    '''
    Video pod auction is the auction to sell a video pod.
    Each candidate has a bid and duration.
    The goal is to find a set of candidates as winners subject to the maximum duration constraint
    '''
    def __init__(self, candidates=[], n_winners=1e6, max_duration=200):
        '''
        initialize a video pod auction
        :param candidates: a list of VideoPodCandidate
        :param n_winners: the maximum number of winners
        :return:
        '''
        Auction.__init__(self, candidates)
        self.n_winners = min(n_winners, len(candidates))
        self.max_duration = max_duration

    def GetOptimalWinners(self):
        '''
        By default, find the set of candidates that maximize total bids.
        :return:
        '''
        prob = pp.LpProblem('KNAPSACK', pp.LpMaximize)
        x = pp.LpVariable.dict('x', range(len(self.candidates)), 0, 1.5, pp.LpInteger)
        prob += (sum(x) <= self.n_winners)
        prob += (sum([x[k] * candidate['duration'] for k, candidate in enumerate(self.candidates)]) \
                <= self.max_duration)
        prob += sum([x[k] * candidate['bid'] for k, candidate in enumerate(self.candidates)] + [0])
        prob.solve()
        for i in range(len(self.candidates)):
            if pp.value(x[i]) == 1:
                self.winners.append(VideoPodWinner(self.candidates[i]))
        return self.winners, pp.value(prob.objective)

class VideoPodVCG(VideoPodAuction):
    '''
    Run video pod auction with VCG.
    '''
    def __init__(self, candidates, n_winners, max_duration):
        VideoPodAuction.__init__(self, candidates, n_winners, max_duration)

    def GetWinners(self):
        winners, welfare = VideoPodAuction(self.candidates, self.n_winners, self.max_duration).GetOptimalWinners()
        for k_winner, winner in enumerate(winners):
            other_welfare = welfare - winner['bid']
            old_duration = winner['duration']
            winners[k_winner].candidate.duration = self.max_duration + 1
            _, new_welfare = VideoPodAuction(self.candidates, self.n_winners, self.max_duration).GetOptimalWinners()
            winner.price = new_welfare - other_welfare
            winner.candidate.duration = old_duration
        self.winners = winners
        return self.winners, welfare

class VideoPodGroupAuction(VideoPodAuction):
    '''
    1. divide the candidates into groups, with the size of each group given by group_size
    2. For each group select a subset
    3. Run knapsack algorithm on the selected groups
    '''
    def __init__(self, candidates, n_winners, max_duration, group_size):
        VideoPodAuction.__init__(self, candidates, n_winners, max_duration)
        self.group_size = group_size

    @ staticmethod
    def SelectGroupCandidate(candidates):
        assert len(candidates) > 0, 'invalid candidates'
        candidates = copy.deepcopy(candidates)
        candidates.append(VideoPodCandidate(0, 1e9))
        candidates.sort(key = lambda x: -x['bid'] / x['duration'])
        end_nums = range(1, len(candidates))
        total_duration = lambda end_num: sum([candidate['duration'] for candidate in candidates[:end_num]])
        end_num = max(end_nums, key = lambda end_num: total_duration(end_num) * candidates[end_num]['bid'])
        return VideoPodGroupCandidate(candidates[:end_num], candidates[end_num].bid * 1.\
                                      / candidates[end_num].duration)

    def GetWinners(self):
        self.candidates.sort(key = lambda candidate: -candidate['duration'])
        candidates = self.candidates + [VideoPodCandidate(0, 1e9) for i in range(self.group_size)]
        group_candidates = []
        for p in range(0, len(self.candidates), self.group_size):
            group_candidates.append(self.SelectGroupCandidate(candidates[p: p+self.group_size]))
        winner_groups, welfare = VideoPodAuction(group_candidates, self.n_winners, self.max_duration)\
            .GetOptimalWinners()
        assert welfare != None, 'Wrong welfare from VideoPodAuction'
        winners = []
        for winner_group  in winner_groups:
            for win_candidate in winner_group['candidates']:
                winners.append(VideoPodWinner(win_candidate, win_candidate['duration'] * winner_group['unitprice']))
        return winners, welfare


