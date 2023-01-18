import copy 
import plumed 
import argparse
import numpy as np
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def get_plumed_params(data, CV):
    params = {}
    for i in data.plumed_constants:
        params[i[0]] = i[1]

    min_list, max_list, nbins_list, dx_list = [], [], [], []
    for i in range(2):
        if f'min_{CV[i]}' in params:
            if 'pi' in params[f'min_{CV[i]}']:
                params[f'min_{CV[i]}'] = eval(params[f'min_{CV[i]}'].replace('pi', 'np.pi'))
            min_list.append(float(params[f'min_{CV[i]}']))

        if f'max_{CV[i]}' in params:
            if 'pi' in params[f'max_{CV[i]}']:
                params[f'max_{CV[i]}'] = eval(params[f'max_{CV[i]}'].replace('pi', 'np.pi'))
            max_list.append(float(params[f'max_{CV[i]}']))

        if f'nbins_{CV[i]}' in params:
            nbins_list.append(int(params[f'nbins_{CV[i]}']))

    min_list = np.array(min_list)
    max_list = np.array(max_list)
    nbins_list = np.array(nbins_list)
    dx_list = (max_list - min_list) / (nbins_list - 1)

    return min_list, max_list, nbins_list, dx_list

def plot_fes_surface(x, y, z, z_max, view_angle, fig_name):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    
    n = int(max(y))
    space = int(np.ceil(n / 10))
    ax.set_yticks(np.arange(0, n + 1, space))
    
    ax.set_xlabel('Torsional angle (degree)', fontsize=16)
    ax.set_ylabel('Alchemical state', fontsize=16)
    ax.set_zlabel('Free energy ($ k_{B}T $)', fontsize=16)
    ax.tick_params(axis='x', labelsize= 12)
    ax.tick_params(axis='y', labelsize= 12)
    ax.tick_params(axis='z', labelsize= 12)
    ax.view_init(*view_angle)

    ax.set_xlim(-180, 180)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, z_max)

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.tight_layout()
    plt.savefig(fig_name, dpi=600)

def plot_fes_contour(x_grids, y_grids, z, y_ticks, fig_name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    img = ax.contourf(x_grids, y_grids, z, cmap='viridis')
    ax.set_xlabel('Torsional angle (degree)')
    ax.set_ylabel('Alchemical state')
    fig.colorbar(img, ax=ax)
    ax.set_yticks(y_ticks)
    plt.savefig(fig_name, dpi=600)

if __name__ == "__main__":
    CV = ['theta', 'lambda']

    rc('font', **{
       'family': 'sans-serif',
       'sans-serif': ['DejaVu Sans'],
       'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='Arial')  

    k = 1.38064852E-23  # Boltzmann constant
    N_A = 6.02214086E23 # Avogadro constant
    factor = (k * 298) * N_A / 1000

    data_A = plumed.read_as_pandas('fes_stateA.dat')
    data_B = plumed.read_as_pandas('fes_stateB.dat')

    # The two fes.dat files should have the same min, max, nbins, dx, hence the save grids for CVs
    min_list, max_list, nbins_list, dx_list = get_plumed_params(data_A, CV)

    # 1. Plot the 2D free energy surface of A, B, and their difference and average
    CV_1 = np.array(data_A[CV[0]]) * 180 / np.pi    # degree
    CV_2 = np.array(data_A[CV[1]]) + 1   # make the state index start from 1
    f_A = np.array(data_A['file.free']) / factor    # kT 
    f_B = np.array(data_B['file.free']) / factor    # kT
    diff_fes = f_A - f_B
    avg_fes = (f_A + f_B) / 2 
    
    plot_fes_surface(CV_1, CV_2, f_A, 55, [30, -45], 'sys2_fes.png')
    """
    plot_fes_surface(CV_1, CV_2, f_B, 55, [30, -45], 'sys2_fes_B.png')
    plot_fes_surface(CV_1, CV_2, diff_fes, 1.5, [30, -45], 'sys2_fes_diff.png')
    plot_fes_surface(CV_1, CV_2, avg_fes, 55, [30, -45], 'sys2_fes_avg.png')

    print(f'Max difference: {np.max(diff_fes):.3f} kT')
    print(f'Average difference: {np.mean(diff_fes):.3f} kT')

    # 2. Plot the contour plot of A, B, and their difference and average
    CV1_grids = np.linspace(min_list[0], max_list[0], nbins_list[0]) * 180 / np.pi
    CV2_grids = np.linspace(min_list[1] + 1, max_list[1] + 1, nbins_list[1]) 
    ff_A = f_A.reshape(nbins_list[1], nbins_list[0])
    ff_B = f_B.reshape(nbins_list[1], nbins_list[0])
    ff_diff = ff_A - ff_B
    ff_avg = (ff_A + ff_B) / 2

    n = int((max(CV_2)))
    space = int(np.ceil(n / 10))
    y_ticks = np.arange(1, n + 1, int(space / 2))

    plot_fes_contour(CV1_grids, CV2_grids, ff_A, y_ticks, 'sys2_contour_A.png')
    plot_fes_contour(CV1_grids, CV2_grids, ff_B, y_ticks, 'sys2_contour_B.png')
    plot_fes_contour(CV1_grids, CV2_grids, ff_diff, y_ticks, 'sys2_contour_diff.png')
    plot_fes_contour(CV1_grids, CV2_grids, ff_avg, y_ticks, 'sys2_contour_avg.png')
    """