# MNE Connectivity Graph Starter

Use this skill to build a tiny EEG connectivity graph with `mne` and `mne-connectivity`.

## What it does

- Creates deterministic toy epochs with three EEG channels.
- Computes alpha-band coherence with `spectral_connectivity_epochs`.
- Converts the resulting matrix into a thresholded edge list and writes a compact JSON summary.

## When to use it

- You need a verified starter for connectomics or graph-style neuroimaging analysis.
- You want a compact example of spectral connectivity before moving to real EEG/MEG datasets.
- You need stable graph summary fields for tests or demos.

## Example

```bash
slurm/envs/neuro/bin/python skills/neuroscience-and-neuroimaging/mne-connectivity-graph-starter/scripts/run_mne_connectivity_graph.py \
  --out scratch/neuro/mne_connectivity_graph_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/neuroscience-and-neuroimaging/mne-connectivity-graph-starter/tests -p 'test_*.py'`
- Expected summary: the strongest edge is `Fz -> Cz` and only one edge survives the default `0.5` threshold
