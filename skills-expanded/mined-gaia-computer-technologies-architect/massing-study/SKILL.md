---
name: massing-study
description: Tests what a site can hold. From a site boundary and the architect's envelope rules (per-edge setbacks, maximum height, floor-to-floor heights, site coverage, FAR or plot ratio, net-to-gross efficiency) it computes footprint, storeys, gross and net area, unit count and the governing constraint, writes a stacked 3D massing (glTF and OBJ) with plan and axonometric images, and can rebuild the massing in Rhino or Blender through their MCP servers when connected. Every planning input is echoed back as user-supplied and to be verified. Use when the architect wants a "feasibility study", "massing", "yield study", "how much can we build", "capacity study", "development potential", "FAR test", or "test option A against option B". Takes site area from site-map, targets from programme-schedule, and checks with area-check; hands to sun-study and site-context for consequences.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Massing Study

A capacity study answers one question fast: given these rules, what fits, and which rule bites? This skill computes it transparently, line by line, from rules the architect supplies, and draws a massing you can open anywhere. It doesn't know the local zoning. It never pretends to.

## When to use

- Bid or feasibility stage: is the client's target area achievable on this site?
- Comparing envelope options (more height and less coverage, a different setback, a FAR bonus).
- Producing a quick 3D massing for a context model, a sun study or a client call.

## Input

All planning numbers come from the architect, from the actual planning or zoning documents. You don't supply them from memory.

- **Site boundary**: vertices in local metres, in order around the site. Take them from a survey, a title plan, `site-map`, or `dxf-drawing` coordinates.
- **Setbacks**: a default, plus per-edge values (edge i runs from vertex i to vertex i+1). Front, side and rear setbacks, building lines and easements all go here.
- **Maximum height**, plus **floor-to-floor heights** for ground and typical floors.
- Optional caps: **site coverage** (footprint over site area), **FAR** (also called plot ratio, FSI, GFZ or floor area ratio; the definitions differ, so confirm what counts as floor area), and a **maximum number of storeys**.
- **Efficiency** (net over gross) as the architect's assumption for the building type, and optionally **average net area per unit** for a unit count.

## Process

1. **Collect the rules and their source** (plan policy, zoning code section, pre-application advice). Note which are firm and which are negotiable.
2. **Write the spec** (JSON format at the top of `scripts/massing.py`) and run it:
   `uv run scripts/massing.py option-a.json --out out/option-a`
   It refuses when a required planning input is missing rather than defaulting it.
3. **Read the calculation log** in the report. It covers site area, footprint after setbacks, coverage trimming, storeys by height, GFA, the FAR cut, net area, units, and which constraint governs footprint and which governs height. Each line shows its arithmetic.
4. **Look at the plan and axonometric images** to confirm the setbacks sit on the edges you intended.
5. **Run variants** by copying the spec and changing one rule at a time. Report options side by side, with the governing constraint for each.
6. **Optional, in Rhino or Blender.** If a Rhino MCP or Blender MCP is connected, rebuild the massing there from the same footprint and storey heights so the architect can keep working in their own model. Check document units first, work on a named layer or collection, and screenshot to confirm. See [references/tool-notes.md](references/tool-notes.md).

## Domain knowledge

- **Setbacks as half-planes.** Each edge's setback is applied as an inward offset of that edge, and the buildable area is what survives all of them. Sharp site corners lose more area than you'd expect, so the buildable percentage of the site is worth quoting.
- **Coverage trimming.** When coverage binds, the footprint is pulled in uniformly. A real scheme would carve courtyards or notches instead. The area result is the same; the shape isn't a design.
- **Storeys from height.** n = 1 + floor((H - ground) / typical). That gives the top of structure, before parapet, roof build-up, plant and lift overrun. Many codes measure height to a specific datum (ridge, parapet, eaves, average grade), so confirm the definition.
- **FAR definitions vary.** Whether basements, plant, balconies, parking, voids or wall thickness count differs by jurisdiction. The script treats GFA as footprint times storeys. Say so, and adjust if the local definition differs.
- **Efficiency is an assumption.** Net-to-gross depends on core strategy, plate depth, corridor type and building type. Ask the architect for theirs, or derive it from a comparable scheme of their own. Don't quote a "typical" figure without a source.
- **What a simple extrusion misses.** Daylight and sky-exposure planes, stepped setbacks above certain heights, separation distances, rights of light, fire access, amenity space, parking and servicing. Any of these can govern instead of the numbers here. The report lists them as not modelled.
- **Units.** Metres throughout. For feet, convert the inputs (1 ft = 0.3048 m) and say so.

## Output format

```
## Massing study: [site], [option]

Planning inputs (USER-SUPPLIED, TO VERIFY): [height, setbacks, coverage, FAR, source of each]

| Option | Footprint | Storeys | GFA | Net | Units | FAR | Coverage | Governs |
|---|---|---|---|---|---|---|---|---|
| A | 802 m2 | 5 | 4,008 m2 | 3,206 m2 | 49 | 3.00 | 60% | coverage / FAR |

Calculation log: [from the report, every line with its arithmetic]
Not modelled: [daylight planes, separation, cores, plant, parking...]
Files: option-a.glb, option-a.obj, option-a_plan.png, option-a_axo.png

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't supply setbacks, heights, FAR or coverage from memory or "typical" zoning. Ask for the document.
- Don't present a yield as achievable or approvable. It is arithmetic on stated rules.
- Don't hide the governing constraint. It is usually the most useful line in the study.
- Don't edit an architect's Rhino or Blender file without saying what you will create, and where, first.
