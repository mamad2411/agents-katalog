---
name: machine-element-sizing
description: Sizes and checks machine elements — bolted joints, shafts (fatigue), rolling bearings (L10 life), helical springs, fillet welds, and spur gears — with shown work and safety factors. Use when the user asks to size, select, or verify a bolt, shaft, bearing, spring, weld, or gear.
---

# Machine Element Sizing

All numbers come from `scripts/me_sizing.py`. Do not do sizing arithmetic in your head.

## Workflow

1. **Identify the element and load case.** Static vs fatigue; steady vs alternating components; operating speed.
2. **Collect inputs in SI (N, mm, MPa, N·mm, rpm).** Convert user units first and state the conversion. If a required input is missing:
   - material strengths → look up in `references/materials.md` and state the source row;
   - stress concentration Kf/Kfs → use the first-iteration defaults in `references/defaults.md`, flag them as assumptions;
   - anything else → ask.
3. **Run the calculator** (`python scripts/me_sizing.py <cmd> --help` for options):
   ```bash
   python scripts/me_sizing.py bolt    --size M10 --grade 8.8 --load 24000 --n-bolts 4 --fatigue
   python scripts/me_sizing.py shaft   --Ma 70000 --Tm 120000 --Kf 1.7 --Kfs 1.5 --Sut 690 --Sy 580
   python scripts/me_sizing.py bearing --type ball --Fr 2500 --rpm 1800 --hours 20000 --reliability 0.95
   python scripts/me_sizing.py spring  --d 2.5 --D 20 --Na 8 --F 120 --material music-wire
   python scripts/me_sizing.py weld    --F 30000 --h 6 --L 200 --electrode E70
   python scripts/me_sizing.py gear    --module 3 --N 20 --F 35 --T 150000 --rpm 1200 --Sy 400
   ```
4. **Iterate** until every check is `PASS`: change size/grade/material, re-run. For shafts, round up to a standard diameter and re-run with updated Kf.
5. **Sanity check** one result by a one-line hand estimate (e.g. τ ≈ 16T/πd³) and confirm it agrees within ~20%.
6. **Report** in the format below.

## Output format

```
## <Element> sizing — <one-line case>
Assumptions: ... (flag every defaulted value)
| Quantity | Value | Unit |       ← key intermediate values from the JSON
Checks:  ✅ n_L = 2.1 ≥ 1.5   ❌ n_f = 1.1 < 1.5
Recommendation: M12 grade 10.9, preload 75% proof, torque ≈ 0.2·Fi·d
Method: <method string from JSON>
```

## Guardrails
- Gear results are Lewis screening only; say that AGMA 2001 / ISO 6336 is required for final design.
- Weld bending requires the weld-group unit properties; see `references/weld_groups.md`.
- Never report a safety factor without stating the failure criterion it refers to.
