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
    y = np.arange(0, 1.1, 0.01)
    X, Y = np.meshgrid(x, y)
    Z = FES(coef_start, X)

    ############################################################
    #                                                          #
    #  Scenario A: A free energy barrier that EXE can overcome #
    #                                                          #
    ############################################################
    
    # Step 1: Define the surface
    c1_start = [-0.000481992, 0.0133127, -0.102597,
                -0.0406179, 2.84049, -7.0026, 6.84595]
    Z1 = FES(c1_start, X)

    c1_end = [0.0000879645, -0.00136518, -0.016613,
            0.420782, -2.41395, 2.95784, 7.93313] # flip the sign and shift up
    Z1[-1] = FES(c1_end, x)

    delta_1 = (Z1[-1] - Z1[0]) / (len(Z1) - 1)   # delta (from start to end)
    for i in range(len(Z1) - 1):
        Z1[i] = Z1[0] + delta_1 * i # + 0.5 * (np.random.rand(1, len(Z1[i])) - 0.5)
    Z1 -= np.min(Z1)

    # Step 2: Plot the surface
    fig = plt.figure(figsize=(21, 6))
    ax0 = fig.add_subplot(131, projection='3d')
    surf = ax0.plot_surface(X, Y, Z1, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax0.view_init(elev=30, azim=-60)
    ax0.set_xlabel('Collective variable', fontsize='14', fontweight='bold', color = args.color)
    ax0.set_xlim3d(0, 13)
    ax0.set_ylabel('Alchemical variable',
                    fontsize='14', fontweight='bold', color = args.color)
    ax0.set_ylim3d(0, 1)
    ax0.set_zlim3d(0, 16)
    ax0.text(-2, 0, 24, 'Scenario A', weight='bold', fontsize=20, color = args.color)
    ax0.set_zlabel('Free energy ($ kT$)',
                    fontsize='14', fontweight='bold', color = args.color)   
    change_color(ax0, args.color)

    # Step 3: Plot the minimum enery path


    #####################################################################
    #                                                                   #
    #  Scenario B: A free energy barrier present for all lambda states  #
    #                                                                   #
    #####################################################################
    
    # Step 1: Define the surface
    c2_start = [-0.000481992, 0.0133127, -0.102597,
                -0.0406179, 2.84049, -7.0026, 6.84595]   # same as c1_start
    Z2 = FES(c2_start, X)

    c2_end = [-0.000481992, 0.0133127, -0.102597,
                -0.0406179, 2.84049, -7.5026, 6.84595]  # only the second last coef is different from c2_start
    Z2[-1] = FES(c2_end, x)
    Z2[-1] = 5 * np.sin(0.8 * x - np.pi)

    delta_2 = (Z2[-1] - Z2[0]) / (len(Z2) - 1)  # delta (from start to end)
    for i in range(len(Z2) - 1):
        Z2[i] = Z2[0] + delta_2 * i # + (np.random.rand(1, len(Z2[i])) - 0.5)
    Z2 -= np.min(Z2)

    # Step 2: Plot the surface
    ax1 = fig.add_subplot(132, projection='3d')
    surf = ax1.plot_surface(X, Y, Z2, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax1.view_init(elev=30, azim=-60)
    ax1.set_xlabel('Collective variable', fontsize='14', fontweight='bold', color=args.color)
    ax1.set_xlim3d(0, 13)
    ax1.set_ylabel('Alchemical variable',
                    fontsize='14', fontweight='bold', color = args.color)
    ax1.set_ylim3d(0, 1)
    ax1.set_zlim3d(0, 24)
    ax1.text(-2, 0, 36, 'Scenario B', weight='bold', fontsize=20, color=args.color)
    ax1.set_zlabel('Free energy ($ kT$)',
                    fontsize='14', fontweight='bold', color=args.color)
    change_color(ax1, args.color)


    #################################################################
    #                                                               #
    #  Scenario C: Deep free energy basins in the alchemical space  #
    #                                                               #
    #################################################################
    
    # Step 1: Define the surface
    Z3 = FES([0], X)  # flat surface to be modified
    mid = int((len(Z3) - 1) * 0.5)

    Z3[0] = 3 * np.sin(0.8 * x - np.pi)
    Z3[mid] = 10 * (np.sin(0.5 * x + 0.8 * np.pi) - 1)
    Z3[-1] = 3 * np.sin(x)
   
    diff_0 = Z3[mid] - Z3[0]
    for i in np.arange(0, mid, 1):
        # nonlinearly transform from "start" to "mid"
        Z3[i] = Z3[0] + diff_0 * (i / mid) ** 3  #+ (np.random.rand(1, len(Z3[i])) - 0.5)

    delta_3_mid = (Z3[-1] - Z3[mid]) / (len(y) - mid - 1)
    for i in np.arange(mid, len(y) - 1, 1):
        # Note taht here we add delta_3_mid * i instead of delta_3_mid * (i - mid) to create a different profile
        Z3[i] = Z3[mid] + delta_3_mid * (i - mid) #+ (np.random.rand(1, len(Z3[i])) - 0.5)
    
    Z3 -= np.min(Z3)

    # Step 2: Plot the surface
    ax2 = fig.add_subplot(133, projection='3d')
    surf = ax2.plot_surface(X, Y, Z3, rstride=2, cstride=1, cmap=plt.get_cmap(
            'viridis'), alpha=0.9, zorder=10)
    ax2.view_init(elev=30, azim=-60)
    ax2.set_xlabel('Collective variable', fontsize='14', fontweight='bold', color = args.color)
    ax2.set_xlim3d(0, 13)
    ax2.set_ylabel('Alchemical variable',
                    fontsize='14', fontweight='bold', color = args.color)
    ax2.set_ylim3d(0, 1)
    ax2.set_zlim3d(0, 40)
    ax2.text(-2, 0, 60, 'Scenario C', weight='bold', fontsize=20, color = args.color)
    ax2.set_zlabel('Free energy ($ kT$)',
                    fontsize='14', fontweight='bold', color = args.color)   
    change_color(ax2, args.color)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('FES_scenarios.png', dpi=600, transparent=args.transparent)

    # plt.show()