__author__ = 'lyc'

from generator import VideoPodGenerator
from auction import VideoPodGroupAuction, VideoPodVCG
import numpy as np

if __name__ == '__main__':
    n_iterations = 20
    n_candidates = 10
    vcg_revenues = []
    vcg_welfares = []
    group_revenues = []
    group_welfares = []
    for iteration in range(n_iterations):
        candidates = VideoPodGenerator(n_candidates).GetInstance()
        group_winners, group_welfare = VideoPodGroupAuction(candidates, 5, 240, 5).GetWinners()
        vcg_winners, vcg_welfare = VideoPodVCG(candidates, 5, 240).GetWinners()
        vcg_revenue = sum([winner['price'] for winner in vcg_winners])
        group_revenue = sum([winner['price'] for winner in group_winners])
        assert group_welfare != None, 'None Group welfare'
        assert vcg_welfare != None, 'None VCG welfare'
        for value in ['vcg_revenue', 'group_revenue', 'vcg_welfare', 'group_welfare']:
            exec '%ss.append(%s)' % (value, value)
    print np.mean(vcg_revenues), np.mean(group_revenues)
    print vcg_revenues, group_revenues

