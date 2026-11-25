---
name: mechanics-visuals
description: Produces clean, correct mechanics teaching figures — Mohr's circle, shear/moment/deflection diagrams, S–N curves, stress–strain curves, and free-body diagrams — as PNG/SVG for slides, notes, or exams. Use when the user asks to draw, plot, or visualize a mechanics concept, an FBD, a beam diagram, or a stress state.
---

# Mechanics Visuals

The numbers behind every figure come from `scripts/mech_plots.py`, so the picture and the values always agree.

## Workflow
1. **Pin down the scenario**: geometry, loads, supports, sign convention, and units. If the user is teaching, ask once which textbook's convention they follow (the default is Shigley/Hibbeler).
2. **Generate the figure:**
   ```bash
   python scripts/mech_plots.py mohr --sx 80 --sy -40 --txy 30 --out mohr
   python scripts/mech_plots.py beam --L 2000 --support simply --point 800:5000 --udl 0:2000:2 --I 8.3e6 --out beam
   python scripts/mech_plots.py sn   --Sut 690 --Se 280 --out sn
   python scripts/mech_plots.py ss   --sy 350 --Sut 480 --n 0.18 --out ss
   ```
3. **Free-body diagrams**: no script. Write a matplotlib or SVG drawing following `references/fbd_style.md` (body as a light-grey shape, every force as a labelled arrow from its point of application, reactions in a different color, coordinate triad in a corner). Check equilibrium numerically (ΣF = 0, ΣM = 0) and print the residuals before you show the figure.
4. **Verify**: compare one value against a closed form, e.g. simply supported center load M_max = PL/4, δ = PL³/48EI. State the comparison.
5. **Deliver**: the PNG for viewing, the SVG for slides, and a 2–3 sentence caption with the key numbers.

## Style
Use one accent color for loads, one for reactions and grey for geometry. Use SI units, label every axis, and keep titles under about 8 words. Never put more than one concept in a single figure unless the user asks for it.
