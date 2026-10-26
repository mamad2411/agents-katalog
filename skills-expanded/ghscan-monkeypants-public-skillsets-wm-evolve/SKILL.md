---
name: wm-evolve
description: >
  Position supply chain components on the evolution axis to create a
  Wardley Map in OWM format. Assesses each component's evolutionary
  stage using Wardley's characteristics (ubiquity, certainty, market).
  Produces the first real OWM map with both visibility and evolution axes
  grounded in evidence. Use after supply chain is agreed
  (supply-chain.agreed.md exists).
compatibility: Requires Node.js (npx) for OWM rendering via cli-owm
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "4"
  freedom: medium
---

# Evolution Positioning for Wardley Maps

You are conducting the **evolution assessment phase** of a Wardley mapping
engagement. This is where the map becomes a Wardley map — you are adding
the horizontal axis (evolution/maturity) to the vertical axis (visibility)
established in the supply chain stage.

## Prerequisites

Check that the project directory contains:
- `chain/supply-chain.agreed.md`
- `needs/needs.agreed.md`
- `brief.agreed.md`

Check that the client workspace contains:
- `resources/index.md` and research sub-reports in `resources/`

If `supply-chain.agreed.md` is missing, tell the user to complete
`wm-chain` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Understanding evolution

Read [evolution-characteristics.md](references/evolution-characteristics.md)
for the full assessment framework. The key question for each component:
**where is this in its evolutionary journey from novel to commodity?**

| Stage | Maturity range | Key signal |
|-------|---------------|------------|
| Genesis | 0.00 - 0.17 | Novel, few know about it, no market |
| Custom | 0.17 - 0.40 | Bespoke, emerging awareness, competitive advantage |
| Product | 0.40 - 0.70 | Off-the-shelf, multiple vendors, best practice |
| Commodity | 0.70 - 1.00 | Utility, ubiquitous, cost of doing business |

## Step 1: Cluster components

Group the components from `chain/supply-chain.agreed.md` into logical
clusters for assessment. Clusters might be:
- Components in the same domain (e.g. "fleet management cluster")
- Components at similar depths in the value chain
- Components from the same technology area

This grouping is for your working convenience — the final map does not
show clusters.

## Step 2: Assess evolution per cluster

For each cluster, write an assessment to
`evolve/assessments/{cluster-slug}.md`:

```markdown
# Evolution Assessment: {Cluster Name}

| Component | Stage | Maturity | Evidence |
|-----------|-------|----------|----------|
| {name} | {Genesis/Custom/Product/Commodity} | {0.00-1.00} | {brief evidence} |

## Inertia

- {Component}: {inertia signal and source}

## Reasoning

{Narrative explaining the assessments, particularly any that are
debatable or surprising. Reference research sub-reports.}
```

For each component, apply the assessment questions from
[evolution-characteristics.md](references/evolution-characteristics.md):

1. **Ubiquity**: How many people/organisations use this?
2. **Certainty**: How well understood is it?
3. **Market**: Can you buy it off the shelf? Multiple vendors?
4. **Differentiator**: Is it a source of competitive advantage?
5. **Publication**: Are there standards, best practices, textbooks?

You may use **web search** to verify evolution claims — for example,
searching for how many commercial products exist in a category, or
whether industry standards have been published.

Mark **inertia** where you identify resistance to change (existing
investment, skills lock-in, contractual obligations, cultural attachment).

## Step 3: Generate OWM map

Read [owm-dsl-reference.md](references/owm-dsl-reference.md) for the
full OWM syntax.

Generate `evolve/map.owm` by combining:
- **Anchors** from `needs/needs.agreed.md` (user classes -> anchors at
  visibility 0.90-0.97)
- **Components** from `chain/supply-chain.agreed.md` with:
  - Visibility (Y) derived from depth in the dependency tree
  - Maturity (X) from your evolution assessments
- **Dependencies** from the supply chain
- **Inertia** markers where identified

### Visibility mapping

Convert dependency tree depth to visibility coordinates:
- Depth 0 (anchors/users): 0.90 - 0.97
- Depth 1 (user needs): 0.80 - 0.90
- Depth 2 (capabilities): 0.65 - 0.80
- Depth 3 (sub-capabilities): 0.45 - 0.65
- Depth 4+ (infrastructure): 0.10 - 0.45

Spread components at the same depth across the visibility range to
avoid overlap. Use `label` offsets where component names would collide.

### Map structure

```owm
title {Organisation} — {Scope}

// Anchors
anchor {User Class 1} [{vis}, {mat}]
anchor {User Class 2} [{vis}, {mat}]

// User needs
component {Need 1} [{vis}, {mat}]
component {Need 2} [{vis}, {mat}]

// Capabilities
component {Capability} [{vis}, {mat}]
component {Capability} [{vis}, {mat}] inertia

// Infrastructure
component {Infra} [{vis}, {mat}]

// Dependencies
{User Class 1}->{Need 1}
{Need 1}->{Capability}
{Capability}->{Infra}

style wardley
```

## Rendering

After writing any `.owm` file, render it to SVG:
```
bin/ensure-owm.sh clients/{org}/projects/{slug}/evolve/map.owm
```

This checks for `cli-owm` and installs it if missing, then produces
`evolve/map.svg`. Show the SVG to the client alongside the OWM source.

## Step 4: Present to client

Present:
1. The evolution assessments (summarised) — for each component, its
   proposed stage and key evidence
2. The generated OWM map and its rendered SVG

Ask:
1. "Do these evolution positions feel right? Which components would
   you move left (less mature) or right (more mature)?"
2. "Have I identified inertia correctly? Where else do you feel
   resistance to change?"
3. "Does the overall shape of the map match your intuition about
   your organisation?"

Evolution positioning is **heavily judgement-based**. The client has
internal knowledge the research cannot capture. Expect significant
iteration.

## Step 5: Iterate and agree

Based on client feedback:
1. Update assessments in `evolve/assessments/`
2. Regenerate `evolve/map.owm`
3. Present again until the client is satisfied

When the client agrees:
1. Copy to `evolve/map.agreed.owm`
2. Record the agreement:
   ```
   wm-evolve/scripts/record-agreement.sh --client {org} --project {slug} \
     --field "Components={count} components mapped" \
     --field "Key inertia points={list}" \
     --field "Caveats={any components with uncertain positioning}"
   ```

## Common pitfalls

- **Don't confuse internal maturity with market maturity.** The
  organisation may have a mature internal system for something the
  broader market considers custom-built.
- **Don't anchor on the organisation's perspective alone.** A company
  building something in-house doesn't mean it's Genesis — it might be
  a Product they chose to custom-build.
- **Spread components.** If everything clusters in one area of the map,
  you're probably wrong about some positions. Real maps show components
  spread across the evolution axis.
- **Label offsets matter.** Use `label [-100, 4]` or similar to prevent
  text overlap. The map must be readable.

## Completion

When `map.agreed.owm` is written, tell the user the next step is
`wm-strategy` to add strategic annotations (evolution arrows,
build/buy/outsource decisions, pipelines, and insights).
