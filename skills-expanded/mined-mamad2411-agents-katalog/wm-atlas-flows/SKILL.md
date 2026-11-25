---
name: wm-atlas-flows
description: >
  Extract flow links and their connected components from the comprehensive
  strategy map. Strips structural dependencies to show only dynamic
  relationships (data, signal, money flows). Identifies feedback loops
  as cycles in the flow graph. Adds minimal structural context.
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.1"
  skillset: wardley-mapping
  stage: "atlas"
  freedom: medium
---

# Atlas: Flow Dynamics

You are generating a **flow-focused map** from a comprehensive Wardley Map.
This is a derived artifact that strips away structural dependencies to
reveal the dynamic relationships: what moves between components, in which
direction, and what feedback loops exist.

## Prerequisites

Check that the project directory contains:
- `strategy/map.agreed.owm`
- `chain/supply-chain.agreed.md`

If `strategy/map.agreed.owm` is missing, tell the user to complete
`wm-strategy` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Staleness check

Compare modification times:
- **Sources**: `strategy/map.agreed.owm`, `chain/supply-chain.agreed.md`
- **Outputs**: `atlas/flows/map.owm`, `atlas/flows/analysis.md`

If all outputs exist and are newer than all sources, report that the
flows atlas is up to date and skip regeneration. If any source is newer,
or any output is missing, proceed.

## Step 1: Extract flow links

Read `strategy/map.agreed.owm` and extract every flow link:
- `A+>B` (forward flow)
- `A+<B` (reverse flow)
- `A+<>B` (bidirectional flow)
- `A+'label'>B`, `A+'label'<B`, `A+'label'<>B` (labelled flows)

For each flow, record: source, target, direction, label (if any).

Collect the set of all components that participate in at least one flow.

## Step 2: Add structural context

The flow-only components need enough context to be understandable. For
each flow-connected component:
1. Find its immediate parent in the dependency tree (one level up)
2. Find the anchor it ultimately serves (top of its chain)

Add these context components to the map. Do **not** add the full
dependency tree -- only the minimal scaffolding needed to understand
what each flow-connected component is and where it sits.

## Step 3: Identify feedback loops

Build a directed graph from the flow links. Search for cycles (strongly
connected components). A cycle means a feedback loop -- output from one
component eventually flows back to influence it.

For each cycle found, record:
- The components involved
- The flow labels (what circulates)
- Whether it is a reinforcing loop (positive feedback) or a balancing
  loop (negative feedback), based on what the flows carry

## Step 4: Generate flow map

Read [owm-dsl-reference.md](../wm-evolve/references/owm-dsl-reference.md)
for full OWM syntax.

Write `atlas/flows/map.owm`:

```owm
title {Organisation} — Flow Dynamics
// Derived from strategy/map.agreed.owm — do not edit directly

// Context anchors (only those connected to flow-participating components)
anchor {Anchor} [{vis}, {mat}]

// Flow-connected components (preserve original positions)
component {Component A} [{vis}, {mat}]
component {Component B} [{vis}, {mat}]

// Structural context (minimal — only parent links for orientation)
component {Parent} [{vis}, {mat}]
{Anchor}->{Parent}
{Parent}->{Component A}

// Flow links (the focus of this map)
{Component A}+'data'>{Component B}
{Component B}+'signal'<{Component A}

// Feedback loop annotations
annotation 1 [{vis}, {mat}] Feedback loop: {description}
annotations [0.90, 0.03]

style wardley
```

Guidelines:
- **Preserve original positions** so the reader can cross-reference with
  the full strategy map.
- **Include all flow links** from the source map, unchanged.
- **Structural dependencies** appear only as context scaffolding, not as
  the focus. Use annotated links (`;context`) to visually distinguish them.
- **Annotate each feedback loop** with a numbered annotation explaining
  what circulates and whether it reinforces or balances.

## Step 5: Write analysis

Write `atlas/flows/analysis.md`:

```markdown
# Flow Dynamics

## Flow inventory

| From | To | Direction | Carries | Notes |
|------|----|-----------|---------|-------|
| {A}  | {B} | forward  | {label} | {obs} |

## Feedback loops

### Loop {n}: {name}

**Components**: {list}
**Circulates**: {what flows around the loop}
**Type**: Reinforcing / Balancing
**Strategic implication**: {what this loop means — does it amplify
advantage, create runaway risk, stabilise operations?}

## Flow disruption risks

{For each flow, consider: what happens if it breaks? Which flows are
single-threaded with no redundancy? Which carry critical signals that
the organisation depends on for decision-making?}

## Dynamics and strategy

{How do the flows relate to strategic advantage? Are critical feedback
loops protected or exposed? Which flows could a competitor disrupt?
Where could new flows be added to strengthen the system?}
```

Read `chain/supply-chain.agreed.md` to ground the flow analysis in the
agreed dependency structure.

## Step 6: Render

```
bin/ensure-owm.sh clients/{org}/projects/{slug}/atlas/flows/map.owm
```

## Output

| File | Purpose |
|------|---------|
| `atlas/flows/map.owm` | Flow-focused map |
| `atlas/flows/map.svg` | Rendered SVG |
| `atlas/flows/analysis.md` | Flow dynamics analysis |

Present the SVG and analysis to the user. If the strategy map contains
no flow links, report that explicitly and explain that flows can be added
via `wm-iterate` using the `+>`, `+<`, `+<>` syntax.

After completion, regenerate the deliverable site:
```
bin/render-site.sh clients/{org}/projects/{slug}/
```
