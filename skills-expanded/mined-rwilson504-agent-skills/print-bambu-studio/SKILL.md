---
name: print-bambu-studio
description: 'Bambu Studio slicer reference: profiles, key settings per material, support strategies, plate management, .3mf project files, and lessons learned. USE FOR: slicing in Bambu Studio, choosing print profiles, support placement, infill choice, seam tuning, multi-color printing, troubleshooting slicer-side issues.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["bambu-studio","slicer","print-profiles","supports","infill"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/3dprint", "emoji": "🖨️" } }
---

# Bambu Studio — Slicer Reference

## Purpose
Accumulated slicer knowledge for **Bambu Studio**.
Companion to `print-bambu-p2s` (printer hardware). Updated every time a
slicer setting causes a problem or solves one.

> **Companion skills:**
> - `print-bambu-p2s` — printer hardware, calibration, maintenance
> - `cad-build123d-general` *(separate plugin)* — FDM design rules, if you
>   model with build123d

---

## Profiles

Bambu Studio ships with default profiles per (printer × nozzle × material).
Start there; tune from there.

### Default profile naming convention

`<Printer> <Nozzle> <Material> <Variant>`

Examples:
- `Bambu Lab P2S 0.4 nozzle Generic PLA`
- `Bambu Lab P2S 0.4 nozzle Bambu PETG HF`
- `Bambu Lab P2S 0.4 nozzle Generic ABS @BBL P2S`

When you tune a profile, **save as a new named profile** — never overwrite
the default. Use the format `<base> — <use case>`, e.g.
`P2S 0.4 PLA — Outdoor enclosures`.

## Key Settings by Material

### PLA (default workhorse)
| Setting | Value | Notes |
|---------|-------|-------|
| Nozzle temp | 220 °C | Lower (210) for finer detail; higher (230) for stronger bonds |
| Bed temp | 65 °C | Textured PEI |
| First layer speed | 50 mm/s | Slower = better adhesion |
| Print speed | 200 mm/s default | Bambu defaults are fine |
| Cooling | 100% from layer 2 | PLA loves cooling |
| Retraction | 0.8 mm | Default |
| Adaptive airflow | Cooling mode (auto) | P2S adaptive airflow draws cool external air — door stays closed (unlike P1S which needed cracking open) |

### PETG
| Setting | Value | Notes |
|---------|-------|-------|
| Nozzle temp | 250 °C | Higher than PLA for layer adhesion |
| Bed temp | 80 °C | Up to 85 °C for large parts |
| First layer speed | 30 mm/s | PETG needs squish; go slow |
| Cooling | 30–50% | Too much cooling = weak layers |
| Retraction | 1.0 mm | Slightly more than PLA to combat stringing |
| Z hop | Enabled (0.4 mm) | Reduces blob drag across surfaces |
| Adaptive airflow | Cooling mode (auto) | Door closed; adaptive system handles drafts |
| Brim | 5–8 mm for parts > 100 mm | PETG shrinks; brim catches edge lift |

### ABS / ASA
| Setting | Value | Notes |
|---------|-------|-------|
| Nozzle temp | 260 °C | |
| Bed temp | 100 °C | Max bed temp; needed for adhesion |
| First layer speed | 30 mm/s | |
| Cooling | 0% layer 1, then 20–30% | Too much cooling = warping |
| Adaptive airflow | Heating mode (auto) | P2S closes external intake; internal circulation traps heat |
| Brim | Always | ABS warps; brim is non-negotiable for any part |
| Ventilation | Required outside print | Fumes — P2S activated carbon filter handles VOCs but vent the room |

### TPU (95A+)
| Setting | Value | Notes |
|---------|-------|-------|
| Nozzle temp | 230 °C | |
| Bed temp | 50 °C | |
| Print speed | 30–50 mm/s | Slow — TPU compresses in the feeder |
| Retraction | Disabled or minimal | TPU stretches; retraction = jams |
| Cooling | 50% | |
| AMS | DO NOT USE | Print from external spool only |
| Infill | Gyroid | Preserves flexibility |

## Support Strategies

| Support type | When to use |
|--------------|-------------|
| **None** | Overhangs ≤ 45°, bridges < 5 mm |
| **Normal (auto)** | Standard overhangs, mechanical parts where surface finish under support doesn't matter |
| **Tree (auto)** | Organic shapes, isolated overhangs, minimizing material |
| **Tree (manual)** | Complex parts where auto places supports in hard-to-remove spots |
| **PVA / BVOH (AMS)** | Captured features (e.g. interior of a hollow shape); pricey but clean |
| **Painted on (custom)** | When you need precise control — paint exactly where supports go |

### Support tuning settings worth knowing

