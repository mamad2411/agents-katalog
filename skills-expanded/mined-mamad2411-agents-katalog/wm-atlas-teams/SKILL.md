---
name: wm-atlas-teams
description: >
  Apply Wardley's Pioneers/Settlers/Town Planners team model to the
  strategy map. Produces a map with PST bounding box overlays showing
  which components belong to which team archetype. Analyses skills,
  culture, handoff points, and hiring priorities for each zone.
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.1"
  skillset: wardley-mapping
  stage: "atlas"
  freedom: medium
---

# Atlas: Team Topology (Pioneers / Settlers / Town Planners)

You are generating a **team-focused map** applying Wardley's Pioneers,
Settlers, Town Planners (PST) model to a comprehensive strategy map.
The output shows which components belong to which team archetype and
analyses the organisational implications.

## Prerequisites

Check that the project directory contains:
- `strategy/map.agreed.owm`

If `strategy/map.agreed.owm` is missing, tell the user to complete
`wm-strategy` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Staleness check

Compare modification times:
- **Sources**: `strategy/map.agreed.owm`
- **Outputs**: `atlas/teams/map.owm`, `atlas/teams/analysis.md`

If all outputs exist and are newer than all sources, report that the
teams atlas is up to date and skip regeneration. If any source is
newer, or any output is missing, proceed.

## Step 1: Classify components by evolution zone

Read `strategy/map.agreed.owm` and classify every component:

| Zone | Evolution range | Team archetype |
|------|----------------|----------------|
| Genesis + early Custom | 0.00 - 0.30 | Pioneers |
| Late Custom + Product | 0.30 - 0.60 | Settlers |
| Late Product + Commodity | 0.60 - 1.00 | Town Planners |

For each component, record its name, position, and assigned zone.

Handle edge cases:
- **Pipeline components**: different variants may span zones. Note which
  variants belong to which team.
- **Components with evolve arrows**: the current position determines
  current ownership, but the evolve target indicates a future handoff.
- **Components with inertia in transition zones**: these are likely
  handoff friction points.

## Step 2: Determine PST bounding boxes

Calculate bounding boxes for each zone using the `[y1, x1, y2, x2]`
syntax. The boxes should:
- Cover all components in that zone with some padding
- Use the full visibility range of the components in the zone
- Not overlap (adjust boundaries at the zone edges)

Typical defaults if components are spread across the full map:
```
pioneers [0.95, 0.00, 0.10, 0.30]
settlers [0.95, 0.30, 0.10, 0.60]
townplanners [0.95, 0.60, 0.10, 1.00]
```

Adjust these based on the actual distribution of components. If a zone
has no components, omit its bounding box and note this in the analysis.

## Step 3: Identify handoff points

Find components where:
1. A **dependency crosses zone boundaries** -- the parent is in one zone
   and the child is in another. These are inter-team interfaces.
2. An **evolve arrow crosses zone boundaries** -- a component is moving
   from one team's domain to another. These are future handoffs.
3. **Inertia sits on a zone boundary** -- resistance to the handoff
   itself.

## Step 4: Generate teams map

Read [owm-dsl-reference.md](../wm-evolve/references/owm-dsl-reference.md)
for full OWM syntax.

Write `atlas/teams/map.owm`:

```owm
title {Organisation} — Team Topology (PST)
// Derived from strategy/map.agreed.owm — do not edit directly

// PST bounding boxes
pioneers [{y1}, {x1}, {y2}, {x2}]
settlers [{y1}, {x1}, {y2}, {x2}]
townplanners [{y1}, {x1}, {y2}, {x2}]

// Anchors (preserve all)
anchor {Anchor} [{vis}, {mat}]

// Pioneer zone components
component {Genesis Component} [{vis}, {mat}]

// Settler zone components
component {Product Component} [{vis}, {mat}]

// Town Planner zone components
component {Commodity Component} [{vis}, {mat}]

// Dependencies (preserve all)
{Parent}->{Child}

// Evolve arrows crossing zone boundaries (handoff indicators)
evolve {Component} {target}

// Handoff annotations
annotation 1 [{vis}, {mat}] Handoff: pioneers to settlers
annotations [0.90, 0.03]

// Zone boundary notes
note +Cross-zone dependency [{vis}, {mat}]

style wardley
```

Guidelines:
- **Preserve all components and dependencies** from the source map.
- **Include the PST bounding boxes** using the `pioneers`, `settlers`,
  `townplanners` keywords with `[y1, x1, y2, x2]` coordinates.
- **Annotate cross-zone dependencies** to highlight team interfaces.
- **Mark evolve arrows that cross zones** -- these represent planned
  handoffs from one team archetype to another.

## Step 5: Write analysis

Write `atlas/teams/analysis.md`:

```markdown
# Team Topology: Pioneers / Settlers / Town Planners

## Component distribution

| Zone | Components | Count |
|------|-----------|-------|
| Pioneers (genesis/early custom) | {list} | {n} |
| Settlers (late custom/product) | {list} | {n} |
| Town Planners (commodity) | {list} | {n} |

## Zone profiles

### Pioneers

**Components**: {list}
**Skills needed**: Experimentation, research, tolerance for failure,
rapid prototyping, domain expertise.
**Culture**: High autonomy, low process, comfort with ambiguity.
**Key question**: {what capability is being explored or invented here?}

### Settlers

**Components**: {list}
**Skills needed**: Product management, engineering discipline, user
research, API design, documentation.
**Culture**: Balance of innovation and reliability, customer focus.
**Key question**: {what's being productised and for whom?}

### Town Planners

**Components**: {list}
**Skills needed**: Operations, SRE, vendor management, cost
optimisation, compliance, scale engineering.
**Culture**: Efficiency, reliability, standardisation, measurement.
**Key question**: {what's being operated as utility infrastructure?}

## Handoff points

| From | To | Component | Trigger |
|------|----|-----------|---------|
| Pioneers | Settlers | {component} | {evolve arrow / maturity signal} |
| Settlers | Town Planners | {component} | {evolve arrow / maturity signal} |

{For each handoff: what needs to happen for this transition to succeed?
What artefacts must the originating team produce? What does the
receiving team need to be ready for?}

## Cross-zone dependencies

{Dependencies that cross zone boundaries. These are inter-team
interfaces that need explicit contracts, APIs, or coordination
mechanisms. Each cross-zone dependency is a potential source of
friction.}

## Hiring and capability focus

{Based on the component distribution: where should the organisation
invest in hiring? If most components are in the settler zone, the
organisation needs strong product engineers. If pioneers dominate,
it needs researchers and experimenters. If town planners dominate,
it needs operators and vendor managers.}

## Pipeline implications

{For pipeline components spanning zones: the pioneer end needs
different management than the town planner end. How should ownership
be structured?}
```

## Step 6: Render

```
bin/ensure-owm.sh clients/{org}/projects/{slug}/atlas/teams/map.owm
```

## Output

| File | Purpose |
|------|---------|
| `atlas/teams/map.owm` | PST-annotated map |
| `atlas/teams/map.svg` | Rendered SVG |
| `atlas/teams/analysis.md` | Team topology analysis |

Present the component distribution table and SVG first, then offer the
detailed zone profiles and handoff analysis. This is a derived view --
no client agreement gate is needed.

After completion, regenerate the deliverable site:
```
bin/render-site.sh clients/{org}/projects/{slug}/
```
