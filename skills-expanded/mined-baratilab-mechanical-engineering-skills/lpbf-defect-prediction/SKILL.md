---
name: lpbf-defect-prediction
description: Predict laser powder bed fusion (L-PBF) defect regimes — keyholing, lack of fusion, balling, or none — from process parameters (material, laser power, scan speed, beam diameter, hatch spacing, layer thickness), check measured melt-pool dimensions against the standard defect criteria, and draw power–velocity process maps with a recommended window. Based on AdditiveLLM (Barati Farimani Lab) and the MeltpoolNet dataset. Use for metal AM parameter selection, "will these settings keyhole?", process windows, or porosity troubleshooting.
---

# L-PBF defect prediction (AdditiveLLM)

Takes a metal L-PBF parameter set and says which defect regime it most likely falls in. Can
also draw the safe window across power and speed. The workflow follows *AdditiveLLM*
(Pak & Barati Farimani, Additive Manufacturing Letters 2025): MeltpoolNet melt-pool data,
labelled with three geometric criteria, augmented over hatch and layer, and learned as a
multi-label classifier. Paper details and how this skill differs are in
`references/paper-notes.md`.

Everything runs through `scripts/lpbf.py` (numpy, pandas, scikit-learn, matplotlib,
pyarrow). The first run downloads MeltpoolNet (~1 MB) from
github.com/BaratiLab/MeltpoolNet to `~/.cache/mechanical-engineering-skills/meltpoolnet`. Set
`LPBF_CACHE` to put it elsewhere.

## Pick the mode from what the user has

| User has | Use | Why |
|---|---|---|
| Measured or simulated melt-pool **depth, width (and length)** | `criteria` | Exact physics rules. No model, no uncertainty beyond the measurement. |
| Process parameters only | `predict` (after `build` + `train`, once) | Learned from about 2,400 experiments plus augmentation. |
| "What settings should I use?" | `map` | Power–velocity map, defect-free region, most robust point, and where the data actually is. |

## Criteria (paper Eqs. 1–3)

```bash
python scripts/lpbf.py criteria --depth 120 --width 150 --length 420 --hatch 100 --layer 40
```

| Regime | Fires when |
|---|---|
| Keyholing | W / D < 1.5 |
| Lack of Fusion | (h / W)² + (t / D)² > 1 |
| Balling | L / W > π |

The labels are not exclusive. **None** means every criterion that could be evaluated passed.
Missing inputs leave that criterion unevaluated, and the output says so. Never report "None"
when a criterion was skipped.

## Model (one-time, about 1 minute)

```bash
python scripts/lpbf.py build --out data.parquet      # ≈325k rows; prints label shares
python scripts/lpbf.py train --data data.parquet --model model.joblib   # grouped split by default
```

- `train` prints exact-match accuracy (all four labels correct) and F1 for each label.
- Default `--split grouped` holds out whole melt pools, typically about 88% exact match.
- `--split random` reproduces the paper's protocol and scores about 98%. It is inflated by
  leakage, so never quote it as expected accuracy (see notes).
- `--no-monotone` removes the physics constraints, for ablation only.

## Predict and map

```bash
python scripts/lpbf.py predict --model model.joblib --material Ti-6Al-4V \
    --power 280 --velocity 1200 --beam 80 --hatch 100 --layer 30
python scripts/lpbf.py map --model model.joblib --material Ti-6Al-4V \
    --hatch 100 --layer 30 --beam 80 --out map.png [--pmax 500 --vmax 2500]
```

- `predict` returns a probability for each regime, the predicted labels (None only if no
  defect head reaches 0.5), line and volumetric energy, and the model's validation scores.
- `map` shades the regions where each defect head is above 0.5. Green means all three are
  below 0.5. Measured points for that material are drawn as circles. The output also reports
  the defect-free fraction and the most robust point (the largest smoothed margin).
- Materials in the data include SS316L, SS17-4PH, IN625, IN718, IN738LC, Ti-6Al-4V,
  Hastelloy X, Cu10Sn, AlSi10Mg, Ti-48Al and others. Other alloys need
  `--props density,Cp,k,Tm`, and you should warn the user that the result is extrapolated.

## How to report

1. Give the regime and its probability, plus the energy numbers.
2. Name the physical lever:
   - keyhole: lower power or raise speed;
   - LoF: lower hatch or layer, or raise energy;
   - balling: lower speed at the same energy, or reduce the power–speed product.
3. Say whether the point lies inside the measured data (circles on the map) or is
   extrapolated. Green regions with no circles are guesses.
4. For a real build, recommend a small DOE of single tracks and density cubes around the
   suggested point. The model narrows the search; it does not replace qualification.

## Caveats to pass on

- Labels come from single-track melt-pool geometry. They do not cover spatter, cracking,
  residual stress, contour or downskin effects.
- W/D < 1.5 is a conservative keyhole rule. Many SS316L conduction-mode tracks trip it, so
  that material's map shows a narrow window.
- Balling has few examples because it needs melt-pool length, so the balling head rarely fires.
- To fine-tune an actual LLM as in the paper, `data.parquet` includes the Baseline `[SEP]`
  text. See `references/finetune.md`.

Cite: Pak & Barati Farimani, *Addit. Manuf. Lett.* 14 (2025) 100292; Akbari et al.,
*MeltpoolNet*, *Addit. Manuf.* 55 (2022) 102817.
