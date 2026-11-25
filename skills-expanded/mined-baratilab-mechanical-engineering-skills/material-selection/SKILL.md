---
name: material-selection
description: Selects engineering materials with the Ashby method — translate function, constraints, objectives into a performance index, screen, rank, and justify a shortlist with charts. Use when the user asks which material to use, compares materials, wants a lighter/cheaper/stiffer alternative, or mentions Ashby charts or performance indices.
---

# Material Selection (Ashby method)

## Workflow
1. **Translate the design** into four items and write them down:
   - Function (tie, beam, panel, spring, hinge, heat spreader…)
   - Constraints, both hard (service temp, min strength, corrosion, food-safe) and geometric (fixed length, fixed width)
   - Objective (minimize mass, cost, or volume)
   - Free variable (usually section size or thickness)
2. **Pick the performance index.** Use the table in `references/indices.md`. If the case isn't listed, derive it: write the objective, eliminate the free variable using the constraint equation, and group the material properties. Show this derivation in 3–4 lines.
3. **Run the screen and rank:**
   ```bash
   python scripts/rank_materials.py --index stiff-beam --Tmin 80 --exclude ceramic --top 8 --out sel
   python scripts/rank_materials.py --index stiff-beam --minimize-cost --top 8 --out sel_cost
   ```
   Run both the mass and the cost version unless the user cares about only one.
4. **Apply judgment the index can't capture**: manufacturability at the expected volume, joining, corrosion, availability, fatigue behaviour, anisotropy (CFRP UD), and brittleness (ceramics, cast iron). Cut the list to 3 candidates.
5. **Report**: function/constraints/objective table → index derivation → ranked table (relative index, cost/kg) → chart `sel_chart.png` → recommendation with runner-up and the trade-off between them.

## Notes
- The database (`references/materials.csv`) holds typical mid-range values for screening. Before final design, use supplier datasheets or MMPDS values.
- Users can add rows to the CSV. Keep its units: GPa, kg/m³, MPa, $/kg.
