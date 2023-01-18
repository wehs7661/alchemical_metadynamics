import time
import plumed 
import itertools
import argparse
import numpy as np 
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt 
from matplotlib import rc 
from prettytable import PrettyTable
np.random.seed(0)

def initialize():
    parser = argparse.ArgumentParser(
        description='This codes plots the pair distribution function g(r) given the box vectors of the simulation box.'
    )
    parser.add_argument(
        "-v",
        "--vec",
        type=float,
        nargs='+',
        help='The box vectors of a rectangular simulation box.'
    )
    parser.add_argument(
        "-n",
        "--nbins",
        type=int,
        default=200,
        help="The number of bins for the histogram."
    )
    parser.add_argument(
        "-s",
        "--samples",
        type=int,
        default=5000000,
        help="The number of samples drawn from uniform distributions to estimate the real distribution given the box lengths."
    )
    parser.add_argument(
        "-p",
        "--peak",
        choices=['hist', 'kde'],
        default='hist',
        help="The method to estimate the peak position of the input distribution."
    )
    
    arg_parse = parser.parse_args()

    return arg_parse

def find_peak(data, nbins, method):
    """
    data (array-like): The input data
    nbins (n): The number of bins for histograms
    method (str): Two choices: 'hist' or 'kde'
    """
    if method == 'hist':
        hist = np.histogram(data, bins=nbins)
        n_max_idx = list(hist[0]).index(max(hist[0]))
        p = 0.5 * (hist[1][n_max_idx] + hist[1][n_max_idx + 1])
    elif method == 'kde':
        sns.histplot(data, bins=nbins, kde=True)
        xy_data = plt.gca().get_lines()[0].get_xydata()
        x, y = list(np.transpose(xy_data)[0]), list(np.transpose(xy_data)[1])
        p = x[y.index(max(y))]

    return p

if __name__ == "__main__":
    t1 = time.time()
    args = initialize()
    plt.figure()

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
        })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='Arial')

    # 1. Calculate relevant parameters
    r_max = np.linalg.norm(args.vec) / 2 

    # 2. Read in data and plot q(r) for each simulation.
    data_1 = plumed.read_as_pandas('analysis_1D.dat')
    data_1 = data_1[data_1['lambda']==39]['d']
    hist_1 = plt.hist(data_1, bins=args.nbins, range=[0, r_max], label='1D $\lambda$-MetaD', alpha=0.8, density=True, color='lightgreen')

    data_2 = plumed.read_as_pandas('analysis_2D.dat')
    data_2 = data_2[data_2['lambda']==39]['d']
    hist_2 = plt.hist(data_2, bins=args.nbins, range=[0, r_max], label='2D $\lambda$-MetaD', alpha=0.8, density=True, color='lightblue')

    # 3. Estimate the distribution p(r) corresponding to the given box lengths
    r = []
    for j in range(args.samples):
        r.append(0.5 * np.linalg.norm(np.array(args.vec) * np.random.rand(3)))
            
    # sns.histplot(r, bins=args.nbins, kde=True, stat='density', label='Real distribution')
    sns.kdeplot(r, label='Real distribution')
    plt.xlabel('COM distance')
    plt.ylabel('Probability density')
    plt.grid()
    plt.legend()
    plt.savefig('pair_correlation_fitting.png', dpi=600)

    # Plot with matplotlib but not saved. This is just for later analysis
    hist_3 = plt.hist(r, bins=args.nbins, range=[0, r_max], label='Real distribution', alpha=0.8, zorder=0, density=True)

    # 4. Assess the similarity between different distributions
    print('\nComparison of the distribution from each simulation with the reference')
    print('======================================================================')
    
    # 4-1: Estimate the peak positions
    print(f'The theoretical peak position is at {min(args.vec) / 2:.3f} nm.')
    peak_1 = find_peak(data_1, args.nbins, args.peak)
    peak_2 = find_peak(data_2, args.nbins, args.peak)

    # 4-2. K-S tests
    d_1, p_1 = stats.ks_2samp(r, data_1)
    d_2, p_2 = stats.ks_2samp(r, data_2)

    # 4-3. RMSE calculation
    RMSE_1 = np.sqrt(np.sum((hist_1[0] - hist_3[0]) ** 2)) / len(hist_1[0])
    RMSE_2 = np.sqrt(np.sum((hist_2[0] - hist_3[0]) ** 2)) / len(hist_2[0])
    
    if p_1 >= 0.05:
        r_1 = 'Consistent'
    else:
        r_1 = 'Inconsistent'
    
    if p_2 >= 0.05:
        r_2 = 'Consistent'
    else:
        r_2 = 'Inconsistent'

    x = PrettyTable()
    x.field_names = ['Simulation', 'Peak position', 'RMSE', 'D-statistics', 'p-value', 'Conclusion']
    x.add_row(['1D lambda-MetaD', f'{peak_1:.3f}', f'{RMSE_1:.5f}', f'{d_1:.3f}', f'{p_1:.3f}', f'{r_1}'])
    x.add_row(['2D lambda-MetaD', f'{peak_2:.3f}', f'{RMSE_2:.5f}', f'{d_2:.3f}', f'{p_2:.3f}', f'{r_2}'])
    print(x)
    