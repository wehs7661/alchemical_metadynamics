import plumed 
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
from matplotlib import rc

if __name__ == '__main__':
    rc("font", **{"family": "sans-serif", "sans-serif": ["DejaVu Sans"], "size": 10})
    # Set the font used for MathJax - more on this later
    rc("mathtext", **{"default": "regular"})
    plt.rc("font", family="Arial")

    data_1 = plumed.read_as_pandas('analysis_1D.dat')
    data_2 = plumed.read_as_pandas('analysis_2D.dat')
    t = np.array(data_1['time']) / 1000
    n_1 = np.array(data_1['n'])
    n_2 = np.array(data_2['n'])

    # algo = rpt.Window(width=40, model="l2").fit(n)
    # change_loc = algo.predict(n_bkps=10)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(t, n_1)
    # for i in change_loc:
        # print(f'Marking the change location at {t[i-1]} ns ...')
        # plt.axvline(t[i-1], lw=2, color='red')
    plt.xlabel('Time (ns)')
    plt.ylabel('Number of water molecules')
    plt.title('1D alchemical metadynamics')
    plt.grid()
    plt.savefig('water_timeseries_1D.png', dpi=600)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(t, n_2)
    # for i in change_loc:
        # print(f'Marking the change location at {t[i-1]} ns ...')
        # plt.axvline(t[i-1], lw=2, color='red')
    plt.xlabel('Time (ns)')
    plt.ylabel('Number of water molecules')
    plt.title('2D alchemical metadynamics')
    plt.grid()
    plt.savefig('water_timeseries_2D.png', dpi=600)