| Setting | Default | When to change |
|---------|---------|----------------|
| Support overhang threshold | 30° | Lower (20°) for crisper overhangs; higher (45°) to use less material |
| Support / object Z distance | 0.2 mm | Lower = harder to remove but better surface; higher = easier remove but rough |
| Support pattern | Rectilinear | Crosshatch for stronger support; gyroid for organic parts |
| Top interface layers | 2 | More = smoother top of supported surface; uses more material |

## Infill

| Pattern | Strengths | Use for |
|---------|-----------|---------|
| **Gyroid** | Equal strength all directions, good flow | Mechanical parts, default choice |
| **Grid** | Fast, simple | Quick prints, decorative |
| **Honeycomb / Adaptive Cubic** | Strong:weight ratio | Functional prints with weight constraints |
| **Lightning** | Fastest, just enough to support top layers | Cosmetic prints, prototypes |
| **Concentric** | Follows part outline | Flexible TPU parts |

| Density | Use for |
|---------|---------|
| 10–15% | Decorative, prototypes |
| 20% | Default — most functional parts |
| 30–40% | Mechanical load, threaded inserts |
| 50%+ | Structural / safety-critical (rare for FDM) |
| 100% | Don't — use more walls instead, it's stronger and faster |

**Wall count rule:** For mechanical strength, **add walls before adding
infill**. 4 walls + 15% infill is stronger than 2 walls + 50% infill,
and prints faster.

## Seam Placement

| Setting | When to use |
|---------|-------------|
| **Aligned (default)** | Visible seam in one column — predictable but ugly |
| **Random** | Seam scattered — less visible but adds tiny blobs |
| **Nearest** | Slicer picks closest point — fastest but inconsistent |
| **Painted seam** | Manual placement — best for cosmetic parts |

For visible parts, paint the seam onto a hidden edge (back, bottom corner).

## Plate Management

- One plate = one print job. Use multiple plates for multi-stage projects.
- Use **assembly view** for multi-part designs to verify mating before
  printing each piece.
- **Auto-arrange** is decent but doesn't know which faces are cosmetic;
  manually orient critical parts before slicing.

## Project Files (.3mf)

A `.3mf` project file bundles:
- The model(s)
- The plate layout
- The print profile
- Per-object settings (different material per object, support overrides, etc.)

**Always save the .3mf** for any project that might be reprinted. Drop it
in the project folder next to the source STL/STEP. Future-you will thank
present-you.

Naming convention: `<project-slug>-<variant>.3mf`, e.g.
`controller-enclosure-v3.3mf`.

## Lessons Learned

> **Append every new lesson here as it's discovered.** Format:
> `### YYYY-MM-DD — Short title` followed by Symptom / Root Cause / Fix.

*(No lessons documented yet — this section grows with use.)*

<!--
EXAMPLE FORMAT:

### 2026-04-30 — PETG seam blobs on cylindrical part

**Symptom:** Vertical line of small blobs running up a printed-cylinder
side, all aligned with the seam.

**Root cause:** Pressure advance not calibrated for the new spool of PETG;
slicer's "Aligned" seam piles all the over-extrusion at exactly one column.

**Fix:** Ran flow + pressure advance calibration in Bambu Studio for this
spool. Changed seam to "Painted" and placed it on a back-facing edge.

**Lesson:** New PETG spool = new calibration. And for cosmetic cylinders,
always use painted seams.
-->

## Quick Reference — Slicer Setting Diagnosis

| Symptom | Likely slicer cause | Setting to adjust |
|---------|--------------------|--------------------|
| Stringing | Retraction too low | +0.2 mm retraction; enable Z hop |
| Corner blobs | Pressure advance not tuned | Calibrate; lower outer wall speed |
| Top pillowing | Too few top layers or low infill | Top layers ≥ 5; infill ≥ 15% |
| Visible layer lines on curves | Layer height too coarse | Drop to 0.16 mm or 0.12 mm |
| Support scars on cosmetic surfaces | Support Z distance too low | Raise to 0.25 mm |
| Brim too hard to remove | Brim-object gap too low | Increase brim separation 0.05 mm |
| Multi-color bleeds at transitions | Purge volume too low | Raise per-transition purge volume |
| Slow print speed even at "fast" preset | Outer wall speed locked low | Bump outer wall speed (caution: surface quality trade) |
| Thin walls disappear | Wall thickness < 1 nozzle width | Redesign in CAD to ≥ 1.6 mm walls |

## See Also

- Bambu Studio docs: <https://wiki.bambulab.com/en/software/bambu-studio>
- Companion skill: `print-bambu-p2s` (printer hardware)
- Design-side rules: `cad-build123d-general` *(separate plugin)* § FDM print rules
