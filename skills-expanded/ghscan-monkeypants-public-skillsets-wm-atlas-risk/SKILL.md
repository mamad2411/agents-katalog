---
name: wm-atlas-risk
description: >
  Risk analysis combining structural signals from the strategy map:
  single points of failure, deep dependency chains, inertia on critical
  paths, external dependencies with limited alternatives, and components
  with no evolution path. Produces a risk-annotated map and detailed
  analysis with likelihood, impact, and mitigation per risk cluster.
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.1"
  skillset: wardley-mapping
  stage: "atlas"
  freedom: medium
---

# Atlas: Risk Analysis

You are generating a **risk-focused map** from a comprehensive Wardley
Map. This view combines multiple structural signals to identify where
things could go wrong. The output is a risk-annotated map and a detailed
risk register.

## Prerequisites

Check that the project directory contains:
- `strategy/map.agreed.owm`
- `chain/supply-chain.agreed.md`
- `evolve/assessments/*.md`
- `strategy/plays/*.md`
- `decisions.md`

If `strategy/map.agreed.owm` is missing, tell the user to complete
`wm-strategy` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Staleness check

Compare modification times:
- **Sources**: `strategy/map.agreed.owm`, `chain/supply-chain.agreed.md`,
  `evolve/assessments/*.md`, `resources/index.md`
- **Outputs**: `atlas/risk/map.owm`, `atlas/risk/analysis.md`

If all outputs exist and are newer than all sources, report that the
risk atlas is up to date and skip regeneration. If any source is newer,
or any output is missing, proceed.

## Step 1: Build the dependency graph

Read `strategy/map.agreed.owm` and construct the full dependency graph.
For each component, compute:
- **Fan-in**: how many components depend on it (incoming edges)
- **Fan-out**: how many components it depends on (outgoing edges)
- **Depth**: longest path from any anchor to this component
- **Reach**: how many anchors can transitively reach this component

Read `chain/supply-chain.agreed.md` for any structural details not
captured in the OWM dependencies.

## Step 2: Identify risk signals

Scan for each of these structural risk patterns:

### Single points of failure
Components with high fan-in (3+ dependents) and no pipeline or
alternative. If this component fails, multiple capabilities break.

### Deep dependency chains
Paths of 4+ links from anchor to leaf. Longer chains mean more
opportunities for failure and harder debugging.

### Inertia on critical paths
Components marked `inertia` that sit on the critical path (the longest
dependency chain from anchor to leaf). Inertia here blocks the most
important evolution moves.

### External dependencies
Components that represent third-party services, vendors, or market
ecosystems. Check: are there alternatives? What's the switching cost?
Re-read research for vendor lock-in signals.

### No evolution path
Components with no `evolve` arrow and no play addressing them, sitting
at an evolution stage that won't remain stable. Stagnation risk.

### Execution strategy gaps
Components with no `(build)`, `(buy)`, or `(outsource)` decorator.
Unclear ownership is a risk signal.

## Step 3: Contextualise risks from analytical artifacts

For each identified risk signal, read the analytical work:

1. **Evolution assessments** (`evolve/assessments/*.md`): Evolution
   stage and inertia evidence for risk-flagged components. A component
   stuck in custom with inertia is riskier than one evolving toward
   commodity.
2. **Strategy plays** (`strategy/plays/*.md`): Do any plays address
   or depend on risk-flagged components? A risk on a component
   targeted by a strategic play has higher urgency.
3. **Decisions log** (`decisions.md`): Were risks discussed during
   client feedback loops? The client may have flagged mitigating
   factors or confirmed concerns.

Supplement from primary research (`resources/`) only for:
- Corroborating evidence not in assessments (outage history, vendor
  concentration data)
- Mitigating or aggravating factors not captured in analytical work

## Step 4: Cluster and score risks

Group related risk signals into **risk clusters** -- a cluster is a
connected set of components that share or compound a risk. For each
cluster:

