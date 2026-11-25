---
name: wm-strategy
description: >
  Add strategic annotations to a positioned Wardley Map. Identifies
  evolution opportunities, build/buy/outsource decisions, inertia
  barriers, pipeline opportunities, and competitive dynamics. Produces
  an annotated OWM map with evolve arrows, execution strategies,
  pipelines, and annotations. Use after evolution map is agreed
  (map.agreed.owm exists in evolve/).
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "5"
  freedom: medium
---

# Strategic Annotation for Wardley Maps

You are conducting the **strategy phase** of a Wardley mapping engagement.
The map is positioned — you are now adding strategic moves, decisions,
and annotations that make the map actionable.

## Prerequisites

Check that the project directory contains:
- `evolve/map.agreed.owm`
- `chain/supply-chain.agreed.md`
- `needs/needs.agreed.md`
- `brief.agreed.md`
- `decisions.md`

Check that the client workspace contains:
- `resources/index.md`

If `evolve/map.agreed.owm` is missing, tell the user to complete
`wm-evolve` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Step 1: Analyse the positioned map

Read `evolve/map.agreed.owm` and identify strategic opportunities
by examining:

### Evolution opportunities
- Components in **Genesis or Custom** that the market is evolving
  toward Product or Commodity. These are candidates for `evolve`
  arrows.
- Components where the organisation is **behind the market** — using
  custom solutions for things that are available as products.
- Components where the organisation could **lead evolution** —
  commoditising something to gain efficiency or undermine competitors.

### Execution strategy
- Components currently built in-house that should be **bought** or
  **outsourced** (high maturity, not a differentiator).
- Components currently outsourced that should be **built** in-house
  (low maturity, potential differentiator).
- Components where the current execution strategy doesn't match their
  evolution stage.

### Pipeline opportunities
- Components where **multiple variants exist** at different evolution
  stages (e.g. legacy system alongside a modern replacement). These
  are candidates for `pipeline` elements.

### Market dynamics
- **Accelerators**: external forces pushing components to evolve
  faster (regulation, technology shifts, competitor moves).
- **Decelerators**: forces slowing evolution (lock-in, regulation,
  standards bodies).

### Structural insights
- **Single points of failure**: components many things depend on.
- **Competitive advantages**: custom components that differentiate.
- **Waste**: commodity components being treated as custom.
- **Duplication**: multiple components serving the same purpose.

## Step 2: Write strategic analyses

For each identified play, write a brief analysis to
`strategy/plays/{play-slug}.md`:

```markdown
# {Play Name}

## Observation

{What you see in the map — the current state}

## Proposal

{What strategic move this suggests}

## Impact

{What changes if this play is executed — which components move,
which dependencies change, what risks arise}

## Evidence

{References to research, supply chain, or evolution assessments
supporting this play}
```

## Step 3: Generate strategy map

Read [owm-dsl-reference.md](references/owm-dsl-reference.md) for the
full OWM syntax.

Start from `evolve/map.agreed.owm` and add strategic elements.
Write to `strategy/map.owm`.

### Evolve arrows

For components with identified evolution opportunities:
```owm
evolve Current Name 0.65
evolve Old Name->New Name 0.72
evolve Component 0.80 (outsource)
```

### Execution strategies

For components with build/buy/outsource recommendations:
```owm
component Custom Platform [0.60, 0.35] (build)
component CRM System [0.55, 0.62] (buy)
component Email Service [0.40, 0.85] (outsource)
```

### Pipelines

For components with variants at different evolution stages:
```owm
pipeline Delivery Platform
{
  component Legacy System [0.25]
  component New Platform [0.55]
}
```

### Annotations

For key strategic insights (numbered, with a legend). **Keep each
annotation under 12 words** so it fits on one line in the rendered legend.
```owm
annotation 1 [0.65, 0.30] Key differentiator — protect from commoditisation
annotation 2 [[0.55, 0.72],[0.40, 0.85]] Outsource these commodities together
annotations [0.90, 0.03]
```

### Notes

For observations that don't warrant numbered annotations:
```owm
note +Key risk: single supplier [0.48, 0.65]
note Regulatory change expected 2026 [0.30, 0.55]
```

### Market forces

```owm
accelerator AI commoditisation [0.50, 0.55]
deaccelerator Regulatory lock-in [0.60, 0.40]
```

## Rendering

After writing any `.owm` file, render it to SVG:
```
bin/ensure-owm.sh clients/{org}/projects/{slug}/strategy/map.owm
```

This checks for `cli-owm` and installs it if missing, then produces
`strategy/map.svg`. Show the SVG to the client alongside the OWM source.

## Step 4: Present to client

Present:
1. A summary of identified strategic plays
2. The annotated map and its rendered SVG
3. For each `evolve` arrow: why this component should move, and what
   that requires

Ask:
1. "Do these strategic moves make sense given your organisational
   context?"
2. "Are there constraints I'm not seeing that would prevent any of
   these moves?"
3. "Which plays are highest priority?"
4. "Are the build/buy/outsource recommendations aligned with your
   strategy?"

## Step 5: Iterate and agree

Based on client feedback:
1. Update plays in `strategy/plays/`
2. Regenerate `strategy/map.owm`
3. Present again until the client is satisfied

When the client agrees:
1. Copy to `strategy/map.agreed.owm`
2. Record the agreement:
   ```
   wm-strategy/scripts/record-agreement.sh --client {org} --project {slug} \
     --field "Key plays={list of agreed strategic moves}" \
     --field "Priorities={which plays the client considers most important}" \
     --field "Deferred={plays considered but deferred, with reasoning}"
   ```

## Guidelines

- **Less is more.** A map with 3-4 clear strategic moves is more
  useful than one with 15 arrows going everywhere. Focus on the
  most impactful plays.
- **Every evolve arrow should have a reason.** Don't add movement
  just because something "could" evolve. The client needs to
  understand why and what it would take.
- **Annotations should provide insight, not description.** "This is
  a database" is not an annotation. "Single point of failure serving
  5 user needs" is.
- **Keep the map readable.** Use label offsets, limit annotations,
  and consider whether a submap would be clearer than cramming
  everything onto one map.

## Completion

When `map.agreed.owm` is written, tell the user:
- The map is now a strategic tool they can act on
- They can use `wm-iterate` for ongoing refinement
- They can re-render the OWM file at any time with
  `bin/ensure-owm.sh path/to/map.owm`, or paste it into
  [onlinewardleymaps.com](https://onlinewardleymaps.com)
