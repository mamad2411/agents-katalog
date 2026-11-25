---
name: stress-field-surrogate
description: Predict full 2D von Mises stress fields from geometry, supports and loads in milliseconds for design iteration — StressD-style conditional diffusion (normalised field + scale network) or a direct regression baseline, a built-in plane-stress Q4 FEM generator for training data (checked against beam theory), and validation on unseen geometries with MAE, MSE and peak-stress error. Based on StressD (Barati Farimani Lab). Use when FEA is too slow inside a design loop, for generative/topology design screening, or to build an FEA surrogate for a part family.
---

# Stress-field surrogate (StressD)

StressD (Jadhav et al., *CMAME* 416 (2023) 116343) generates von Mises stress maps from a 5-channel
input: geometry, support x/y and load x/y. It has two parts:
- a **conditional diffusion** model that produces the field normalised per sample;
- an **auxiliary network** that predicts the scale.

On Nie et al.'s cantilever dataset it cut MAE by about 78% compared with StressNet and StressGAN.
`scripts/stressd.py` reproduces the pipeline and adds a FEM data generator, so you can train on your
own part family. It needs numpy and scipy; the models need PyTorch. Paper numbers and the split
caveat are in `references/paper-notes.md`.

## Workflow
1. **Data.** `python scripts/stressd.py dataset --out cant.npz [--geoms 80 --angles 72 --mags 20]`
   - Generates cantilever geometries in 6 families (plain, holes, notches, tapered, slots, truss
     openings) on a 32 × 24 grid, clamped on the left and loaded at a tip pad over 0–355° and
     5–100 N.
   - The plane-stress Q4 FEM uses E = 200 GPa, ν = 0.3, t = 1 mm, 1 mm elements. It is linear, so
     each geometry costs 2 solves however many load cases you want.
   - The FEM matches Euler–Bernoulli bending stress within 1% on slender strips (tested).
   - For your own parts, replace `random_geometry` with your parametric family, or rasterise CAD
     sections.
2. **Train.**
   - `train --data cant.npz --model diffusion --out sd.pt` is StressD: cosine schedule, T = 500,
     L1 noise loss, and a ViT scale network on 4 × 4 patches.
   - `--model regression` is a direct U-Net baseline (StressNet-like).
   - **Use `--split geometry` (the default).** The paper's 80/20 random split shares geometries
     between train and test. Since stress is linear in load, a geometry seen under other loads is
     nearly free to predict. Only unseen geometries test a design surrogate.
3. **Predict and score.**
   ```bash
   python scripts/stressd.py predict --model sd.pt --data cant.npz --out pred.npz --steps 50
   python scripts/stressd.py metrics --pred pred.npz      # MAE, MSE, peak-stress abs. error, MAPE (paper's metrics)
   python scripts/stressd.py plot --pred pred.npz --out cases.png
   ```
4. **Use in design.** Screen many candidate shapes with the surrogate, then **confirm the winner
   with real FEA** (`quick-fea`).
   - Peak stresses near notches and holes are where surrogates err most. Report the peak error
     alongside the mean.
   - Don't use surrogate output for a safety factor.

## Notes
- The diffusion sampler is stochastic. Average a few samples, or report spread, for critical
  regions; the paper averages 3 runs.
- `fem` runs a single solve for any 32 × 24 mask image, which is handy for spot checks.

Cite: Jadhav et al., *StressD*, Comput. Methods Appl. Mech. Engrg. 416 (2023) 116343.
