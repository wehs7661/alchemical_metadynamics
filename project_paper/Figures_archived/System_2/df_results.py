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

    df = [0.707, -0.232, 0.643, 0.697]
    err = [0.032, 0.033, 0.031, 0.032]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(range(2), df[:2], yerr=err[:2], edgecolor='black', capsize=3, width=0.6, label='1D alchemical metadynamics')
    plt.bar(range(2, 4), df[2:], yerr=err[2:], edgecolor='black', capsize=3, width=0.6, label='2D alchemical metadynamics')
    plt.xticks(range(4))
    ax.set_xticklabels(['State A', 'State B', 'State A', 'State B'])
    plt.ylabel('Estimated solvation free energy ($ k_{B}T $)')
    plt.legend()
    plt.grid()
    plt.savefig('sys2_df_results.png', dpi=600)