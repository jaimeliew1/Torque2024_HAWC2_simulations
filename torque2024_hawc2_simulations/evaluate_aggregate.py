from pathlib import Path
from TSAR import TimeSeriesAggregator
import polars as pl

RESDIR = Path("DTU_10_MW_Reference_Wind_Turbine_v_9-1/res")
OUT_FN = Path("pitch_tsr_HAWC2.csv")

channels = {
    "omega": 10,
    "pitch": 4,
    "torque": 11,
    "power": 12,
    "thrust": 13,
    "wsp": 15,
    "pelec": 61,
}

pattern = "pitch{pitch}_tsr{tsr}_yaw{yaw}.hdf5"


if __name__ == "__main__":
    agg = TimeSeriesAggregator(RESDIR, channels, pattern)
    agg.add("mean", ["torque", "power", "thrust", "omega"])
    agg.run_par(tstart=80)
    df = agg.to_dataframe()

    df = (
        pl.from_pandas(
            df,
        )
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
    df.write_csv(OUT_FN)
