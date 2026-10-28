#!/usr/bin/env python3
"""Lab 8: compare your Crazyflie flight with the baseline flight.

Usage, from the repository root in the container:
    python3 analysis/lab08_analysis.py --run data/YOUR_GITHUB_USERNAME --baseline data/baseline --outdir docs

load_run, load_waypoints, and split_legs are provided. Complete the
functions marked TODO. Part numbers refer to the Lab 8 manual.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml


def load_run(folder: str) -> pd.DataFrame:
    """Read folder/trajectory_log.csv and drop rows with missing goal coordinates (NaN) (Part 2)."""
    df = pd.read_csv(Path(folder) / "trajectory_log.csv")
    return df.dropna(subset=["gx", "gy", "gz"]).reset_index(drop=True)


def load_waypoints(folder: str) -> np.ndarray:
    """Read folder/course_waypoints.yaml and return one row of x, y, z per waypoint."""
    data = yaml.safe_load((Path(folder) / "course_waypoints.yaml").read_text())
    return np.array(data["waypoints"], dtype=float)[:, :3]


def split_legs(df: pd.DataFrame, waypoints: np.ndarray) -> list[dict]:
    """Split the recording into one segment per waypoint (Part 3).

    Return one dictionary per segment:
        waypoint   the destination waypoint number (1 to 13)
        axis       the commanded axis of travel: "x", "y" or "z" (None for waypoint 1)
        direction  +1 or -1, the direction of travel along that axis (0 for waypoint 1)
        first      the segment's first row in df
        last       the segment's last row in df
    """
    goals = df[["gx", "gy", "gz"]].to_numpy()
    starts = [0] + [i for i in range(1, len(goals)) if not np.allclose(goals[i], goals[i - 1])]
    ends = starts[1:] + [len(df)]
    legs = []
    index = 0  # Search in course order because waypoints 1 and 13 are the same point.
    for first, end in zip(starts, ends):
        while not np.allclose(waypoints[index], goals[first], atol=0.001):
            index += 1
            if index == len(waypoints):
                raise ValueError(f"goal {goals[first]} at row {first} matches no remaining waypoint")
        number = index + 1
        if index == 0:
            axis, direction = None, 0
        else:
            step = waypoints[index] - waypoints[index - 1]
            k = int(np.argmax(np.abs(step)))
            axis, direction = "xyz"[k], int(np.sign(step[k]))
        legs.append({"waypoint": number, "axis": axis, "direction": direction,
                     "first": first, "last": end - 1})
        index += 1
    return legs


def apply_filter(df: pd.DataFrame) -> pd.DataFrame:
    """TODO: return a copy with x, y, z filtered (Part 2)."""
    raise NotImplementedError("apply_filter: see Part 2 of the manual")


def leg_metrics(df: pd.DataFrame, legs: list[dict], i: int) -> dict:
    """TODO: return leg time, rise time, overshoot, off-path RMS, and height error RMS for legs[i] (Part 4)."""
    raise NotImplementedError("leg_metrics: see Part 4 of the manual")


def course_time(folder: str) -> float:
    """TODO: read and return the course time from folder/launch.log (Part 4)."""
    raise NotImplementedError("course_time: see Part 4 of the manual")


def metrics_table(run_rows: list[dict], base_rows: list[dict]) -> pd.DataFrame:
    """TODO: return a table with columns metric, leg, baseline, yours, delta, pct_delta (Part 5)."""
    raise NotImplementedError("metrics_table: see Part 5 of the manual")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", required=True, help="your run folder, data/YOUR_GITHUB_USERNAME")
    parser.add_argument("--baseline", required=True, help="the baseline folder, data/baseline")
    parser.add_argument("--outdir", default="docs")
    args = parser.parse_args()
    Path(args.outdir).mkdir(exist_ok=True)

    run, base = load_run(args.run), load_run(args.baseline)
    run_legs = split_legs(run, load_waypoints(args.run))
    base_legs = split_legs(base, load_waypoints(args.baseline))
    print("your flight:", [leg["waypoint"] for leg in run_legs])
    print("baseline:   ", [leg["waypoint"] for leg in base_legs])
    # TODO: filter, measure each horizontal leg, save the three figures in args.outdir,
    # and print and save the metrics table.


if __name__ == "__main__":
    main()
