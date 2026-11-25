---
name: meltpool-geometry
description: Predict metal additive manufacturing melt-pool depth, width and length and melt-pool mode (keyhole, lack of fusion, balling, desirable) from laser/electron-beam power, speed, beam size and alloy properties, with Rosenthal estimates, dimensionally consistent power-law fits, and honest cross-study validation. Based on MeltpoolNet (Barati Farimani Lab). Use for melt-pool size estimates, single-track planning, absorptivity and Rosenthal calculations, or adapting a melt-pool model to your own machine with a few measured tracks.
---

# Melt-pool geometry (MeltpoolNet)

This skill estimates the melt pool for a metal AM parameter set with three tools that go from most
interpretable to most data-driven:
1. the **Rosenthal** point-source solution;
2. a **dimensionally consistent power law** fitted to experiments;
3. **ML models** trained on the MeltpoolNet benchmark (Akbari et al., *Additive Manufacturing* 55
   (2022) 102817).

All of it runs through `scripts/meltpool.py` (numpy, pandas, scipy, scikit-learn, matplotlib). The
data downloads on first use from github.com/BaratiLab/MeltpoolNet into
`~/.cache/mechanical-engineering-skills/meltpoolnet`, the same cache `lpbf-defect-prediction` uses.

Units: P in W, V in mm/s, beam/hatch/layer/melt-pool sizes in µm, ρ in kg/m³, Cp in J/kg·K, k in
W/m·K, melting T in K.

## Pick the tool

| Question | Command |
|---|---|
| Quick physics estimate, any alloy | `rosenthal --material SS316L --power 200 --velocity 800` (or `--props ρ,Cp,k,Tm --absorptivity η`) |
| An explicit, explainable formula from data | `identify --target depth\|width\|length` |
| Best-guess numbers for a known alloy | `train` once per target, then `predict --models depth.joblib,width.joblib ...` |
| How far can I trust it? | `benchmark --target depth --split paper [--calibrate 3] --plot parity.png` |
| Melt-pool mode | `classify --features baseline,onehot --split paper` |
| Adapt to *my* machine | `train ... --extra my_tracks.csv` (your measured single tracks, MeltpoolNet column names) |

Features (`--features`, comma list):
- `baseline`: P, V, ρ, Cp, k, Tm
- `energy`: line energy and normalized absorptivity
- `abs1`: paper Eq. 2; needs beam diameter and minimum absorptivity
- `abs2`: paper Eq. 3. It uses the **measured width**, so it leaks the label; avoid it.
- `hatch`, `layer`
- `onehot`: material
- `composition`: wt%
- `elemental`: composition-weighted element properties

## How to report a prediction
1. Give the ML number and the Rosenthal number side by side, plus W/D. W/D < 1.5 suggests keyhole
   mode (see `lpbf-defect-prediction`).
2. Quote the **leave-paper-out** validation stored in the model (`validation_paper_split`), not
   the random-split score.
   - Without any of the user's own data, a new machine is close to an unseen paper: depth R² ≈ 0
     on this data.
   - Say so, and recommend measuring 3–10 single tracks. Retrain with `--extra`; in benchmark terms
     that brings R² to about 0.5–0.7.
3. Flag inputs outside the training range (`outside_training_range`), unknown alloys (passed
   `--props`), and EBM vs. laser (the data is mostly SLM).

## Facts to keep straight
- The Rosenthal depth here uses Q = η_m·P (minimum absorptivity from the data), which is right for
  conduction mode. It badly under-predicts keyhole depths. The paper's Eq. 8 uses Q with A = 2.5 for
  AlSi10Mg and 2 otherwise.
- The paper's random-split R² values (0.96–0.996) and its published equations do not reproduce on
  the current public CSV. See `references/paper-notes.md` for the numbers this skill measures.
  Report those.

Cite: Akbari et al., MeltpoolNet, *Addit. Manuf.* 55 (2022) 102817.
