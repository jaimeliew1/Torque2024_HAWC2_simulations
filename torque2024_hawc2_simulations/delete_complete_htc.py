from pathlib import Path
import click
from tqdm import tqdm

LOGDIR = Path("DTU_10_MW_Reference_Wind_Turbine_v_9-1/log")
HTCDIR = Path("DTU_10_MW_Reference_Wind_Turbine_v_9-1/htc")


def check_complete(fn_log: Path) -> bool:
    with open(fn_log) as f:
        lines = f.readlines()
        if len(lines) == 0:
            return False
    return "Elapsed" in lines[-1]


if __name__ == "__main__":
    complete_stems = [
        fn.stem for fn in tqdm(LOGDIR.glob("*.log")) if check_complete(fn)
    ]

    htc_to_delete = [fn for fn in HTCDIR.glob("*.htc") if fn.stem in complete_stems]
    if click.confirm(
        f"{len(htc_to_delete)} htc files to delete. Continue?", default=False
    ):
        for fn in htc_to_delete:
            if fn.exists():
                fn.unlink()
                print(f"{fn} has been deleted.")
    else:
        print("Operation canceled.")
