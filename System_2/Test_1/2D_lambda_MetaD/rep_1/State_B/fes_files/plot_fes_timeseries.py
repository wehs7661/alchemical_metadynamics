import glob
import time
import plumed
import argparse
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
from matplotlib import rc

def initialize():
    parser =argparse.ArgumentParser(
        description='This code plots the timeseries of the free energy difference between the coupled and uncoupled states and estimate the truncation fraction.')
    parser.add_argument('-dt',
                        '--dt',
                        type=int,
                        default=20,
                        help='The time interval between generation of fes_*.dat files in ps.')
    parser.add_argument('-T',
                        '--temp',
                        type=float,
                        default=298,
                        help='The temperature of the simulation.')
    arg_parse = parser.parse_args()
    return arg_parse

if __name__ == "__main__":
    t1 =time.time()
    args = initialize()

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10,
        'weight': 'bold',
    })
    # Set the font used for MathJax - more on thiprint(images)
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='Arial')

    NA = 6.0221408E23    # Avogadro constant
    k = 1.380649E-23     # Boltzmann constant
    conv = k * args.temp * NA / 1000   # 1 kT in kcal/mol

    n_files = len(glob.glob('fes_*.dat'))

    df = []
    for i in range(n_files - 1):  # The last two files are typically the same
        data = plumed.read_as_pandas(f'fes_{i}.dat')
        fes = np.array(data['projection'])

        df.append((fes[-1] - fes[0]) / conv)
    np.save('df.npy', df)

    t = (np.arange(n_files - 1) + 1) * args.dt / 1000

    algo = rpt.Window(width=50, model='l2').fit(np.array(df))
    change_loc = algo.predict(n_bkps=10)               # index 
    change_t = np.array(change_loc) * args.dt / 1000   # ns

    plt.figure()
    plt.plot(t, df)
    for i in change_t:
        plt.axvline(i, lw=1, color='red')
    plt.xlabel('Time (ns)')
    plt.ylabel('Free energy difference (kT)')
    plt.grid()
    plt.savefig('fes_timeseries.png', dpi=600)

    if change_loc[-1] == n_files - 1:
        truncate_loc = change_loc[-2]
        truncate_t = change_t[-2]
    else:
        truncate_loc = change_loc[-1]
        truncate_t = change_t[-1]
    
    print(f'Change point locations (ns): {change_t}')
    print(f'Truncation location: {truncate_t} (ns)')
    print(f'Truncation fraction: {truncate_loc / (n_files - 1) * 100:.2f}%')
    print(f'Elapsed time: {time.time() - t1} s')


