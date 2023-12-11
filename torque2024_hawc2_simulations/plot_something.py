from pathlib import Path

import polars as pl
import matplotlib.pyplot as plt
import numpy as np


FIGDIR = Path("fig")
FIGDIR.mkdir(parents=True, exist_ok=True)

DATA_FN = Path("pitch_tsr_HAWC2.csv")

power_normaliser = 0.5 * 1.225 * np.pi * 89**2 * 5**3 / 1000
if __name__ == "__main__":
    # Load aggregated data.
    df = pl.read_csv(DATA_FN).with_columns(
        (pl.col("power") / power_normaliser).alias("Cp")
    )

    print(df)

    # Pivot
    df_piv = (
        df.filter(pl.col("yaw") == 0)
        .sort(["pitch", "tsr"])
        .pivot(
            index="tsr",
            columns="pitch",
            values="Cp",
        )
        .sort(["tsr"])
    )

    tsr = df_piv["tsr"].to_numpy() / 2
    pitch = np.array(df_piv.columns[1:], dtype=float)
    Z = df_piv.to_numpy()[:, 1:]
    Z[Z < 0] = 0.01

    # Plot
    fig, ax = plt.subplots()
    ax.contourf(-pitch, tsr, Z, cmap="viridis")
    CS = ax.contour(-pitch, tsr, Z, colors="k", linewidths=0.8)
    ax.clabel(CS, inline=True, fontsize=10)

    plt.ylim(5, 12)
    plt.xlim(-15, 15)
    plt.savefig(FIGDIR / "contour.png", dpi=500, bbox_inches="tight")
