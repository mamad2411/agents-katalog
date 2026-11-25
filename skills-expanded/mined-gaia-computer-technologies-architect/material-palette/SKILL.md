---
name: material-palette
description: Propose a cohesive 3–5 material palette (with finishes, roles, aging forecast, and detailing notes) for an architectural concept, balanced for style, budget, climate, and maintenance. Use when material direction is open, when building a family around one anchor material, or when checking whether a palette has real internal logic rather than being a Pinterest collage. Say "suggest materials", "palette for a [style] house", or "what goes with [material]". Feeds render-prompt and space-feel.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Material Palette

Suggest a cohesive palette of 3-5 materials and finishes for an architectural project, based on style, budget, climate, and spatial intent.

## When to use

- Early design stages when material direction is open
- Client has named one material and you need to build a coherent family around it
- Translating a mood board into specifiable materials
- Checking whether a proposed palette has internal logic or is just a Pinterest collage

## Input

One or more of:
- Architectural style or reference projects
- Climate and orientation
- Budget bracket (social housing / mid-market / high-end / no-limit)
- One or two "anchor" materials the client has already chosen
- Spatial intent (monastic calm, industrial energy, domestic warmth, civic gravitas)

## Process

1. Identify the anchor material -- the one that sets the tone. If none given, derive from style and budget.
2. Select 2-4 supporting materials using the palette logic rules below.
3. Assign each material to a role: primary surface, secondary surface, accent, detail/hardware.
4. Check the palette against climate (will it weather well?), budget (is it buildable?), and maintenance reality.
5. Specify finish level: rough/honed/polished, treated/untreated, painted/natural.
6. Note aging characteristics -- how this palette will look in 5, 15, 50 years.

## Domain knowledge

### Material families

The full family reference — types, how each reads in light, how it ages, where it sits on cost — lives in [references/material-families.md](references/material-families.md). Load it when you need specifics for stone, timber, metal, ceramic/brick, plaster/lime, glass, or textile. Treat every performance and cost figure there as convention to verify against a real datasheet, not a specification.

### Palette logic

**The 3-material rule**: most successful architectural palettes use exactly 3 materials in a clear hierarchy -- one dominant (60%+ of surface area), one secondary (20-30%), one accent (5-10%). More than 5 materials usually means the palette lacks discipline.

**Contrast pairing**: pair one warm material with one cool. Timber + concrete. Brick + steel. Stone + glass. This creates visual tension that keeps a scheme alive.

**Texture gradient**: vary texture from rough to smooth across the palette. A scheme of all smooth materials feels sterile. All rough feels heavy. The gradient creates a reading order.

**Inside-outside continuity**: carry at least one material from exterior to interior (typically floor or wall) to dissolve the threshold. But change the finish -- exterior stone can be rough-split outside, honed inside.

**The "honest joint" test**: where two materials meet, the joint should be legible. Shadow gaps, expressed flashings, visible fixings, or deliberate reveals. Covering joints with sealant is a failure of detailing.

**Climate check**: in wet climates, avoid materials that stain from water runoff (pale render below Corten, soft stone below copper). In hot-arid climates, thermal mass materials (stone, concrete, rammed earth) outperform lightweight assemblies.

**Budget reality**: if budget is tight, spend money on what you touch (door handles, handrails, thresholds) and what catches light (window reveals, key wall surfaces). Use honest cheap materials (birch plywood, raw blockwork, painted steel) rather than fake versions of expensive ones.

## Output format

```
## Material Palette

### Anchor material
[Material + finish] — [role: primary surface]
[Why it sets the tone for this project]

### Supporting materials
| Material + finish | Role | Surface area | Why |
|---|---|---|---|
| ... | Secondary surface | ~25% | ... |
| ... | Accent / detail | ~5% | ... |
| ... | Hardware / joinery | Punctual | ... |

### Palette logic
[1-2 sentences on how these materials relate to each other]

### Aging forecast
- Year 1: [how it looks fresh]
- Year 5: [early patina]
- Year 20+: [mature character]

### Detailing notes
- [Key junction or joint to get right]
- [Maintenance regime]
```

## What you don't do

- Do not suggest materials you cannot specify. "Reclaimed wood" is not a specification. Species, dimensions, finish, source, and grade are.
- Do not mix more than one "hero" material. Two competing feature materials cancel each other out.
- Do not ignore maintenance. A beautiful material that looks terrible after 3 years without upkeep is a bad choice for most clients.
- Do not suggest materials purely for visual effect without considering thermal, acoustic, and structural performance.
- Do not default to the same safe palette (white walls, oak floors, black steel). Push when the project warrants it.
