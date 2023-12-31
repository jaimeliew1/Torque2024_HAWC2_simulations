from pathlib import Path
from TSAR import HAWC2IO
import matplotlib.pyplot as plt
from foreach import foreach

FIGDIR = Path("fig")
FIGDIR.mkdir(parents=True, exist_ok=True)

RESDIR = Path("DTU_10_MW_Reference_Wind_Turbine_v_9-1/res")


channels = {
    "omega": 10,
    "pitch": 4,
    "torque": 11,
    "power": 12,
    "thrust": 13,
    "wsp": 15,
    "pelec": 61,
}


def plot(fn):
    df = HAWC2IO.read(fn, channels)

    fig, axes = plt.subplots(len(channels), 1, sharex=True)
    for channel, ax in zip(channels.keys(), axes):
        ax.plot(df.index, df[channel])
        ax.set_ylabel(channel)

    plt.savefig(FIGDIR / f"{fn.stem}.png", bbox_inches="tight", dpi=500)
    plt.close()


if __name__ == "__main__":
    filelist = list(RESDIR.glob("*yaw0.00.hdf5"))

    foreach(plot, filelist)
