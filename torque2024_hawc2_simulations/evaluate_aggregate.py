from pathlib import Path
from TSAR import TimeSeriesAggregator

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

    print(df)

    df.to_csv(OUT_FN) # to do: convert to polars ans substitute column names

