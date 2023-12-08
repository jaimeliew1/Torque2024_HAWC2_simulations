from pathlib import Path
from itertools import product
from typing import Callable
from jinja2 import Template, StrictUndefined
import numpy as np
import polars as pl
from tqdm import tqdm

TEMPLATE_FN = Path(__file__).parent / "DTU_10MW_RWT_template.htc.j2"
OUT_DIR = Path(__file__).parent.parent / "DTU_10_MW_Reference_Wind_Turbine_v_9-1/htc/"
print(OUT_DIR)


def generate_single_htc(context: dict, out_fn: Path, template: Template) -> str:
    text = template.render(**context)

    out_fn.parent.mkdir(exist_ok=True, parents=True)
    with open(out_fn, "w") as f:
        f.write(text)

    return text


def generate_params(
    constants: dict, variables: dict[str, list], functionals: dict[str, Callable]
) -> pl.DataFrame:
    keys = list(variables.keys())
    dicts = []
    for param_tuple in product(*variables.values()):
        row = constants | {k: v for k, v in zip(keys, param_tuple)}
        row_funcs = {k: func(row) for k, func in functionals.items()}
        dicts.append(row | row_funcs)

    return pl.from_dicts(dicts)


def generate_from_template(
    template_fn: Path,
    out_dir: Path,
    variables: dict,
    constants: dict = {},
    functionals: dict = {},
) -> pl.DataFrame:
    df = generate_params(constants, variables, functionals)

    with open(template_fn) as f:
        template = Template(f.read(), undefined=StrictUndefined)

    for row in tqdm(df.iter_rows(named=True), total=len(df)):
        out_fn = out_dir / (row["filestem"] + ".htc")
        generate_single_htc(row, out_fn, template)

    return df


if __name__ == "__main__":
    constants = {"R": 178}  # Radius from controller setting
    variables = {
        "wsp": [5],
        "pitch": np.arange(-15, 15, 1),
        "yaw": np.arange(0, 60, 5),
        "tsr": np.arange(5, 24, 0.5),
    }
    functionals = {
        "filestem": lambda x: f"pitch{x['pitch']:.2f}_tsr{x['tsr']:.2f}_yaw{x['yaw']:.2f}"
    }
    df = generate_from_template(TEMPLATE_FN, OUT_DIR, variables, constants, functionals)

    print(df)
