---
name: thermal-porosity
description: Predict layer-wise porosity in laser powder bed fusion from in-situ thermal (pyrometry) image sequences — empty-frame filtering, CT pore alignment and ESD thresholds, pore-count regression and 16x16 porosity localization with interpretable thermal-history baselines and the paper's CNN / video-transformer models, scored by RMSE, R² and IoU. Based on ThermoPore (Barati Farimani Lab with Sandia). Use for in-situ monitoring data, porosity digital twins, CT-to-thermal correlation, or part-qualification studies.
---

# Thermal-image porosity (ThermoPore)

ThermoPore (Pak et al., *Additive Manufacturing* 95 (2024) 104503) links every L-PBF build layer's
in-situ pyrometry sequence (200 frames, 64 × 64 px at about 21 µm/px) to the pores micro-CT later
finds in that layer. It has two tasks:
- **count** the pores;
- **localize** them on a 16 × 16 grid.

`scripts/thermopore.py` covers the whole pipeline. It needs numpy, pandas and scikit-learn; the deep
models also need PyTorch. Paper details and reference numbers are in `references/paper-notes.md`.

## Workflow
1. **Rehearse** (no data needed): `python scripts/thermopore.py synth --out run/`.
   - This builds a synthetic 10-step × 16-layer build with pores tied to cold and hot cells.
   - Use it to check the pipeline and learn the formats. It is **not** evidence of real-world
     accuracy, and every result from it carries `"synthetic_data": true`. Say so.
2. **Prepare real data:**
   ```bash
   python scripts/thermopore.py prepare --frames layers/ --pores ct_pores.csv --out run/ \
       --z-offset 5 --xy-offset 120,40 [--min-peak 900] [--voxel-um 3.63]
   ```
   - `layers/` holds one `.npy` or `.tif` stack per build layer, sorted by name.
   - Empty frames are dropped by a threshold on each frame's peak temperature (automatic unless you
     pass `--min-peak`), then each layer is resampled to 200 frames.
   - `ct_pores.csv` has `pore_id, layer, x_um, y_um, esd_um`, or `voxels` plus `--voxel-um`. Its
     coordinates are already in the thermal camera's frame, except for the offsets you pass.
   - **Alignment matters most.** Check it with `map` (step 4) on a layer where the whole scan is in
     view, before training anything.
3. **Baseline first (CPU, seconds):**
   ```bash
   python scripts/thermopore.py baseline --data run/ --task count [--depth 1|2|3] [--esd-min musigma]
   python scripts/thermopore.py baseline --data run/ --task localize
   ```
   - The features are thermal-history maps: peak T, min-of-peak, mean T, dwell above a melt threshold
     and peak-T roughness, pooled to 16 × 16.
   - The baseline gives a number to beat and features you can explain: cold cells point to lack of
     fusion, hot cells to keyholing.
4. **Look at a layer:**
   `python scripts/thermopore.py map --data run/ --layer 40 --out l40.png` shows one frame, the peak
   map, the dwell map and the CT pore map.
5. **Deep models (GPU recommended):**
   ```bash
   python scripts/thermopore.py train --data run/ --task count --epochs 500 [--rotate] --out cnn.pt
   python scripts/thermopore.py train --data run/ --task localize --epochs 1000 [--rotate] --out vivit.pt
   ```
   - These are the paper's architectures. `--small` shrinks the ViViT and raises learning rates for
     CPU smoke tests.
   - `--rotate` applies one rotation to the whole sequence and its label map, and never changes
     intensities.

## Reporting
- Use the paper's split: 75/25 *within* each process step. Report the count task as RMSE and R²
  with predictions rounded to integers; report localization as mean and max IoU at the threshold
  chosen on the training layers.
- State the ESD threshold.
  - With a 100-voxel minimum, gas pores dominate and are hard to predict.
  - A μ+σ cut (about 50 µm) keeps keyhole and lack-of-fusion pores, but leaves few positive cells,
    so IoU becomes noisy.
- Compare with the paper (R² 0.57 best, RMSE 7.84, IoU 0.32 mean), and with your own baseline.
- If the deep model doesn't beat the baseline, report that. The paper notes its dataset was small,
  and so is most real CT data.
- These models flag regions for CT and inspection; they don't replace qualification.

Cite: Pak et al., ThermoPore, *Addit. Manuf.* 95 (2024) 104503.
