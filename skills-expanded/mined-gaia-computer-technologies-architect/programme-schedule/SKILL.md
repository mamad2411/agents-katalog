---
name: programme-schedule
description: Build or sanity-check a schedule of accommodation — room list, per-space areas from named benchmarks, circulation and net-to-gross with an explicit efficiency factor, reconciled to a target GIA or budget. Use when an architect needs an "area schedule", "schedule of accommodation", "space programme", net/gross gross-up, or "does this fit". Shows every calculation step (free-typed arithmetic is unreliable), states benchmarks as convention to verify (never code), and flags gaps. Extends design-brief.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Programme Schedule

Turn a programme into a schedule of accommodation that adds up — room list, areas, circulation, and the net-to-gross gross-up — and check it against the target. This is the quantitative spine of the brief, and it is exactly where an unaided model goes wrong, so the discipline below is the point of the skill.

## Read this first: numbers must be shown, not typed

Language models are unreliable at consistent arithmetic — they confuse net and gross, mislay a factor, and confidently emit a total that doesn't equal its parts. So:

1. **Show every calculation.** Never write a total you didn't derive in front of the reader. Each area line shows quantity × unit area = subtotal; the gross line shows net ÷ efficiency = gross.
2. **Keep net and gross rigidly separate.** State which you mean, every time. Net internal area (usable rooms) and gross internal area (everything inside the external walls, including structure and circulation) are different numbers — never blur them. (This is the area-schedule version of confusing kW and kWh; it corrupts everything downstream.)
3. **State the efficiency factor explicitly** and apply it visibly: `GIA = net ÷ efficiency`. Don't bury the gross-up.
4. **Re-add at the end and check** the sum equals the reconciliation target. If it doesn't, say so and show the gap — don't quietly adjust a line to make it fit.
5. **Benchmarks are convention, not code.** Every unit-area figure is a starting point to confirm, tagged as such — never presented as a requirement.

If the arithmetic is non-trivial, compute it stepwise and consider emitting a formula-bearing table (so the architect can drop it into a spreadsheet and the cells recompute) rather than hand-typed totals.

## When to use

- After `design-brief`, to turn the programme into checked areas.
- To test "does this fit?" — will the schedule sit inside the site's buildable area or the budget.
- To gross-up a net area to GIA, or reverse-engineer a net target from a GIA cap.

## Input

- The room/space list (or the building type, to generate a first-pass list).
- Any known areas or standards the architect wants used (these override benchmarks).
- The reconciliation target: a target GIA, a site's buildable area, a budget, or a unit count.
- Building type and quality tier (affects the efficiency factor and unit areas).

## Process

1. **Assemble the room list** from the brief or the type. Flag spaces briefs routinely forget: storage, plant, risers, circulation, WCs, refuse, cleaner's stores.
2. **Assign a net area to each** from a named benchmark or the architect's own standard. Tag each figure `[benchmark — confirm]`.
3. **Sum the net internal area,** showing the subtotals.
4. **Apply circulation and gross-up.** Either list circulation as its own line, or apply a net-to-gross efficiency factor — but state which, and show the maths.
5. **Reconcile to the target.** Net or gross as appropriate. Show the difference. If over, show what would have to give; if under, show the headroom.
6. **Report gaps and assumptions** plainly.

## Domain knowledge

### Net-to-gross efficiency — typical ranges (convention, confirm per project)

The efficiency factor is `net usable ÷ gross internal`. Typical ranges by type — **starting points to verify, not standards:**
- Offices: ~75–85% (tall towers with big cores can fall to ~65–70%).
- Residential: often ~80–85% (higher for houses, lower for flats with more common circulation).
- Labs / healthcare: ~50–65% (heavy servicing and circulation).
- Schools: ~65–75%.

Lower efficiency = more gross area (and cost) for the same usable space. Always state the figure you used and why.

### Gross-up worked example (show your work like this)

```
Net internal area (sum of rooms):        420 m²
Assumed efficiency (mid-rise flats):     80%   [confirm]
Gross internal area = 420 ÷ 0.80 =       525 m²
Target GIA (site cap):                   500 m²
Difference:                              +25 m² OVER — see options below
```

### Where free-typed numbers go wrong (watch for these)

- A total that doesn't equal the sum of its lines — always re-add.
- Multiplying, then applying the efficiency the wrong way (× instead of ÷).
- Mixing net and gross between the room table and the reconciliation.
- Dropping the spaces nobody lists (plant, risers, circulation) and then "discovering" the building is bigger than the schedule.

## Output format

```
## Schedule of Accommodation — [project]

| Space | Qty | Unit area (m²) | Subtotal (m²) | Basis |
|---|---:|---:|---:|---|
| [room] | 2 | 14 | 28 | [benchmark — confirm] |
| ... | | | | |
| **Net internal area** | | | **[sum]** | re-added |

Efficiency assumed: [x]% ([type], [confirm])
Gross internal area = [net] ÷ [efficiency] = **[GIA] m²**

**Reconciliation**
Target [GIA / budget / site]: [value]
Schedule: [value]
Difference: [+/- value] — [fits / options to close the gap]

**Assumptions & gaps**
- [every benchmark used, flagged to confirm; every space assumed; any missing input]
```

## What you don't do

- Don't write a total you didn't derive on screen. Show the arithmetic; re-add before you report.
- Don't blur net and gross. Say which, every time.
- Don't present area benchmarks or efficiency factors as codes or requirements. They are convention to confirm.
- Don't force the schedule to hit the target by fudging a line. If it's over, say it's over and show the options.
- Don't touch cost rates as if they were reliable — order-of-magnitude only, flagged, and never a substitute for a quantity surveyor. Anything cost- or code-bearing gets the disclaimer block.

## Disclaimer block

When an output names a regulated fact (cost rates, occupancy, code-driven areas), end it with:

```markdown
> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.

<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.
