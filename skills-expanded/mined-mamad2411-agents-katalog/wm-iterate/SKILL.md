---
name: wm-iterate
description: >
  Refine an existing Wardley Map in OWM format. Can adjust evolution
  positions, split components into pipelines, add or remove dependencies,
  create submaps for detailed areas, add market forces, or compare map
  versions. Use when you have an existing OWM map that needs refinement
  based on new information, changed context, or client feedback.
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "6+"
  freedom: medium
---

# Wardley Map Iteration and Refinement

You are refining an existing Wardley map in OWM format. This is an
open-ended skill for ongoing map maintenance and evolution.

## Prerequisites

Check that the project directory contains at least one `.owm` file.
Typical locations under `clients/{org}/projects/{project-slug}/`:
- `evolve/map.owm` or `evolve/map.agreed.owm`
- `strategy/map.owm` or `strategy/map.agreed.owm`

If no OWM file exists, tell the user to complete earlier stages first
(at minimum through `wm-evolve`).

Read [owm-dsl-reference.md](references/owm-dsl-reference.md) for the
full OWM DSL syntax.

## Identify the working map

Ask the user which map to refine, or determine from context:
- If a `strategy/map.agreed.owm` exists, that is likely the current map
- If only `evolve/map.agreed.owm` exists, use that
- The user may specify a different file

Read the current map and `decisions.md` for context.

## Refinement operations

Based on the user's request, perform one or more of these operations:

### Adjust evolution positions

Move components left or right on the maturity axis:
```owm
// Before
component Platform [0.60, 0.35]
// After
component Platform [0.60, 0.55]
```

Update the corresponding assessment in `evolve/assessments/` if it
exists, noting why the position changed.

### Split into pipeline

Replace a single component with a pipeline showing variants:
```owm
// Before
component Delivery [0.65, 0.45]

// After
pipeline Delivery
{
  component Legacy Delivery [0.25]
  component Modern Delivery [0.55]
  component API Delivery [0.72]
}
```

Update dependencies — things that depended on the original component
now depend on specific variants.

### Add or remove components

New information may reveal missing components or show that listed
components don't actually exist as distinct things.

When adding: determine visibility from its position in the dependency
chain, evolution from assessment.

When removing: ensure all dependencies to/from the component are
also removed or redirected.

### Add or modify dependencies

```owm
// Add a dependency
NewParent->ExistingComponent

// Add an annotated dependency
Component->Dependency; context note

// Add a flow
DataSource+'real-time'>Consumer
```

### Create submaps

When an area of the map is too detailed for the main map:

1. Extract the cluster into a new `.owm` file
2. Replace the cluster in the main map with a `submap` element:
   ```owm
   submap Fleet Management [0.65, 0.48] url(fleet)
   url fleet [path/to/fleet-management.owm]
   ```
3. Redirect dependencies to point at the submap

### Add market forces

```owm
accelerator AI commoditisation [0.50, 0.55]
deaccelerator Regulatory lock-in [0.60, 0.40]
```

### Add or update annotations

**Keep each annotation under 12 words** so it fits on one line in the
rendered legend.
```owm
annotation 3 [0.55, 0.42] New insight from client feedback
note +Warning: vendor lock-in risk [0.48, 0.72]
```

### Compare versions

If the user asks to compare map versions:
1. Read both `.owm` files
2. Identify differences:
   - Components added, removed, or repositioned
   - Dependencies changed
   - Strategic elements added or removed
3. Summarise the changes in plain language

## Working with the client

For each proposed change:
1. Explain **what** you're changing and **why**
2. Show the relevant OWM snippet before and after
3. Ask for confirmation before writing

For larger refactoring:
1. Present a summary of all proposed changes
2. Get agreement on the overall direction
3. Apply changes
4. Present the updated map for final review

## Rendering

After writing or updating any `.owm` file, render it to SVG:
```
bin/ensure-owm.sh path/to/map.owm
```

This checks for `cli-owm` and installs it if missing, then produces
an SVG alongside the OWM file. Show the SVG to the client.

## After making changes

1. Write the updated map (to the same file, or a new version if the
   user prefers)
2. If the change is significant enough to warrant client sign-off,
   produce a new `.agreed.owm` and record the update:
   ```
   wm-iterate/scripts/record-update.sh --client {org} --project {slug} \
     --title "{description of what changed}" \
     --field "Changes={summary}" --field "Reason={why}"
   ```
3. Summarise what changed and why

## Common iteration patterns

### "The map doesn't feel right"
Start by asking **which components** feel wrong. Often it's evolution
positions that need adjustment. Walk through the evolution
characteristics for the contested components.

### "Things have changed since we mapped this"
Identify what changed (new product launch, acquisition, regulation,
technology shift). Trace the impact through the map — which components
are affected? Do positions or dependencies change?

### "We need more detail in this area"
Create a submap for the area. Decompose the high-level component into
its constituent parts. Position and assess evolution for each.

### "We want to explore a scenario"
Copy the current map to a new file (e.g. `scenario-cloud-migration.owm`).
Apply the hypothetical changes. Compare with the current map to
visualise the impact.

### "New user/need identified"
Add the anchor and need. Trace its supply chain down through existing
components (reuse where possible) and new ones. Assess evolution of
any new components.
