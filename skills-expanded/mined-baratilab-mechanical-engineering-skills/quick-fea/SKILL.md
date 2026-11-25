---
name: quick-fea
description: Runs quick linear-static and modal finite-element analysis on a STEP part (gmsh mesh + scikit-fem quadratic tets), reports max stress, deflection, natural frequencies, and always checks against a hand calculation and a mesh-convergence run. Use when the user asks for FEA, stress analysis, deflection, stiffness, natural frequency, or whether a part will survive a load.
---

# Quick FEA

Setup: `pip install gmsh scikit-fem matplotlib`. On headless Linux, gmsh also needs `apt-get install libglu1-mesa libxcursor1 libxinerama1 libxft2`. Units: mm, N, MPa, t/mm³.

## Workflow
1. **Geometry.** Use the user's STEP, or build one with the `parametric-part-cad` skill. Remove cosmetic features (logos, small chamfers) that don't carry load. Note the bounding box; you'll use it to pick boundary faces.
2. **Write down the idealization** before you solve: the material (E, ν, ρ, σy), which faces are fixed, which faces carry the load, the load magnitude and direction, and what is being neglected (contact, preload, plasticity, large deflection).
3. **Hand calculation first.** Estimate the answer with a closed form: beam bending σ = Mc/I, δ = FL³/3EI, Lamé thick cylinder, plate formulas (`references/hand_calcs.md`). This is the sanity anchor.
4. **Solve:**
   ```bash
   python scripts/fea.py part.step --E 69000 --nu 0.33 --fix "x[0] < 1e-3" \
       --load "x[0] > 149.999" --force 0,0,-500 --size 4 --out run1
   python scripts/fea.py part.step --E 69000 --nu 0.33 --rho 2.7e-9 --fix "x[0] < 1e-3" --modes 6 --out modal
   ```
   Face selection uses expressions on facet midpoints, for example `np.abs(x[2]-10)<1e-3`, or `(x[0]**2+x[1]**2) < 6.1**2` for a bolt hole.
5. **Convergence.** Re-run with `--size` halved. A result is converged when max displacement changes by less than 2% and the 99th-percentile von Mises stress by less than 5%. Max von Mises at a sharp re-entrant corner is a singularity: it never converges. Report the stress at a small distance from the corner, or add the real fillet.
6. **Check:**
   - `equilibrium_error_pct` < 1%;
   - FEA agrees with the hand calculation within about 15% for the nominal region, or you can explain why it differs;
   - margin = σy / σ_vm(p99) − 1, reported against the user's target safety factor;
   - deflection small compared with thickness. If not, linear theory doesn't apply; say so.
7. **Report**: idealization sketch (text), mesh table, results with the convergence column, hand-calc comparison, contour image `run1_vm.png`, margin, and recommendations.

## Limits
Linear elastic, small deflection, no contact, isotropic material. For bolted joints, model the bolt-hole bearing area as the fixed or load face, not the whole hole. For thin shells, use a fine mesh (at least 2 elements through thickness) or flag the stiffness error.
