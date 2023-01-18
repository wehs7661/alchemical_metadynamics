import os
import sys
import time
import glob
import natsort
import argparse
import plumed
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib import rc


def initialize():
    parser = argparse.ArgumentParser(
        description="This code plots the angle and dihedral angle distribution for two simulations."
    )
    parser.add_argument(
        "-f",
        "--folders",
        required=True,
        nargs=2,
        help="The two folders where the outputs of the two simulations reside."
        "This must be specified if the paths to the xtc/top files are not specified.",
    )
    parser.add_argument("-x", "--xtc", nargs=2, help="The paths to the two xtc files.")
    parser.add_argument(
        "-t",
        "--top",
        help="The topology file where angle/dihedrla information is from. "
        "Note that the angle/dihedral information of the two simulations should be the same.",
    )
    parser.add_argument(
        "-r",
        "--rerun",
        default=False,
        action="store_true",
        help="Whether to rerun the plumed driver or not. If not, then what the code does is just replot the data, if given.",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        help="The common prefix of the file name of the output figures.",
    )
    parser.add_argument(
        "-o", "--outdir", default="distribution_analysis", help="The output directory."
    )

    args_parse = parser.parse_args()

    return args_parse


class Logging:
    def __init__(self, outfile):
        self.outfile = outfile

    def logger(self, *args, **kwargs):
        """
        This function prints a string on screen and to a file.
        """
        print(*args, **kwargs)
        with open(self.outfile, "a") as f:
            print(file=f, *args, **kwargs)


def get_atom_indices(top_file):
    """
    Gets the atom indices of all angles/dihedrals from a topology file.

    Parameters
    ----------
    top_file (str): The filename of the topology.

    Returns
    -------
    angle_indices (list): The indices of all angles.
    dihedral_indices (list): The indices of all dihedrals.
    """
    infile = open(top_file, "r")
    lines = infile.readlines()
    infile.close()

    n = -1  # line indices (=line number -1)
    angle_start, dihedral_start = False, False
    angle_indices, dihedral_indices = [], []
    for line in lines:
        n += 1
        if "[ angles ]" in line:
            angle_start = True
        if "[ dihedrals ]" in line:
            dihedral_start = True

        if angle_start is True and line[0] != ";" and line[0] != "[":
            if len(line.split()) == 0:
                angle_start = False
            else:
                angle_line = line.split()[:3]
                angle_indices.append([int(i) for i in angle_line])

        if dihedral_start is True and line[0] != ";" and line[0] != "[":
            if len(line.split()) == 0:
                dihedral_start = False
            else:
                dihedral_line = line.split()[:4]
                # Note that atom indices might be repeptitive for different dihedrals
                if [int(i) for i in dihedral_line] not in dihedral_indices:
                    dihedral_indices.append([int(i) for i in dihedral_line])

    return angle_indices, dihedral_indices


def write_plumed_input(indices, output_file, outdir):
    """
    Writes the PLUMED input file for running the plumed driver.

    Parameters
    ----------
    indices (list): A list of indices of a certain angle/dihedral.
    output_file (str): The file name of the output of plumed driver.
    """
    str1 = ",".join([str(i) for i in indices])

    if len(indices) == 3:  # angle atom indices
        plumed_input = open(f"{outdir}/plumed_angle.dat", "w")
        plumed_input.write(f"theta: ANGLE ATOMS={str1}\n")
        plumed_input.write(f"PRINT ARG=theta STRIDE=10 FILE={outdir}/angle/{output_file}")
        plumed_input.close()

    elif len(indices) == 4:  # dihedral atom indices
        plumed_input = open(f"{outdir}/plumed_dihedral.dat", "w")
        plumed_input.write(f"theta: TORSION ATOMS={str1}\n")
        plumed_input.write(f"PRINT ARG=theta STRIDE=10 FILE={outdir}/dihedral/{output_file}")
        plumed_input.close()


