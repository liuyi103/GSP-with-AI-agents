# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 14:55:00 2015

@author: lyc
"""

class Winner:
    ''' The winner of an auction. '''
    def __init__(self, candidate, price = 0):
        self.candidate = candidate
        self.price = price
    
    def __getitem__(self, key):
        try:
            exec 'value = self.candidate[\'%s\']' % key
            return value
        except:
            exec 'value = self.%s' % key
        return value

GSPWinner = Winner

VideoPodWinner = Winner

if __name__ == '__main__':
    from candidate import GSPCandidate
    winner = GSPWinner(GSPCandidate())
    print winner['bid'], winner['price']