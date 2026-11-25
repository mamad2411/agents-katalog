---
name: linkage-synthesis
description: Synthesizes planar one-degree-of-freedom linkages (four-bar, six-bar, multi-bar) whose end-effector traces a target curve, following LinkD — the N×24 graph representation, dyadic topology validation, 200-angle forward kinematics with branch-defect detection, node-by-node construction with bounded retries, and Chamfer-distance evaluation, plus practicality limits on link ratios and pivots. Use when the user wants a mechanism that traces a path, coupler-curve or path-generation synthesis, a four-bar/six-bar design, or to validate/simulate/animate an existing linkage.
---

# Linkage synthesis (LinkD method)

Paper: Y. Jadhav, A. Barati Farimani, *LinkD: AutoRegressive Diffusion Model for Mechanical Linkage Synthesis*, arXiv:2601.04054. LinkD builds a mechanism one joint at a time with a causal transformer plus a DDPM, checks every new node kinematically, and resamples a failing node up to K times. Node-level retry raised its valid-generation rate from 29.4% (one-shot) to 99.6%.

**What's bundled.** The paper's representation, validation, kinematics and metric are reproduced exactly (`linkage.py`). The trained model isn't public, so `synth.py` replaces the diffusion sampler with optimization-driven proposals under the same discipline: build node by node, validate the full revolution, use bounded retries, and keep only improvements. Tell the user which generator was used.

Setup: `pip install numpy scipy matplotlib`. `S=scripts`.

## Mechanism format
```json
{"nodes": [[x, y], ...], "fixed": [0, 2], "edges": [[0,1],[1,3],[2,3],[1,4],[3,4]],
 "motor": [0, 1], "effector": 4}
```
The motor link is the crank: node `motor[1]` rotates a full turn about fixed node `motor[0]`. Every other moving joint must connect to **exactly two** already-known joints (dyadic assembly), so the mechanism has one degree of freedom.

## Workflow
1. **Get the target path.** Use CSV points (`x,y` header) from the user, digitize a sketch, or use a preset (`ellipse`, `crescent`, `bean`). Ask whether a rotated or mirrored path is acceptable. LinkD notes that a mechanism can be installed rotated or mirrored; if so, use `--invariant`.
2. **Synthesize.**
   ```bash
   python $S/synth.py target.csv --out mech.json --max-nodes 8 [--invariant] [--seed 0]
   ```
   Stage 1 fits a four-bar with up to 25 retries. Stage 2 grows six-bar steps (a ground-anchored dyad plus a coupler point), each validated, keeping a step only if it improves the fit by more than 2%. Runtime is about 15 s for a four-bar and a few minutes for growth. Try 2–3 seeds; the problem has many solutions.
3. **Validate and inspect.**
   ```bash
   python $S/linkage.py validate mech.json      # topology + 200-angle kinematics, link-length drift, joint clearance
   python $S/linkage.py plot mech.json --target mech_target.csv --out mech.png
   ```
   `valid` must be true. Also check the `practicality` block from `synth.py`: link ratio ≤ 8, ground pivots separated, no link shorter than 10% of the path, footprint ≤ 6× the path. Look at the plot. Short rocker links cause kinks and cusps in the path.
4. **Report** the mechanism table (joint coordinates, fixed or moving, link lengths), the Chamfer distance and its protocol, the path overlay, and the practicality metrics. Scale the normalized design to the user's size (multiply all coordinates by the path size).
5. **Hand off.** For hardware, model the links with `parametric-part-cad` or `cadsmith-text-to-cad` (pin diameters and link thickness), then check stresses with `machine-element-sizing`.

## Metric (two protocols)
- Default: both curves are resampled by arc length (400 points) and normalized (centred, unit RMS radius), then the Chamfer distance (LinkD Eq. 7: mean nearest-neighbour L2 in both directions) is computed. Crank-angle sampling bunches points where the end-effector moves slowly. Under mixed sampling, an *exact* mechanism scores 0.107 against its own path; under arc-length resampling it scores 0.008.
- `compare --raw`: LinkD's protocol (200 uniform motor angles on both curves). Use it only when both curves come from mechanisms.

## Other tools
- `linkage.py encode/decode` converts to and from LinkD's N × 24 matrix: validity, type (1 fixed / 0 revolute / −1 pad), normalized x and y, and 20 lower-triangular adjacency entries. Use it to prepare data for, or read samples from, a trained LinkD model.
- `linkage.py simulate` writes the end-effector path; `compare` scores any two paths.

## Limits
Planar, revolute-only, single crank input, rigid links, no dynamics. Branch defects (the mechanism can't reach part of the revolution) and over-constrained or non-dyadic graphs are rejected, as in the paper. Transmission angle isn't optimized; check it for the final design if forces matter.
