---
name: thermal-fluids-calc
description: Thermal-fluids design calculations — pipe and duct pressure drop and pump head, heat exchanger rating and sizing (LMTD / ε-NTU), fin design, and fluid properties via CoolProp. Use when the user asks about pressure drop, pump sizing, heat exchanger duty or area, cooling fins, or properties of water, air, refrigerants, or oils.
---

# Thermal-Fluids Calculator

Run `scripts/thermo_fluids.py` (needs `pip install CoolProp`). Inputs are in SI. Convert first and state the conversion.

## Workflow
1. **Classify**: internal flow, heat exchanger, extended surface, or properties only.
2. **Get properties at the right temperature**: use the mean bulk temperature for heat exchangers. Always use `props`; never use remembered property values.
   ```bash
   python scripts/thermo_fluids.py props --fluid Water --T 40
   ```
   CoolProp names: `Water`, `Air`, `R134a`, `R1234yf`, `Nitrogen`, `CO2`, `INCOMP::MEG-30%` (glycol mix).
3. **Calculate**
   ```bash
   # Pressure drop in 50 m of 2" sch40 steel pipe, 4 L/s water, 3 elbows + valve
   python scripts/thermo_fluids.py pipe --D 0.0525 --L 50 --Q 0.004 --K 3.2 --T 20
   # Rate an exchanger with known UA
   python scripts/thermo_fluids.py hx --mh 0.5 --cph 4180 --mc 0.8 --cpc 4180 --Thi 80 --Tci 15 --UA 2500
   # Size for a duty, report area for U = 800 W/m2K
   python scripts/thermo_fluids.py hx --mh 0.5 --cph 4180 --mc 0.8 --cpc 4180 --Thi 80 --Tci 15 --q 60000 --U 800
   # Aluminum fin
   python scripts/thermo_fluids.py fin --k 200 --h 40 --L 0.03 --t 0.002 --w 0.05 --Tb 85 --Tinf 25
   ```
   Typical minor-loss K values and U ranges are in `references/coefficients.md`.
4. **Check**: energy balance closes (q = Ch·ΔTh = Cc·ΔTc), no temperature cross, Re regime stated, velocities reasonable.
5. **Report**: assumptions → results table → checks → recommendation (pipe size, exchanger area with a 10–25% fouling margin, fin count).