- **Likelihood**: High / Medium / Low -- how probable is the failure?
- **Impact**: High / Medium / Low -- what breaks if it happens?
- **Mitigation**: what could reduce likelihood or impact?

## Step 5: Generate risk map

Read [owm-dsl-reference.md](../wm-evolve/references/owm-dsl-reference.md)
for full OWM syntax.

Write `atlas/risk/map.owm`:

```owm
title {Organisation} — Risk Map
// Derived from strategy/map.agreed.owm — do not edit directly

// Anchors (preserve all)
anchor {Anchor} [{vis}, {mat}]

// All components (preserve original positions)
component {Component} [{vis}, {mat}]

// Dependencies (preserve all — full graph needed for risk context)
{Parent}->{Child}

// Risk annotations — one per cluster
annotation 1 [{vis}, {mat}] {Risk cluster summary}
annotation 2 [[{vis1}, {mat1}],[{vis2}, {mat2}]] {Risk spanning components}
annotations [0.90, 0.03]

// Risk notes — for individual risk signals
note +SPOF: {n} dependents, no alternative [{vis}, {mat}]
note +No evolution path [{vis}, {mat}]
note +Deep chain: {depth} links [{vis}, {mat}]
note +Vendor lock-in [{vis}, {mat}]

style wardley
```

Guidelines:
- **Preserve the full map structure.** Risk context requires seeing all
  dependencies, not a pruned subset.
- **Use notes liberally** to mark individual risk signals directly on
  the component. Prefix with `+` for emphasis.
- **Use annotations** for risk clusters that span multiple components.
  The annotation legend serves as the risk register summary.
- **Keep annotations under 12 words** per the rendering constraint.

## Step 6: Write analysis

Write `atlas/risk/analysis.md`:

```markdown
# Risk Analysis

## Risk register

| # | Cluster | Likelihood | Impact | Components | Signal |
|---|---------|-----------|--------|------------|--------|
| 1 | {name}  | H/M/L     | H/M/L  | {list}     | {type} |

## Detailed risk clusters

### Risk {n}: {Cluster name}

**Likelihood**: {H/M/L} — {reasoning}
**Impact**: {H/M/L} — {what breaks, who is affected}
**Signal type**: {SPOF / deep chain / inertia / external / stagnation}

**Components involved**:
- {Component}: {specific risk signal for this component}

**Research evidence**: {what the research says about this risk area}

**Mitigation options**:
1. {Concrete action to reduce likelihood or impact}
2. {Alternative approach}

**Cost of inaction**: {what happens if this risk is ignored}

## Structural observations

**Most depended-upon components** (highest fan-in):
| Component | Fan-in | Has alternative? |
|-----------|--------|-----------------|
| {name}    | {n}    | Yes/No          |

**Longest dependency chains**:
| Chain | Depth | Critical path? |
|-------|-------|---------------|
| {anchor} -> ... -> {leaf} | {n} | Yes/No |

## Risk heat map

{Qualitative summary: where does risk concentrate on the map? Is risk
clustered in infrastructure, in custom components, in external
dependencies? Does the evolution axis correlate with risk — are genesis
components riskier than commodities, or vice versa?}

## Recommendations

{Prioritised list of risk mitigation actions. Focus on the highest
likelihood + highest impact clusters first. Reference specific
components and suggest concrete structural changes.}
```

## Step 7: Render

```
bin/ensure-owm.sh clients/{org}/projects/{slug}/atlas/risk/map.owm
```

## Output

| File | Purpose |
|------|---------|
| `atlas/risk/map.owm` | Risk-annotated map |
| `atlas/risk/map.svg` | Rendered SVG |
| `atlas/risk/analysis.md` | Risk register and analysis |

Present the risk register summary table first, then the SVG, then offer
the detailed analysis. This is a derived view -- no client agreement
gate is needed.

After completion, regenerate the deliverable site:
```
bin/render-site.sh clients/{org}/projects/{slug}/
```
