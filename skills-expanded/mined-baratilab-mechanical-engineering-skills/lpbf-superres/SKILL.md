---
name: lpbf-superres
description: Turn low-cost webcam images of an L-PBF build plate into high-resolution layer images — register webcam and scientific-camera views with part-centre homographies and deformation maps, build patch datasets with leakage-safe splits, train a conditional diffusion model (or CNN baseline), and score with PSNR, SSIM, MAE, wavelet texture distance, part IoU and edge roughness (Ra, Rq). Based on the Barati Farimani Lab / Sandia diffusion super-resolution paper. Use for layer-wise optical monitoring, camera upgrades on a budget, or recovering surface roughness from layer images.
---

# LPBF layer-image super-resolution

Ogoke et al. (*Additive Manufacturing* 107 (2025) 104790) trained a conditional **diffusion** model to
map a 1080p webcam's view of the powder bed to what a scientific camera sees. The model recovers
scan tracks, powder texture and part-edge roughness, so cheap cameras can support high-resolution
layer-wise monitoring.

`scripts/sr.py` covers the full pipeline. It needs numpy, scipy, OpenCV, scikit-image and
PyWavelets; the models also need PyTorch, ideally with a GPU. Paper numbers and the deliberate
differences from it are in `references/paper-notes.md`.

## Workflow
1. **Collect pairs.** For each layer, one HR and one LR image of the whole plate (grayscale PNGs,
   same file order in `hr/` and `lr/`). The build needs at least 4 separated parts so registration
   has anchors.

   No data yet? `python scripts/sr.py synth --out plate/` makes a ring-part build plate with a known
   camera warp.
2. **Register:** `python scripts/sr.py register --hr plate/hr --lr plate/lr --out aligned/`.
   - Parts are segmented in both views and their centres matched (Hungarian).
   - A RANSAC homography is fitted, then the remaining centre offsets are interpolated
     (thin-plate RBF) into a deformation map.
   - Output: HR warped onto the webcam view, and LR bicubic-upsampled to the HR pixel size ("same
     pixels, different detail").
   - **Check `median_centre_error_px`. It should be well under 1 px.** Bad registration silently
     ruins everything downstream.
3. **Patches:**
   `python scripts/sr.py patches --aligned aligned/ --out pairs.npz [--split layer|part]`.
   - The default matches the paper: 64 × 64 patches, 115 per layer, test layers held out.
   - `--split part` holds out whole parts, which is the stricter test.
4. **Train:**
   - `python scripts/sr.py train --pairs pairs.npz --model diffusion --out diff.pt --epochs 300` (GPU)
   - `--model cnn` trains a deterministic baseline.
   - On CPU, pass `--max-minutes` for a time-boxed run.
5. **Predict and score:**
   ```bash
   python scripts/sr.py predict --model diff.pt --pairs pairs.npz --out pred.npz --steps 50
   python scripts/sr.py metrics --pred pred.npz          # HR|LR vs HR|SR: PSNR, SSIM, MAE, wavelet texture distance
   python scripts/sr.py plate --aligned aligned/ --px-um 10 --model diff.pt --layers 0,5,10   # part IoU, Ra, Rq per source
   ```

## How to read the results
- A **deterministic CNN** usually wins on PSNR and MAE but loses on texture. It predicts the mean
  of all plausible HR images, so scan tracks and powder blur out and edges look too smooth (low Ra).
- A **diffusion model** samples one plausible HR image. Its PSNR may be lower, but its texture
  distance and roughness should land closer to HR. That is the paper's argument. Report both kinds
  of metric, never PSNR alone.
- Hallucinated detail is still hallucinated. Super-resolved images are good for monitoring and
  roughness *statistics*; they are not evidence of a specific defect at a specific pixel. Confirm
  anything that will drive a decision on the HR camera or on CT.

Cite: Ogoke et al., *Addit. Manuf.* 107 (2025) 104790.
