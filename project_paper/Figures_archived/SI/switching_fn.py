import numpy as np 
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
    plt.rc('font', family='Arial') 

    r = np.arange(0, 3.5, 0.01)
    s = (1 - (r / 0.35) ** 6) / (1 - (r / 0.35) ** 12)

    plt.figure()
    plt.plot(r, s)
    plt.xlabel('Inter-particle distance $r_{ij}$')
    plt.ylabel('Coordination number $s_{ij}$ (nm)')
    plt.grid()
    plt.savefig('switching_fn.png', dpi=600)
