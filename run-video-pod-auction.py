__author__ = 'lyc'

from generator import VideoPodGenerator
from auction import VideoPodVCG, VideoPodMCVBR
import numpy as np

if __name__ == '__main__':
    n_iterations = 20
    n_candidates = 20
    vcg_revenues = []
    vcg_welfares = []
    cvbrs = []
    for iteration in range(n_iterations):
        candidates = VideoPodGenerator(n_candidates).GetInstance()
        vcg_winners, vcg_welfare, CVBR = VideoPodMCVBR(candidates, 100, 240).GetWinners()
        print CVBR
    #     vcg_revenue = sum([winner['price'] for winner in vcg_winners])
    #     assert vcg_welfare is not None, 'None VCG welfare'
    #     for value in ['vcg_revenue', 'vcg_welfare']:
    #         exec '%ss.append(%s)' % (value, value)
    # print np.mean(vcg_revenues)
    # print vcg_revenues

