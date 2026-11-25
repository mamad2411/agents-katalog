# MNE EEG Preprocessing Starter

Use this skill to create a tiny synthetic EEG recording with `MNE-Python`, apply a simple band-pass filter, and summarize the preprocessing effect.

## What it does

- Builds a deterministic two-channel `RawArray` with oscillatory signal plus low-frequency drift.
- Applies a basic `1-30 Hz` band-pass filter.
- Returns compact JSON with sampling rate, channel names, and before/after dispersion summaries.

## When to use it

- You need a runnable starter for `EEG / MEG preprocessing`.
- You want a verified local `MNE-Python` example before working on real electrophysiology recordings.

## Example

```bash
slurm/envs/neuro/bin/python skills/neuroscience-and-neuroimaging/mne-eeg-preprocessing-starter/scripts/run_mne_eeg_preprocessing.py \
  --out scratch/neuro/mne_preprocessing_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/neuroscience-and-neuroimaging/mne-eeg-preprocessing-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase31_frontier_leaf_conversion_skills -v`
