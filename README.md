# Lab 8: Sim-to-Real PID Analysis on Crazyflie Hardware: [Your Name]

ECE 383 / ME 555: Introduction to Robotics and Automation (Fall 2026)

Update this README with your name, NetID, and the one command that runs your
analysis script.

## Contents

- `analysis/lab08_analysis.py`: your analysis script. `load_run`,
  `load_waypoints`, and `split_legs` are provided. Complete the functions marked TODO.
- `data/`: course staff add your run folder (`data/YOUR_GITHUB_USERNAME/`) and
  the baseline folder (`data/baseline/`) after staff record your flight. Do not edit these folders.
- `docs/`: save the three figures named in the manual here using your script.

## Run the analysis

From the repository root in the container:

```bash
python3 analysis/lab08_analysis.py --run data/YOUR_GITHUB_USERNAME --baseline data/baseline --outdir docs
```

Course staff grade your Gradescope PDF and this repository. The command above
must regenerate your figures and metrics table from the files in `data/`.
