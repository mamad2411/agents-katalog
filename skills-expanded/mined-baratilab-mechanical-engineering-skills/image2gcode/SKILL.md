---
name: image2gcode
description: Turns a photo, hand sketch, or slice image of a 2D/2.5D part directly into printer-ready FDM G-code without CAD, following the Image2Gcode pipeline — boundary extraction to a 224×224 silhouette, per-layer (X,Y,E) toolpath keypoints, denormalization to printer G-code with header/footer, and validation (build limits, extrusion monotonicity, travel distance). Use when the user wants to print something from a picture or drawing, convert an image or outline to G-code, analyze or normalize G-code toolpaths, or work with the Image2Gcode diffusion model's input/output format.
---

# Image2Gcode: image → G-code (2D / 2.5D)

Paper: Z. Wang, Y. Jadhav, P. Pak, A. Barati Farimani, *Image2Gcode: Image-to-G-code generation for additive manufacturing using diffusion-transformer model*, Additive Manufacturing Letters 17 (2026) 100374.

**What's bundled.** The paper's preprocessing, keypoint representation, post-processing and validation are reproduced exactly. The trained DDPM (DinoV2 + 1-D U-Net) is available from the authors on request. In its place, `generate` is a deterministic perimeter-plus-infill generator that emits the same keypoint and G-code format, so model samples drop in later (`references/ddpm_hook.md`). Tell the user which generator produced their toolpath.

Scope matches the paper: parts described by one cross-section, or a few layer-wise consistent ones (plates, brackets, gaskets, coasters, 2.5D extrusions). For full 3-D parts, use CAD (`parametric-part-cad`) and a slicer.

Setup: `pip install opencv-python-headless shapely numpy matplotlib`. I = `scripts/i2g.py`.

## Workflow
1. **Preprocess the image.**
   ```bash
   python $I preprocess sketch.jpg --out sil.png --mode sketch   # pen outline on paper
   python $I preprocess photo.jpg  --out sil.png --mode photo    # object photo on a plain background
   python $I preprocess slice.png  --out sil.png --mode slice    # already a filled cross-section
   ```
   **Look at `sil.png`.** White should be material and holes black. If the outline isn't closed or the background leaks in, fix the input (crop, raise contrast, close gaps) rather than tuning the toolpath.
2. **Get physical size and print settings from the user**: overall size (the image has no scale), thickness (layers × layer height), nozzle and line width, infill pattern and density, temperatures, bed size. If unstated, use defaults (0.2 mm layers, 0.45 mm lines, 2 perimeters, 25% rectilinear, PLA 210/60 °C) and list them.
3. **Generate.**
   ```bash
   python $I generate sil.png --size-mm 60 --layers 15 --infill rectilinear --density 0.25 --out part.gcode
   ```
4. **Validate and inspect.**
   ```bash
   python $I validate part.gcode --bed 220 220 250
   python $I plot part.gcode --out paths.png --layers 0,1
   ```
   `ok` must be true. Check the plot: closed perimeters around every hole, infill inside the walls only, alternating raster direction between layers. Compare the reported area or bbox with the intended size.
5. **Deliver** the G-code, the path plot, and a settings table, with first-print advice (preview it in the user's slicer or viewer first; the header homes and heats with standard Marlin codes).

## Working with existing G-code
- `python $I keypoints any.gcode --out kp.npz` builds Slice-100K-style per-layer (X, Y, E) keypoints with the paper's normalization. It handles G90/G91, M82/M83, mid-file G92 E resets, and constant-E travels. Use it for datasets, comparisons, and travel-distance studies (the paper reports a −2.40% mean travel distance against heuristic slicers).
- `python $I emit kp.npz --layer 0 --size-mm 40 --out layer.gcode` denormalizes keypoints (including model samples) into G-code at any physical scale, with `--flow-mult` for printer-specific extrusion.

## Limits
Hand-drawn wobble carries into the part, since the boundary is the drawing. Very thin features (under 2 line widths) vanish in the perimeter offset. There's no bridging or support logic, so the parts are prismatic by construction.
