#!/usr/bin/env python
"""This is a Python code for the plotting of 2-dimensional data.
"""

import argparse
import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


def initialize():

    parser = argparse.ArgumentParser(
        description='This code saves a contour plot based on 3-dimensional data')
    parser.add_argument('-f',
                        '--xvg',
                        nargs='+',
                        help='Names of the input .xvg files')
    parser.add_argument('-l',
                        '--legend',
                        default='label',
                        nargs='+',
                        help='Legends of the curves')
    parser.add_argument('-x',
                        '--xlabel',
                        type=str,
                        help='The name and units of x-axis')
    parser.add_argument('-y',
                        '--ylabel',
                        type=str,
                        help='The name and units of y-axis')
    parser.add_argument('-t', '--title', type=str, help='Title of the plot')
    parser.add_argument('-n',
                        '--pngname',
                        type=str,
                        help='The filename of the figure')

    args_parse = parser.parse_args()

    return args_parse


if __name__ == '__main__':

    args = initialize()

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    plt.figure()  # ready to plot!

    if isinstance(args.xvg, str):  # the case of only one input
        args.xvg = list(args.xvg)
        # for the case of only one input, the legend arugment takes the default
        # but will not be shown

    for i in range(len(args.xvg)):
        x, y = [], []
        infile = open('%s' % args.xvg[i], 'r')
        lines = infile.readlines()
        infile.close
        # Parse data
        n = 0
        m = 0
        for line in lines:
            if line[0] == '#' or line[0] == '@':
                m += 1  # number of parameter lines
        # read in data starting from (m+1)-th line to the end
        for line in lines[m:]:
            if line[0] != '#' and line[0] != '@':
                tokens = line.split()
                x.append(float(tokens[0]))
                y.append(float(tokens[1]))
        x, y = np.array(x), np.array(y)
        if i == 1:
            x *= 20

        if max(abs(x)) >= 10000:
            x = x / 1000
        T = 298.15
        conversion1 = 1.38064852 * 6.02 * T / 1000  # from kcal/mol to kT
        conversion2 = np.pi/180 # from radian to degree
        # x = x /conversion2
        # y = y / conversion1
        
        # find the x value which corrspond to a y value that is closet to the mean of y
        y_avg = np.mean(y[int(0.5 * len(y)):])
        y_avg = np.mean(y)
        diff = np.abs(y - y_avg)
        t_avg = x[np.argmin(diff)]
        print(y_avg)
        print(t_avg)
        print(y[np.argmin(diff)])

        plt.plot(x, y, label='%s' % args.legend[i])
        # plt.hold(True)

    plt.title('%s' % args.title)
    plt.xlabel('%s' % args.xlabel)
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ylabel('%s' % args.ylabel)
    if max(abs(y)) >= 10000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.grid(True)

    if len(args.xvg) > 1:
        plt.legend(ncol=2)

    # Save the image, but not overwrite the file with the same file name.
    # The name of the file should be 'pic.png', 'pic_1.png', ...
    n = 0   # number of the figures that have been produce in the same dir.
    if os.path.isfile('%s.png' % args.pngname):
        n += 1
        while os.path.isfile('%s_%s.png' % (args.pngname, n)):
            n += 1
        plt.savefig('%s_%s.png' % (args.pngname, n))
    plt.savefig('%s_0.png' % args.pngname)

    plt.show()


