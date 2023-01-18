"""
This codes demonstrates two methods for numerically solving pair distribution of a given box vector.
"""
import time
import itertools
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
from matplotlib import rc

if __name__ == "__main__":
    rc('font', **{
       'family': 'sans-serif',
       'sans-serif': ['DejaVu Sans'],
       'size': 10
       })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    # User-defined parameters
    box_vec = [4.02, 4.05, 4.06]
    nbins = 200
    grid_x = 0.01         # for Method 1
    print('\nParameters')
    print(f'- Box vector: {box_vec}')
    print(f'- Number of bins for histograms: {nbins}')

    # Method 1: Divide the simulation box into subunits
    print('\nEstimating the distribution using Method 1 ...')
    t1 = time.time()
    n_grids = [int(np.ceil(i / grid_x)) for i in box_vec]
    N = [int(i / 2) for i in n_grids]
    delta_x = itertools.product(range(N[0]), range(N[1]), range(N[2]))
    dist = [np.linalg.norm(i) * grid_x for i in delta_x]
    print(f'- The length of the grid: {grid_x}')
    print(f'- Number of grids on each side: {n_grids}')
    print(f'- Number of subunits: {len(dist)}')    
    print(f'\nTime elapsed: {time.time() - t1:.2f} s')

    # Method 2: Randomly pick a point in the simulation box
    t1 = time.time()
    print('\nEstimating the distribution using Method 1 ...')
    print(f'- Number of samples: {len(dist)}')
    r = []
    n_samples = len(dist)   # same number of samples to compare with method 1
    for i in range(n_samples):
        r.append(0.5 * np.linalg.norm(np.array(box_vec) * np.random.rand(3)))
    print(f'\nTime elapsed: {time.time() - t1:.2f} s')

    # Plotting the distributions
    t1 = time.time()
    print('\nPlotting the distriutions ...')
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(2, 1, 1)

    plt.subplot(1, 2, 1)
    sns.histplot(dist, bins=nbins, stat='density', kde=True)
    plt.xlabel('r')
    plt.ylabel('p(r)')
    plt.title('Method 1', weight='bold')
    plt.grid()

    plt.subplot(1, 2, 2)
    sns.histplot(r, bins=nbins, stat='density', kde=True)
    plt.xlabel('r')
    plt.ylabel('p(r)')
    plt.title('Method 2', weight='bold')
    plt.grid()

    plt.tight_layout()
    plt.savefig('pair_distribution.png', dpi=600)
    print(f'\nTime elapsed: {time.time() - t1:.2f} s')

    # Note that the peak position is acutally analytically solvable, which should be at half of the shortest side
    # Here we still provide two possible methods that could solve the peak position without knowing the analytical solution.
    # Note that the peak position does not seem to converge with increasing number of bins though.
    # The code in this section can be modified with argparse as needed. 
    peak_method = None  
    if peak_method == 'hist':   # get the peak position from the histogram data
        hist = np.histogram(dist, bins=nbins)
        n_max_idx = list(hist[0]).index(max(hist[0]))
        p = 0.5 * (hist[1][n_max_idx] + hist[1][n_max_idx + 1])
    elif peak_method == 'kde':  # get the peak position from the kde plot
        xy_data = plt.gca().get_lines()[0].get_xydata()
        x, y = list(np.transpose(xy_data)[0]), list(np.transpose(xy_data)[1])
        p = x[y.index(max(y))]
