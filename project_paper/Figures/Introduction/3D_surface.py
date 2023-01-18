import copy 
import argparse
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rc
np.random.seed(0)

def initialize():
    parser = argparse.ArgumentParser(
        description='This code demonstrates two possible cases of free energy surface that can fail expanded ensemble.')
    parser.add_argument('-f',
                        '--font',
                        choices=['Arial', 'Serif'],
                        default='Arial',
                        help='The font for the figures.')
    parser.add_argument('-c',
                        '--color',
                        default='black',
                        help='The color of the texts and borders.')
    parser.add_argument('-t',
                        '--transparent',
                        action='store_true',
                        default=False,
                        help='Whether the figure should be saved with transparent backgrounds.')
    args_parse = parser.parse_args()
    return args_parse

def FES(coef, x, x_shift=0):
    y = 0
    for i in range(len(coef)):
        y += coef[i] * (x - x_shift) ** (len(coef)-1 - i)
    return y

def change_color(ax, color):
    # For better presentation in the webpage
    ax.tick_params(color=color, labelcolor=color)
    for spine in ax.spines.values():
        spine.set_edgecolor(color)

if __name__ == "__main__":
    args = initialize()
    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10,
        'weight': 'bold',
    })
    # Set the font used for MathJax - more on thiprint(images)
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family=args.font)

    # A template surface to start with
    coef_start = [-0.000481992, 0.0133127, -0.102597,
                  -0.0406179, 2.84049, -7.0026, 6.84595]
    coef_mid = [-0.000481992, 0.0133127, -0.102597,
                -0.0406179, 2.84049, -7.5026, 6.84595]  # the second last coef is different from "start"

    x = np.arange(0, 12.1, 0.1)
    y = np.arange(0, 1.1, 0.1)
    X, Y = np.meshgrid(x, y)
    Z = FES(coef_start, X)

    ############################################################
    #                                                          #
    #  Scenario A: A free energy barrier that EXE can overcome #
    #                                                          #
    ############################################################
    
    fig = plt.figure(figsize=(21, 6))
    ax0 = fig.add_subplot(131, projection='3d')
    coef_end = [0.0000879645, -0.00136518, -0.016613,
                0.420782, -2.41395, 2.95784, 7.93313] # flip the sign and shift up

    Z0 = copy.deepcopy(Z)
    """
    Z0[5] = FES(coef_mid, x)
    delta_start_mid = (Z0[5] - Z0[0]) / 5
    for i in np.arange(0, 5, 1):
        Z0[i] = Z0[0] + delta_start_mid * i - np.random.rand(1, len(Z0[i]))
    """

    Z0[-1] = FES(coef_end, x)
    delta_mid_end = (Z0[-1] - Z0[0]) / (len(y) - 1)
    for i in range(len(y) - 1):
        Z0[i] = Z0[0] + delta_mid_end * i + np.random.rand(1, len(Z0[i]))
    Z0 -= np.min(Z0)

    surf = ax0.plot_surface(X, Y, Z0, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax0.view_init(elev=30, azim=-60)
    ax0.set_xlabel('Collective variable', fontsize='10', fontweight='bold', color = args.color)
    ax0.set_xlim3d(0, 13)
    ax0.set_ylabel('Alchemical variable',
                    fontsize='10', fontweight='bold', color = args.color)
    ax0.set_ylim3d(0, 1)
    ax0.set_zlim3d(0, 18)
    ax0.text(-0.5, 0, 27, 'Scenario A', weight='bold', fontsize=18, color = args.color)
    ax0.set_zlabel('Free energy ($ kT$)',
                    fontsize='10', fontweight='bold', color = args.color)   
    change_color(ax0, args.color)

    # Plott the minimum enery path


    #####################################################################
    #                                                                   #
    #  Scenario B: A free energy barrier present for all lambda states  #
    #                                                                   #
    #####################################################################
    ax1 = fig.add_subplot(132, projection='3d')
    coef_end = [-0.000481992, 0.0133127, -0.102597,
                  -0.0406179, 2.84049, -7.5026, 6.84595]  # we keep other coefs the same

    Z1 = copy.deepcopy(Z)   # below we modify the free energy surface from the template
    Z1[5] = FES(coef_mid, x)
    delta_start_mid = (Z1[5] - Z1[0]) / 5
    for i in np.arange(0, 5, 1):
        Z1[i] = Z1[0] + delta_start_mid * i - 2 * np.random.rand(1, len(Z1[i]))
    Z1[10] = FES(coef_end, x)
    delta_mid_end = (Z1[10] - Z1[6]) / 5
    for i in np.arange(1, 10, 1):
        Z1[i] = Z1[1] + delta_mid_end * i - (6 * np.random.rand(1, len(Z1[i])) - 3)
    Z1 -= np.min(Z1)

    surf = ax1.plot_surface(X, Y, Z1, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax1.view_init(elev=30, azim=-60)
    ax1.set_xlabel('Collective variable', fontsize='10', fontweight='bold', color=args.color)
    ax1.set_xlim3d(0, 13)
    ax1.set_ylabel('Alchemical variable',
                    fontsize='10', fontweight='bold', color = args.color)
    ax1.set_ylim3d(0, 1)
    ax1.set_zlim3d(0, 40)
    ax1.text(-0.5, 0, 60, 'Scenario B', weight='bold', fontsize=18, color=args.color)
    ax1.set_zlabel('Free energy ($ kT$)',
                    fontsize='10', fontweight='bold', color=args.color)
    change_color(ax1, args.color)


    #################################################################
    #                                                               #
    #  Scenario C: Deep free energy basins in the alchemical space  #
    #                                                               #
    #################################################################
    ax2 = fig.add_subplot(133, projection='3d')
    coef_end = [0.0000879645, -0.00136518, -0.016613,
                0.420782, -2.41395, 2.95784, 7.93313]

    Z2 = copy.deepcopy(Z)
    Z2[5] = FES(coef_mid, x)
    delta_start_mid = (Z2[5] - Z2[0]) / 5
    for i in np.arange(0, 5, 1):
        Z2[i] = Z2[0] + delta_start_mid * i - np.random.rand(1, len(Z2[i]))
    Z2[10] = FES(coef_end, x)
    delta_mid_end = (Z2[10] - Z2[6]) / 5
    for i in np.arange(6, 10, 1):
        Z2[i] = Z2[6] + delta_mid_end * i - np.random.rand(1, len(Z2[i]))
    Z2 -= np.min(Z2)

    surf = ax2.plot_surface(X, Y, Z2, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax2.view_init(elev=30, azim=-60)
    ax2.set_xlabel('Collective variable', fontsize='10', fontweight='bold', color = args.color)
    ax2.set_xlim3d(0, 13)
    ax2.set_ylabel('Alchemical variable',
                    fontsize='10', fontweight='bold', color = args.color)
    ax2.set_ylim3d(0, 1)
    ax2.set_zlim3d(0, 40)
    ax2.text(-0.5, 0, 60, 'Scenario C', weight='bold', fontsize=18, color = args.color)
    ax2.set_zlabel('Free energy ($ kT$)',
                    fontsize='10', fontweight='bold', color = args.color)   
    change_color(ax2, args.color)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('FES_scenarios.png', dpi=600, transparent=args.transparent)
    
