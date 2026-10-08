---
name: prioritize-backlog
type: atomic
license: MIT
description: >
  Use when prioritizing a backlog, ranking features, or applying RICE,
  MoSCoW, value-vs-effort, or WSJF.
  Trigger words: prioritize, backlog, RICE, MoSCoW, value vs effort,
  ranking, WSJF.
metadata:
  version: 1.0.0
  user-invocable: "true"
---
# Prioritizing a Backlog

Rank work items by impact and urgency using a framework — not gut feeling.

## HARD-GATE
- Understand each item's impact and effort before scoring.
- Provide criteria for each dimension.
- Force relative ordering; avoid marking everything "high priority".
- Every ranking decision needs a stated reason.

## Core Process
1. Receive ticket/feature list.
2. Detect or choose framework (RICE, MoSCoW, value-vs-effort, WSJF).
3. Score each item using the framework's dimensions (see Inline Scoring Criteria).
4. Order by score; break ties by strategic alignment or dependencies.
5. Flag items needing clarification or with dependency constraints.
6. Output ordered backlog.

## Inline Scoring Criteria
### RICE
Reach × Impact × Confidence ÷ Effort (higher = higher priority).
Dimensions: Reach (#users/quarter), Impact (0.25–3), Confidence (50/80/100%), Effort (person-weeks).

### MoSCoW
- **Must**, **Should**, **Could**, **Won't**.

### Value-vs-Effort
2×2 matrix: Quick wins (high value/low effort) → do first.

### WSJF
(User value + Time criticality + Risk reduction) ÷ Job size (each 1–10).

## Output
- Framework used and why.
- Ordered table: Rank, Item, Score, Rationale.
- Framework breakdown (per-item dimensions) for scored frameworks.
- Flagged items and notes.

## Integration
- **plan-tickets**: prioritize tickets after drafting
- **plan-sprint**: use ordered backlog to select sprint candidates
- **estimate-tasks**: estimates feed effort-based frameworks
