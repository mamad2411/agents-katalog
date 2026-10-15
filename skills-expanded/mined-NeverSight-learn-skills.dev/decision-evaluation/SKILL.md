---
name: decision-evaluation
description: Evaluate options for a specific design decision node and recommend one with explicit trade-offs. Use when the design already exposes a concrete choice such as architecture style, state management approach, auth model, storage pattern, sync strategy, or multi-agent coordination model. Trigger when the user needs structured comparison and recommendation for a bounded design decision. Do not use for broad design discovery, full-system decomposition, or final readiness review.
---

# Decision Evaluation

## Overview

This skill evaluates one explicit design decision at a time.

It does not discover the whole design. It does not validate overall readiness. Its job is to compare real options for a bounded decision node and produce a recommendation with reasons.

## When to Use

Use this skill when:

- the design already contains a concrete decision node
- the user is effectively asking "which of these approaches should we choose?"
- the decision will materially affect architecture, implementation path, compatibility, cost, or operational risk

Typical examples include:

- auth model
- coordination pattern
- storage strategy
- sync model
- state management approach
- retry or execution model

Do not use this skill when:

- the design tree is not formed yet
- the task is still broad design discovery
- the main need is deeper refinement rather than bounded comparison
- the task is a final readiness gate

## Core Responsibilities

Your responsibilities are:

1. Frame the exact decision question.
2. Present 3 to 4 real options when real options exist.
3. Compare trade-offs clearly and concretely.
4. Recommend one option or a justified combination when appropriate.
5. Explain why the rejected options are not preferred in this context.
6. Record the result in a reusable decision record.

## Comparison Standard

Compare options using the dimensions that matter to the decision. These often include:

- implementation complexity
- compatibility with the current system
- operational risk
- performance
- maintainability
- future flexibility
- debugging and observability implications

Do not force every dimension into every decision. Use only the ones that actually matter.

## Expected Outputs

Produce or update a `design_state` that includes:

- `decision_nodes`
- `decisions`
- `risks`
- optional downstream impact notes for the design tree

## Diagram Conventions

Use character diagrams inside code blocks (no language tag) to visualize trade-offs and architecture topology.

### Star Ratings

Use when comparing 3+ options across 2+ quantitative dimensions.

```
Overall Rating:

Auth0:      ★★★★☆  4/5
Keycloak:   ★★★☆☆  3/5
Self-build: ★☆☆☆☆  1/5

Dimension Breakdown:

Security:       Auth0 ★★★★★  Keycloak ★★★★☆  Self ★★☆☆☆
Speed-to-MVP:   Auth0 ★★★★★  Keycloak ★★★☆☆  Self ★☆☆☆☆
Cost-at-scale:  Auth0 ★★★☆☆  Keycloak ★★★★☆  Self ★★★★★
```

**Rules:**

- `★` (filled, U+2605) + `☆` (empty, U+2606), 5-star scale (max = ★★★★★)
- Format: `label ★★★★☆  4/5`
- Always show all 5 stars (e.g. `★★☆☆☆`, never `★★`)
- Overall rating section first, then Dimension Breakdown
- Breakdown section: one dimension per row, all options on the same row
- Always state the scale explicitly

### Architecture Topology

Use when the decision changes component layout or system topology.

```
┌──────────────────┐
│  Load Balancer   │
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
 [API x2] [API x2]
    │         │
    └────┬────┘
         ▼
  ┌────────────┐
  │  Postgres  │
  └────────────┘
```

- Boxes use `┌ ┐ └ ┘ ─ │` for infrastructure components
- `[brackets]` for application components
- Vertical flow primary; `──→` for horizontal connections

### When to Add Diagrams

- Star ratings: 3+ options × 2+ quantitative dimensions
- Topology: the decision changes the physical or logical component layout
- Do NOT add diagrams for simple yes/no or qualitative comparisons — use markdown tables
- Max width: 78 characters

## Entry and Exit Criteria

Enter when:

- the decision node is explicit and bounded
- the decision has at least two meaningful alternatives

Exit when:

- there is a clear recommended option
- the consequences of that decision are clear enough to feed back into the design

## Handoff Rules

- Hand back to `design-refinement` when the chosen option affects unresolved design branches.
- Hand to `design-readiness-check` when this was the last major unresolved design issue.
- Hand back to `design-orchestrator` if routing should be reconsidered after the decision lands.
- Do not take over general design clarification work.
