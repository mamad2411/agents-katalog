---
name: circuit-checker
description: Validates TikZ/circuitikz schematic layouts for orthogonal wires, spacing, collisions, and clearance.
---

# Circuit Checker Skill

This skill allows Antigravity to validate TikZ and `circuitikz` circuit diagrams in LaTeX files (`.tex`) for geometric compliance, ensuring:
- **No diagonal wires:** All wire segments must be purely horizontal or vertical.
- **Wire-Wire / Wire-Component collisions:** Detects paths intersecting other traces or component bodies.
- **Op-amp clearances:** Ensures components are placed at a safe distance from op-amps (minimum 1.8 units) and lead wires are long enough.
- **Trace spacing:** Maintains a minimum distance (1.5 units) between parallel traces to prevent overlapping.
- **Label clearances:** Checks that text nodes do not overlap components, grounds, or wires.

## How to use

Run the verification script from the terminal:

```bash
python3 ~/.gemini/config/skills/circuit_checker/scripts/find_layout_collisions.py [path_to_latex_file.tex]
```

If no path is specified, the script will automatically check the first `.tex` file in the current working directory.
