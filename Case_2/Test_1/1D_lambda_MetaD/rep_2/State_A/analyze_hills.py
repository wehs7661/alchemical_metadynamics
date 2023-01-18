import glob
import time
import plumed
import natsort
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from pymbar import timeseries


def initialize():
    parser = argparse.ArgumentParser(
        description="Thie code analyzes the convergence of a metadynamics simulation."
    )
    parser.add_argument(
        "-hh",
        "--hills",
        default=natsort.natsorted(glob.glob("HILLS*"))[0],
        help="The HILLS file output by the metadynamics simulation.",
    )
    parser.add_argument(
        "-p",
        "--param",
        required=True,
        help="The name of the CV that serves as the parameter of the plot of hills time series.",
    )
    parser.add_argument(
        "-c",
        "--conv",
        choices=[
            "degree to radian",
            "radian to degree",
            "kT to kcal/mol",
            "kcal/mol to kT",
            "kT to kJ/mol",
            "kJ/mol to kT",
            "kJ/mol to kcal/mol",
            "kcal/mol to kJ/mol",
            "ns to ps",
            "ps to ns",
        ],
        help="The unit conversion for the parameter.",
    )
    parser.add_argument(
        "-f", "--factor", help="The conversion factor for the parameter."
    )
    parser.add_argument(
        "-t",
        "--temp",
        default=298.15,
        help="Temperature of the simulation. This is for convering the units of Gaussian height into kT.",
    )
    parser.add_argument(
        "-d",
        "--discrete",
        default=False,
        action="store_true",
        help="Whether the data of the parameter is discrete.",
    )
    parser.add_argument(
        "-nb", "--nbins", type=int, help="The number of bins for the parameter"
    )
    parser.add_argument(
        "-n", "--notation", help="The notation of the parameter shown in the legend."
    )

    args_parse = parser.parse_args()

    return args_parse


class ImproperlyConfigured(Exception):
    """The given configuration is incomplete or otherwise not usable."""

    pass


def scale_data(data, conversion=None, factor=None, T=298.15):
    """
    This function scales the input data according to the desired unit conversion
    or scaling factor specified by the user.

    Parameters
    ----------
    data : numpy.ndarray
        The input data to be scaled.
    conversion : str
        The string describing what units the conversion should be carried out between.
        Available conversions include "ps to ns", "kT to kJ/mol", "kT to kcal/mol",
        "kJ/mol to kcal/mol", "degree to radian", and their respective conversion in
        the opposite direction. Note that the list of available conversions does not
        mean to be comprehensive since the user could just specify the scaling factor.
    factor : float
        The scaling factor for data scaling.
    T : float
        The temperature to be considered to convert energy units to kT or vice versa.

    Returns
    -------
    data : numpy.ndarray
        The processed data.
    """
    c1 = 1.38064852 * 6.022 * T / 1000  # multiply to convert from kT to kJ/mol
    c2 = np.pi / 180  # multiply to convert from degree to radian
    c3 = 0.239005736  # multiply to convert from J to cal (or kJ/mol to kcal/mol)

    conversion_dict = {
        "ns to ps": 1000,
        "ps to ns": 1 / 1000,
        "kT to kJ/mol": c1,
        "kJ/mol to kT": 1 / c1,
        "kT to kcal/mol": c1 * c3,
        "kcal/mol to kT": 1 / (c1 * c3),
        "kJ/mol to kcal/mol": c3,
        "kcal/mol to kJ/mol": 1 / c3,
        "degree to radian": c2,
        "radian to degree": 1 / c2,
    }

    if conversion is not None:
        if conversion in conversion_dict:
            data *= conversion_dict[conversion]
        else:
            raise utils.ParameterError(
                "The specified conversion is not available. \
                                 Try using the scaling factor. "
            )

    if factor is None:
        factor = 1

    data *= factor

    return data


def color_graident(n, cmap=plt.cm.jet):
    first, last = 225, 50
    colors = np.array([cmap(i) for i in np.linspace(first, last, n).astype(int)])

    return colors


if __name__ == "__main__":
    args = initialize()
    if args.notation is None:
        args.notation = args.param
    if args.discrete is False and args.nbins is None:
        raise ImproperlyConfigured(
            "The number of bins should be specified if the parameter data is continuous."
        )
    c1 = 1.38064852 * 6.022 * args.temp / 1000  # mutiply to convert from kT to kJ/mol

    hills_data = plumed.read_as_pandas(args.hills)
    time = np.array(hills_data["time"]) / 1000  # units: ns
    height = np.array(hills_data["height"]) / c1  # units: kT
    param = np.array(hills_data[f"{args.param}"])
    param = scale_data(param, args.conv, args.factor)

    # Plot Gaussian height as a function of time with each CV as the parameter
    rc("font", **{"family": "sans-serif", "sans-serif": ["DejaVu Sans"], "size": 10})
    # Set the font used for MathJax - more on this later
    rc("mathtext", **{"default": "regular"})
    plt.rc("font", family="Serif")

    grouped_data = []   # for further analysis if needed

    plt.figure()
    if args.discrete is True:
        n = len(np.unique(param))
        colors = color_graident(n)
        for i in np.sort(np.unique(param)):
            grouped_data.append(height[param == i])
            plt.scatter(
                time[param == i],
                height[param == i],
                marker=".",
                label=f"{args.notation}={i:.0f}",
                color=colors[i],
                alpha=0.5,
            )
    else:
        n = args.nbins
        colors = color_graident(n)
        bins = np.histogram(param, bins=args.nbins)[1]
        for i in range(len(bins) - 1):
            mask = np.logical_and(param > bins[i], param < bins[i + 1])
            grouped_data.append(height[mask])
            plt.scatter(
                time[mask],
                height[mask],
                marker=".",
                label=f"{bins[i]:.1f} < {args.notation} < {bins[i + 1]:.1f}",
                color=colors[i],
                alpha=0.5,
            )
    plt.legend(ncol=n // 10 + 1)
    plt.xlabel("Time (ns)")
    plt.ylabel("Hill height (kT)")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"hills_{args.param}", dpi=600)

