from pathlib import Path

import polars as pl
import matplotlib.pyplot as plt
import numpy as np


FIGDIR = Path("fig")
FIGDIR.mkdir(parents=True, exist_ok=True)

DATA_FN = Path("pitch_tsr_HAWC2.csv")


if __name__ == "__main__":
    df = (
        pl.read_csv(DATA_FN)
        .select(pl.exclude("", "chunk"))
        .rename(
            {
                "torque_mean": "torque",
                "power_mean": "power",
                "thrust_mean": "thrust",
                "omega_mean": "omega",
            }
        )
    )
    print(df)

    df_piv = df.filter(pl.col("yaw") == 45).pivot(
        index="tsr", columns="pitch", values="power", sort_columns=True,
    ).sort("tsr")
    # df_piv = df_piv.select("tsr", pl.col(sorted(df.columns[1:])))
    print(df_piv)

    tsr = df_piv["tsr"].to_numpy()/2
    pitch = np.array(df_piv.columns[1:], dtype=float)
    Z = df_piv.to_numpy()[:, 1:]
    Z[Z < 0] = 0.01

    # ax.set_title(surface_label[key])

    fig, ax = plt.subplots()
    ax.plot(-df["pitch"], df["tsr"]/2, ".k")
    ax.contourf(-pitch, tsr, Z, cmap="viridis")
    # CS = ax.contour(-pitch, tsr, Z, colors="k", linewidths=0.8)
    # ax.clabel(CS, inline=True, fontsize=10)

    plt.ylim(5, 12)
    plt.xlim(-15, 15)
    plt.savefig(FIGDIR / "contour.png", dpi=500, bbox_inches="tight")