def run_plumed_driver(idx_list, trajs, key_1, key_2, outdir):
    """
    Runs the plumed driver to calculate a CV as a function given trajectories of interest.

    Parameters
    ----------
    idx_list (list): A list of indices of all angles/dihedrals
    trajs (str): A list of trajectories filenames as the input to the plumed driver.
    key_1, key_2 (str): Suffices for the filename of the PLUMED output file.
    """
    if len(idx_list[0]) == 3:
        a_type = "angle"  # angle type
    elif len(idx_list[0]) == 4:
        a_type = "dihedral"

    for i in range(len(idx_list)):
        output_str = "_".join([str(i) for i in idx_list[i]])
        for j in trajs:
            if key_1 in j:
                suffix = "stateA"
            elif key_2 in j:
                suffix = "stateB"
            output = f"{a_type}_{output_str}_{suffix}.dat"
            write_plumed_input(idx_list[i], output, outdir)
            os.system(
                f"plumed driver --mf_xtc {j} --plumed {outdir}/plumed_{a_type}.dat --timestep 2"
            )

def plot_distribution(data_file):
    """
    Plots the angle or dihedral distribution given a PLUMED output file.

    Parameters
    ----------
    data_file (str): The filename of the output of fthe plumed driver.
    """
    if "stateA" in data_file:
        l_type = "state A"
    elif "stateB" in data_file:
        l_type = "state B"

    data = plumed.read_as_pandas(data_file)
    theta = np.array(data.iloc[:, 1]) * 180 / np.pi

    plt.hist(theta, bins=100, density=True, alpha=0.5, label=l_type)


def get_fig_dimension(n_subplots):
    """
    Gets the dimension of the figure given the number of subplots. The figure
    will be as close as to a square as possible.

    Parameters
    ----------
    n_subplots (int): The number of subplots.

    Returns
    -------
    n_rows (int): The number of rows in the figure.
    n_cols (int): The number of columns in the figure.
    """
    if int(np.sqrt(n_subplots) + 0.5) ** 2 == n_subplots:
        # perfect square number
        n_cols = int(np.sqrt(n_subplots))
    else:
        n_cols = int(np.floor(np.sqrt(n_subplots))) + 1

    if n_subplots % n_cols == 0:
        n_rows = int(n_subplots / n_cols)
    else:
        n_rows = int(np.floor(n_subplots / n_cols)) + 1

    return n_cols, n_rows


def ks_test(data_dir):
    files = glob.glob(f"{data_dir}/*")
    files = natsort.natsorted(files)
    n = int(len(files) / 2)
    for i in range(n):
        f_list = files[2 * i : 2 * (i + 1)]
        data_1, data_2 = plumed.read_as_pandas(f_list[0]), plumed.read_as_pandas(
            f_list[1]
        )
        theta_1, theta_2 = (
            np.array(data_1.iloc[:, 1]) * 180 / np.pi,
            np.array(data_2.iloc[:, 1]) * 180 / np.pi,
        )
        d_statistics, p_value = stats.kstest(theta_1, theta_2)

        L.logger(f"Comparing the data distributions in {f_list[0]} and {f_list[1]} ...")
        L.logger(
            "Null hypothesis: The distributions obtained from the two files are consistent with each other."
        )
        L.logger(f"p-value: {p_value}")
        if p_value > 0.05:
            L.logger(
                "Interpretation: The two distributions are consistent with each other.\n"
            )
        else:
            L.logger(
                "Interpretation: The two distributions are not consistent with each other.\n"
            )


