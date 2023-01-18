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

def initialize():
    parser = argparse.ArgumentParser(
        description='This code plots the 2D free energy surface given a multidimensional fes.dat.')
    parser.add_argument('-i',
                        '--input',
                        default='fes_2D.dat',
                        help='The filename of the input FES file.')
    parser.add_argument('-c',
                        '--CV',
                        required=True,
                        nargs='+',
                        help='The names of the CVs of interest.')
    parser.add_argument('-t',
                        '--temp',
                        type=float,
                        default=298,
                        help='The temperature of the simulation.')
    parser.add_argument('-x',
                        '--xlabel',
                        help='The variable name of the x-axis.')
    parser.add_argument('-y',
                        '--ylabel',
                        help='The variable name of the y-axis.')
    parser.add_argument('-f',
                        '--factors',
                        type=float,
                        nargs='+',
                        default=[1, 1],
                        help='The unit conversion factors to be divded by x and y.')
    parser.add_argument('-n',
                        '--fig_name',
                        help='The file name of the output figure.')
    parser.add_argument('-rx',
                        '--range_x',
                        type=float,
                        nargs='+',
                        help='The minimum and maximum of variabl x in plotting.')
    parser.add_argument('-ry',
                        '--range_y',
                        type=float,
                        nargs='+',
                        help='The minimum and maximum of variabl y in plotting.')
    parser.add_argument('-s',
                        '--shift',
                        help='The file name of the 1D FES data for shifting the 2D free energy surface.')
    parser.add_argument('-a',
                        '--angle',
                        type=float,
                        nargs='+',
                        default=[30, -45],
                        help='The elevation and azimuth angle of the 2D surface.')
    parser.add_argument('-co',
                        '--contour',
                        default=False,
                        action='store_true',
                        help='Whether to plot the contour plot.')

    args_parse = parser.parse_args()
    return args_parse

def get_plumed_params(data, CV):
    params = {}
    for i in data.plumed_constants:
        params[i[0]] = i[1]

    min_list, max_list, nbins_list, dx_list = [], [], [], []
    for i in range(2):
        if f'min_{CV[i]}' in params:
            # if 'pi' in params[f'min_{CV[i]}']:
                # params[f'min_{CV[i]}'] = eval(params[f'min_{CV[i]}'].replace('pi', 'np.pi'))
            min_list.append(float(params[f'min_{CV[i]}']))

        if f'max_{CV[i]}' in params:
            # if 'pi' in params[f'max_{CV[i]}']:
                # params[f'max_{CV[i]}'] = eval(params[f'max_{CV[i]}'].replace('pi', 'np.pi'))
            max_list.append(float(params[f'max_{CV[i]}']))

        if f'nbins_{CV[i]}' in params:
            nbins_list.append(int(params[f'nbins_{CV[i]}']))

    min_list = np.array(min_list)
    max_list = np.array(max_list)
    nbins_list = np.array(nbins_list)
    dx_list = (max_list - min_list) / (nbins_list - 1)

    return min_list, max_list, nbins_list, dx_list


