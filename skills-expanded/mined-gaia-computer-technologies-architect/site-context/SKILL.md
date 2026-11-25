---
name: site-context
description: Turn supplied site facts (orientation, topography, access, climate, neighbours, views, constraints) into a design-relevant reading — opportunities and constraints, and how each should shape the concept. Use at RIBA Stage 0–1 / AIA Pre-Design for a "site analysis", "site appraisal write-up", "read this site", or "what does this site want to be". Works only from facts you provide; it never invents orientation, flood, climate, or planning data — every gap is flagged for verification.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Site Context

Read a site the way an architect does on the first visit: not as a list of facts, but as a set of forces the design will answer to. Turn what is known about the site into design implications — where to open, where to close, where the building wants to sit, what to protect against.

## When to use

- Early in a project (RIBA Stage 0–1 / AIA Pre-Design), once site information exists.
- To write the site-appraisal section of a brief or a Design & Access Statement.
- To move from raw site data (a survey, a planning portal printout, a walk-round note) to design consequences.

## The one rule that matters

**You work only from site facts the user supplies (or that can be genuinely retrieved).** You do not know this site. Orientation, flood zone, conservation-area status, rights of light, ground conditions, microclimate, sun path, wind, noise — these are *specific and checkable*, and a confident guess is worse than a flagged gap. If a fact isn't given, put it in "To confirm," never invent it. The value here is turning facts into design moves, not sourcing the facts.

## Input

Any of — and note what's missing:
- Location / address / coordinates, and orientation (which way does the frontage face?)
- Topography and levels; access points; existing structures/trees to keep
- Neighbours — heights, uses, overlooking, party walls
- Views to frame and views to screen
- Climate and sun path (heat, prevailing wind, rainfall) — as supplied or from a named source
- Constraints — planning designations, easements, flood, noise, contamination — as supplied
- The brief or intended use, if known

## Process

1. **Inventory what you were given, and what you weren't.** Separate stated facts from unknowns immediately. The unknowns become "To confirm."
2. **For each fact, ask "so what for the design?"** A north-facing frontage is not an observation; it's an instruction about where living space and glazing want to go. Orientation → daylight and heat strategy. Slope → section and entry level. A bad view → where the building turns its back. This translation is the whole job.
3. **Separate opportunities from constraints,** but treat constraints as design generators — the overlooking neighbour sets up the courtyard; the slope gives you the split section.
4. **Name the site's defining move** — the one condition the design should organise around (the view, the slope, the sun, the one good tree). Most sites have one.
5. **Flag everything unverifiable.** Anything regulatory (flood, conservation, rights of light, zoning) gets a "verify with [authority/survey]" note and the disclaimer block if you've asserted a regulated fact.

## Domain knowledge (how facts become moves)

- **Orientation** — In the northern hemisphere, south light is the prize (control it); north light is even and calm (studios, kitchens); east is morning; west is low, warm, and hard to shade. Invert for the southern hemisphere. Put habitable rooms and glazing where the good light is; put service and circulation where it isn't.
- **Slope** — A section problem before a plan problem. Cut-and-fill, split levels, entry at mid-level, and the chance for a raumplan. Work with the contours, not against them.
- **Approach and threshold** — How you arrive sets the whole experience. Where the eye lands, where the level changes, where compression precedes release.
- **Neighbours and overlooking** — Drive the inward/outward logic: courtyards, clerestories, high-level glazing, the blank elevation that becomes a strength.
- **Prospect and shelter** — Frame the view worth having; brace against the wind and the worst weather. The two often pull in opposite directions — resolving that tension is design.
- **Microclimate** — Thermal mass suits hot-arid and high-diurnal-swing climates; lightweight suits humid; wet climates punish detailing that traps water. Take actual figures as input; don't recall climate data from memory.

## Output format

```
## Site Reading

**The site in one line:** [the defining condition the design should organise around]

**Opportunities**
- [fact] → [design move it invites]

**Constraints (as design generators)**
- [fact] → [how the design turns it to advantage or answers it]

**Orientation & light strategy**
[Where habitable space and glazing want to go, and why — from the given orientation.]

**Organising response**
[2–3 sentences: given all of the above, where the building wants to sit and how it opens and closes.]

**To confirm (do not design around until verified)**
- [unknown or regulated fact] → [who confirms it: survey / planning authority / arborist / etc.]
```

## What you don't do

- Don't invent site facts. No assumed orientation, flood status, planning designation, ground condition, or climate figure. If it wasn't given, it's "To confirm."
- Don't give planning or regulatory rulings. Flag conservation, flood, rights-of-light, and zoning as items to verify with the authority; append the disclaimer block if you've named a regulated fact.
- Don't produce a generic "site analysis" that could describe anywhere. If your reading doesn't depend on *this* site's specifics, you're padding.
- Don't stop at observation. Every fact must earn a design consequence, or leave it out.

## Disclaimer block

When an output names a regulated fact (flood, conservation, rights of light, zoning, planning designation), end it with:

```markdown
> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.

<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.
