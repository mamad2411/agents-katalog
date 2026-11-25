---
name: am-alloy-screening
description: Screen metal alloys — known grades or new compositions — for laser powder bed fusion printability. Parse a composition, get thermophysical properties (Thermo-Calc/TC-Python CALPHAD when available, built-in alloy data or flagged estimates otherwise), compute Rosenthal melt pools and lack-of-fusion process maps over power and speed, and rank candidates by process window with explicit, unit-checked outputs. Based on the Barati Farimani Lab's agentic AM alloy evaluation. Use for "which alloy can I print for X", new-composition feasibility, LoF process maps, or checking material property files.
---

# AM alloy screening

Pak et al. (*Additive Manufacturing Letters* 17 (2026) 100355) let an LLM agent chain these steps
for any alloy, known or hypothetical:
1. Thermo-Calc thermophysical properties
2. a Rosenthal melt-pool model
3. a lack-of-fusion (LoF) process map

**You are that agent.** `scripts/alloy.py` provides the deterministic tools, and it needs only numpy
and matplotlib. Paper details, plus a unit bug found in the paper's own outputs, are in
`references/paper-notes.md`.

## Workflow
1. **Pin down the candidates.** If the user names an application (corrosion-resistant, high-temperature,
   lightweight), propose 2–5 candidate alloys and say why each fits.
   - `known` lists the built-in grades: SS316L, 17-4PH, H13, IN718, IN625, Hastelloy X, Monel K500,
     Ti-6Al-4V, AlSi10Mg, Al 7050, CuSn10, Cu, W, CoCrMo.
   - New compositions: `compose "Fe-10Ni-10Ti"` (balance element first, wt%), `compose Al90Cu5Ti5`,
     or add `--atomic` for at%.
2. **Get properties.**
   ```bash
   python scripts/alloy.py properties --alloy IN625 --out IN625.json
   python scripts/alloy.py properties --comp "Fe-10Ni-10Ti" [--thermocalc] --out FeNiTi.json
   ```
   - With Thermo-Calc and TC-Python (`references/thermocalc.md`), the database is chosen by the
     paper's rules. You get solidus and liquidus from the liquid fraction, density, Cp, k, and
     absorptivity via Drude from resistivity.
   - Without it, density and Cp come from the rule of mixtures; k, solidus, liquidus and absorptivity
     come from the nearest built-in alloy, with a confidence flag. **Pass a low-confidence warning on
     to the user.**
3. **Check units:** `check mat.json` (it also runs automatically). It catches density in g/m³ and Cp
   in J/mol·K, the slips found in the paper's repository outputs.
4. **Map and rank.**
   ```bash
   python scripts/alloy.py map  --material IN625.json --hatch 50 --layer 30 --out in625.png
   python scripts/alloy.py rank --materials IN625.json SS316L.json --hatch 50 --layer 30 --out compare.png
   ```
   - The defaults are the paper's: P and V from 100 to 1000 (W, mm/s) in steps of 100, at the layer
     and ±25 µm.
   - Widen the ranges (`--power 50:500:25 --velocity 200:2000:100`) when every alloy has an empty
     LoF region, otherwise the ranking only reflects tie-breakers.
   - `rank` sorts by the LoF fraction at the prescribed layer, then over all layers, then by the
     mean overlap criterion.
5. **Recommend from the keyed numbers**, not from impressions of the plot.
   - A *smaller* `lack_of_fusion_fraction` (a larger `process_window_fraction`) is better. The
     paper's one wrong recommendation came from misreading this.
   - Give the property source and confidence, and suggest single-track and density-cube trials
     before qualification.

## Limits (state them)
- Rosenthal is conduction mode only. The LoF boundary is conservative, and keyholing and balling are
  **not** predicted. For those, pair this skill with `lpbf-defect-prediction` and `meltpool-geometry`.
- Absorptivity matters a lot for Cu and Al at IR wavelengths. The Drude estimate is a baseline, and
  real absorptivity rises sharply once keyholing starts.
- New compositions need CALPHAD or measurement. The fallback says so, and you should too.

Cite: Pak, Chandrasekhar & Barati Farimani, *Addit. Manuf. Lett.* 17 (2026) 100355.
