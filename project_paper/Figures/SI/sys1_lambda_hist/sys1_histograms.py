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
    plt.rc('font', family='Arial')

    counts_1 = [656514, 674233, 761901, 893958, 988190, 1025104]
    counts_2  = [815575, 813024, 814638, 827226, 859240, 870197]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(
        x=range(1, 7),
        height=counts_1,
        width=1,
        edgecolor='black'
    )
    plt.ylabel('Count')
    plt.xlabel('Alchemical state')
    plt.title('Expanded ensemble', fontsize=14)
    plt.text(-0.12, 1.1, 'A', transform = ax.transAxes, fontsize=26, weight='bold')
    plt.grid()
    plt.savefig('sys1_EXE_hist.png', dpi=600, bbox_inches='tight')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(
        x=range(1, 7),
        height=counts_2,
        width=1,
        edgecolor='black'
    )
    plt.ylabel('Count')
    plt.xlabel('Alchemical state')
    plt.title('1D alchemical metadynamics', fontsize=14)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.text(-0.12, 1.1, 'B', transform = ax.transAxes, fontsize=26, weight='bold')
    plt.grid()
    plt.savefig('sys1_1D_hist.png', dpi=600, bbox_inches='tight')
