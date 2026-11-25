---
name: key-moments
description: Rank a topic's user-flow branches by proof priority (value × risk × frequency) right after user-flow-map, ordering the branches, gating variation breadth, and promoting or pruning flows so state-model and ux-variations grow the tree in proof order — writes only existing flow-tree ordering fields, no schema change.
type: execution
version: v0.0
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "[optional: topic]"
context_intake: scoped
visual_tier: prototype
---

# Key Moments

Invoke as `$key-moments`.

Rank a topic's user-flow branches by **proof priority** so the rest of the design tree grows in the order that most needs proof. This is a **trunk** skill: it runs **after `$user-flow-map`** and **before `$state-model` and `$ux-variations`**, needs only the flow map, and writes **existing** flow-tree ordering fields — it adds no new artifact and no schema field.

The point is sequencing. Not every flow deserves equal modelling and variation budget. `key-moments` decides which flows are the moments worth proving first (high value, high risk, high frequency), orders the branches accordingly, gates how much variation breadth each flow earns, and **promotes or prunes** flows. `state-model` then attaches just-in-time only to **promoted** flows, and `ux-variations` spends its budget on the moments that matter.

Follow `DESIGN-TREE-LOOP.md` for design-tree routing, state storage, branch decisions, approval boundaries, and task classification. Branch ordering state belongs in `design/**/flow-tree-*.yaml`, not `tasks/todo.md`.

`key-moments` runs only from the `user-flow-map` handoff; see `DESIGN-TREE-LOOP.md` for route-position rules.

## Gate

Before ranking, verify the flow map exists:

- Read `design/**/flow-tree-*.yaml` and the user-flow doc (`design/user-flow-[topic].md` or product-path-scoped equivalent). At least one `branches[]` user-flow branch must exist.
- If no flow map exists, stop and route to `$user-flow-map [topic]` first.
- Do not read or require UX variations, models, UI packets, or prototypes — they do not exist yet and are not inputs.

## Process

1. **Resolve scope.** Identify the product path and topic. Read every user-flow branch from the flow-tree manifest and the flow doc.
2. **Score each flow by proof priority.** For each user-flow branch, assess three factors and combine them into a proof-priority score:
   - **Value** — how much user/business value the flow delivers (first-value moments rank high).
   - **Risk** — how uncertain or contentious the flow is; how likely the current design assumption is wrong.
   - **Frequency** — how often the flow runs in real use.
   Proof priority is roughly **value × risk × frequency**: a high-value, high-risk, frequent flow is the first moment to prove.
3. **Order the branches.** Set `journey_sequence` on each user-flow branch to its proof order (and `evaluation_priority` on child variations where ordering is already known). When the proof order diverges from raw journey progression, record the explicit override in `branch_order_override` (`ordered_branch_ids`, `override_rationale`, `recorded_at`).
4. **Gate variation breadth.** For each flow, note how much variation budget it earns — top-priority moments justify the full breadth `ux-variations` can grow; low-priority flows get a single conservative variation or none.
5. **Promote or prune.** Mark which flows are **promoted** (proceed to `state-model`/`ux-variations`) and which are **parked/pruned** (set the branch `status: parked` with a rationale). Pruned flows are not modelled.
6. **Record rationale.** Write `priority_rationale` on each branch explaining its proof order, variation budget, and promote/prune decision.
7. **Build the alignment page.** Render the proof-priority ranking, the value/risk/frequency factors, the ordering, the variation-breadth gates, and the promote/prune decisions for review.

## Output

The skill updates existing flow-tree fields only:

```text
design/**/flow-tree-*.yaml   # journey_sequence, evaluation_priority, branch_order_override, priority_rationale, status
alignment/key-moments-{topic}.html
```

No new artifact and no schema change.

## Next Work

After the ranking is approved, route to the promoted flows in proof order:

- `$state-model [topic]` to attach the domain model just-in-time to the highest-priority promoted flow.
- `$ux-variations [specific-user-flow]` when a promoted flow already has a confirmed `model_ref` and is ready to grow variations within its gated breadth.

**Recommended next command:** `$state-model [topic]`.

## Constraints

- Read only the flow map; do not require models, UX variations, UI packets, or prototypes.
- Write only existing flow-tree ordering fields (`journey_sequence`, `evaluation_priority`, `branch_order_override`, `priority_rationale`, branch `status`). Do not invent schema fields.
- Do not occupy a route position; this is a trunk skill invoked from `user-flow-map`'s handoff.
- Do not build screens, models, or prototypes; this skill only ranks and orders.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell before the target skill.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/key-moments-{topic}.html`.

The page must show the proof-priority ranking, the value/risk/frequency factors per flow, the resulting branch order, the per-flow variation-breadth gate, and the promote/prune decisions, as review gates before the ordering is written to the flow-tree manifest.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
