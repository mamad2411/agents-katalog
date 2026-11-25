---
name: autoresearch-loop
description: Karpathy's autoresearch loop for metric-optimization experiments — modify one file, run for a fixed budget, keep if the metric improves, git reset if not, log to results.tsv, never stop until interrupted. Use when an experiment has one number to drive and a fixed-cost run; adapt program.md to the codebase (rename train.py/prepare.py, the metric, the budget) and follow it verbatim.
---

# Autoresearch loop (Karpathy)

`program.md` in this directory is the original agent instruction file from
[karpathy/autoresearch](https://github.com/karpathy/autoresearch) (MIT), unmodified.
It is the reference pattern for the **inner loop** of the `autoresearch` skill's
optimization mode.

To use it on a new problem, copy `program.md` into the experiment directory and edit
only the specifics:

- the file the agent may edit (`train.py`) and the files it may not (`prepare.py`)
- the metric line to grep for and its direction
- the fixed run budget and the timeout
- the `results.tsv` columns if the run prints different numbers

Keep the rules: baseline first, one change per commit, keep/discard by the metric,
simpler wins ties, redirect run output to a log file, and do not stop to ask.
