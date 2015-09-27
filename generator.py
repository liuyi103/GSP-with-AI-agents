__author__ = 'lyc'

import numpy as np
import random
from candidate import VideoPodCandidate

class VideoPodGenerator:
    def __init__(self, n_candidates, get_duration = None, get_value = None):
        if get_duration == None:
            get_duration = lambda : random.randint(10, 60)
        if get_value == None:
            get_value = lambda : random.random()
        self.get_duration = get_duration
        self.get_value = get_value
        self.n_candidates = n_candidates

    def GetInstance(self):
        candidates = []
        for i in range(self.n_candidates):
            candidates.append(VideoPodCandidate(self.get_value(), self.get_duration()))
        return candidates
