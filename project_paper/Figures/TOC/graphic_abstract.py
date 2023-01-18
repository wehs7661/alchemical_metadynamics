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

    data_1 = plumed.read_as_pandas('fes.dat')
    data_2 = plumed.read_as_pandas('negbias.dat')
    min_list, max_list, nbins_list, dx_list = get_plumed_params(data_1, CV)

    # 1. Plot the 2D free energy surface
    CV_1 = np.array(data_1[CV[0]]) * 180 / np.pi    # degree
    CV_2 = np.array(data_1[CV[1]]) + 1   # make the state index start from 1
    f = np.array(data_1['file.free']) / factor    # kT 
    b = -np.array(data_2['file.free']) / factor    # kT 
    b -= np.min(b)

    plot_fes_surface(CV_1, CV_2, f, 55, [30, -45], 'before.png')
    plot_fes_surface(CV_1, CV_2, f + b, 95, [30, -45], 'after.png')