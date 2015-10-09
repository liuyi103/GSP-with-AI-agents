from unittest import TestCase
from generator import VideoPodGenerator
from auction import VideoPodAuction

__author__ = 'lyc'


class TestVideoPodAuction(TestCase):
    def test_GetOptimalWinners(self):
        n_iterations = 2
        n_candidates = 10
        vcg_revenues = []
        vcg_welfares = []
        group_revenues = []
        group_welfares = []
        for iteration in range(n_iterations):
            candidates = VideoPodGenerator(n_candidates).GetInstance()
            optimal_winners, optimal_welfare = VideoPodAuction(candidates, 5, 240).GetOptimalWinners()
            print optimal_welfare, optimal_winners