if __name__ == "__main__":
    args = initialize()
    if args.xlabel is None:
        args.xlabel = args.CV[0]
    if args.ylabel is None:
        args.ylabel = args.CV[1]

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
    factor = (k * args.temp) * N_A / 1000

    data = plumed.read_as_pandas(args.input)
    if args.range_x is not None:
        data = data[data[args.CV[0]].between(args.range_x[0], args.range_x[1])]
    if args.range_y is not None:
        data = data[data[args.CV[1]].between(args.range_y[0], args.range_y[1])]

    min_list, max_list, nbins_list, dx_list = get_plumed_params(data, args.CV)
    CV_1 = np.array(data[args.CV[0]]) / args.factors[0]
    CV_2 = np.array(data[args.CV[1]]) / args.factors[1]
    f = np.array(data['file.free']) / factor    # kT 

    if args.shift is not None:
        data_shift = plumed.read_as_pandas(args.shift)
        n_bins_shift = max(int(np.ptp(CV_1) / dx_list[0]) + 1, int(np.ptp(CV_2) / dx_list[1]) + 1)
        # f_shift = list(data_shift['projection'] / factor)    # kT    
        f_shift = list(data_shift['projection'] / factor) 
        f_shift_copy = copy.deepcopy(f_shift)
        for i in range(n_bins_shift - 1):    # should be nbins in the configurational CV
            f_shift.extend(f_shift_copy)
        f_shift = np.array(f_shift)
        shifted_f = f - f_shift
    
    # 1. Plot the 2D free energy surface
    fig = plt.figure(figsize=(9,6))
    ax1 = fig.add_subplot(111, projection='3d')
    if args.shift is not None:
        ax1.plot_trisurf(CV_1, CV_2, shifted_f, cmap='viridis', edgecolor='none') 
    else:
        ax1.plot_trisurf(CV_1 + 1, CV_2, f, cmap='viridis', edgecolor='none') 
    ax1.set_xlabel(args.xlabel, fontsize=16)  # color='white'
    ax1.set_ylabel(args.ylabel, fontsize=16)  # color='white'
    ax1.set_zlabel('Free energy ($ k_{B}T $)', fontsize=16)  # color='white'
    ax1.view_init(args.angle[0], args.angle[1])  # default: (30, -45)
    # ax1.set_title('Free energy surface of System 3')
    #  ax1.tick_params(axis='x', colors='white')
    # ax1.tick_params(axis='y', colors='white')
    # ax1.tick_params(axis='z', colors='white')
    if args.CV[0] == 'lambda':
        n = int(max(CV_1)) + 1
        space = int(np.ceil(n / 10))
        ax1.set_xticks(np.arange(0, n + 1, space))
    if args.CV[1] == 'lambda':
        n = int(max(CV_2)) + 1
        space = int(np.ceil(n / 10))
        ax1.set_yticks(np.arange(0, n + 1, space))

    # ax1.set_xlim(-180, 180)
    # ax1.set_ylim(0, 20)
    # ax1.set_zlim(0, 55)
    ax1.tick_params(axis='x', labelsize= 12)
    ax1.tick_params(axis='y', labelsize= 12)
    ax1.tick_params(axis='z', labelsize= 12)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.tight_layout()
    plt.savefig(f'{args.fig_name}_fes.png', dpi=600)

    # 2. Plot the contour plot
    if args.contour is True:
        CV1_grids = np.linspace(np.min(CV_1) + 1, np.max(CV_1) + 1, int(np.ptp(CV_1) / dx_list[0]) + 1) / args.factors[0]
        CV2_grids = np.linspace(np.min(CV_2), np.max(CV_2), int(np.ptp(CV_2) / dx_list[1]) + 1) / args.factors[1]
        #CV1_grids = np.linspace(min_list[0], max_list[0], nbins_list[0]) / args.factors[0]
        #CV2_grids = np.linspace(min_list[1], max_list[1], nbins_list[1]) / args.factors[1]

        # ff = f.reshape(int(np.ptp(CV_2) / dx_list[1]) + 1, int(np.ptp(CV_1) / dx_list[0]) + 1)
        #ff = f.reshape(nbins_list[1], nbins_list[0])  # not f.reshape(nbins_list[0], nbins_list[1]) !
        
        if args.shift is not None:
            shifted_ff = shifted_f.reshape(int(np.ptp(CV_2) / dx_list[1]) + 1, int(np.ptp(CV_1) / dx_list[0]) + 1)
        
        fig = plt.figure()
        ax2 = fig.add_subplot(111)
        if args.shift is not None:
            img = ax2.contourf(CV1_grids, CV2_grids, shifted_ff, cmap='viridis')
        else:
            img = ax2.contourf(CV1_grids, CV2_grids, ff, cmap='viridis')
        ax2.set_xlabel(args.xlabel)
        ax2.set_ylabel(args.ylabel)
        fig.colorbar(img, ax=ax2)

        if args.CV[0] == 'lambda':
            ax2.set_xticks(np.arange(1, n+1, int(space/2)))
        if args.CV[1] == 'lambda':
            ax2.set_yticks(np.arange(1, n+1, int(space/2)))
        plt.savefig(f'{args.fig_name}_contour.png', dpi=600)

    # if args.contour is True:
    #     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # plt.show()
    # plt.savefig(f'{args.fig_name}.png', dpi=600)