def plot_all_distributions(data_dir, fig_name):
    files = glob.glob(f"{data_dir}/*")
    files = natsort.natsorted(files)
    if "angle" in files[0]:
        a_type = "angle"
    elif "dihedral" in files[0]:
        a_type = "dihedral"
    a_str = a_type[0].upper() + a_type[1:]
    x_label = a_str + " (deg)"
    n_subplots = int(len(files) / 2)
    n_cols, n_rows = get_fig_dimension(n_subplots)

    if n_subplots >= 9:
        fig = plt.figure(figsize=(12, 8))
        fontsize = 8
        fontsize_tick = 6
        fontsize_legend = 4
    else:
        fig = plt.figure()
        fontsize = 12
        fontsize_tick = 10
        fontsize_legend = 8

    for i in range(n_subplots):
        f_list = files[2 * i : 2 * (i + 1)]
        plt.subplot(n_rows, n_cols, i + 1)
        plot_distribution(f_list[1])
        plot_distribution(f_list[0])

        if a_type == "angle":
            indices = [int(i) for i in f_list[0].split('/')[-1].split("_")[1:4]]
        elif a_type == "dihedral":
            indices = [int(i) for i in f_list[0].split('/')[-1].split("_")[1:5]]
        idx_str = "-".join([str(i) for i in indices])

        plt.xlabel(x_label, fontsize=fontsize)
        plt.ylabel("P.D.F.", fontsize=fontsize)
        plt.xticks(fontsize=fontsize_tick)
        plt.yticks(fontsize=fontsize_tick)
        # plt.title(f'{a_str} {idx_str}', fontsize=fontsize, weight='bold')

        plt.grid()
        plt.legend(prop={"size": fontsize_legend})

    plt.suptitle(
        f"The {a_type} distributions of simulations starting from different states",
        fontsize=12,
        weight="bold",
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(fig_name, dpi=600)


class ImproperlyConfigured(Exception):
    """The given configuration is incomplete or otherwise not usable."""

    pass


if __name__ == "__main__":
    t1 = time.time()
    args = initialize()
    
    if args.xtc is None:
        trajs = [
            *glob.glob(f"{args.folders[0]}/*xtc"),
            *glob.glob(f"{args.folders[1]}/*xtc"),
        ]
        if len(trajs) != 2:
            raise ImproperlyConfigured(
                "Incorrect number of xtc files collected. Please specify the paths to the xtc files."
            )

    if args.top is None:
        top = glob.glob(f"{args.folders[0]}/*top")
        if len(top) != 1:
            raise ImproperlyConfigured(
                f"More than 1 topology file found in folder {args.folders[0]}"
            )
        else:
            top = top[0]

    if args.rerun is True:
        try:
            os.system(f"rm -r {args.outdir}/angle")
            os.system(f"rm -r {args.outdir}/dihedral")
        except:
            pass
        os.makedirs(f"{args.outdir}/angle")
        os.makedirs(f"{args.outdir}/dihedral")

        angle, dihedral = get_atom_indices(top)

        key_1 = "".join(set(trajs[0]) - set(trajs[0]).intersection(trajs[1]))
        key_2 = "".join(set(trajs[1]) - set(trajs[0]).intersection(trajs[1]))

        run_plumed_driver(angle, trajs, key_1, key_2, args.outdir)
        run_plumed_driver(dihedral, trajs, key_1, key_2, args.outdir)

    L = Logging(f"{args.outdir}/distribution_analysis.txt")
    L.logger(f'Command line: {" ".join(sys.argv)}')

    # Plot the figures!
    rc("font", **{"family": "sans-serif", "sans-serif": ["DejaVu Sans"], "size": 10})
    # Set the font used for MathJax - more on this later
    rc("mathtext", **{"default": "regular"})
    plt.rc("font", family="serif")


    plot_all_distributions(
        f"{args.outdir}/angle", f"{args.outdir}/{args.prefix}_angle_distributions.png"
    )
    plot_all_distributions(
        f"{args.outdir}/dihedral", f"{args.outdir}/{args.prefix}_dihedral_distributions.png"
    )

    ks_test(f"{args.outdir}/angle")
    ks_test(f"{args.outdir}/dihedral")

    t2 = time.time()
    L.logger(f"Elapsed time: {t2 - t1: 2f} seconds.")

