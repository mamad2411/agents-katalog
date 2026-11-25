---
name: vstack-bottleneck
description: Diagnose why a multi-agent crew is slowing down, backing up under traffic, or hitting capacity limits. Combines deterministic Span-of-Control metrics with qualitative Org-Structure fit + Social Loafing + Superflocks routing analysis to localize whether the bottleneck is mathematical (graph topology) or behavioral (effort dilution).
---

# /vstack-bottleneck

When the crew works but doesn't scale, run this. It splits the bottleneck into the *deterministic* part (graph math: span, depth, centralization, decision-bottleneck index) and the *behavioral* part (who's loafing, who's hoarding traffic, what structural type doesn't fit the task).

## When to invoke

- "Throughput tanked when we added more load."
- "The orchestrator is the bottleneck."
- "Adding more agents made it worse."
- "We have 30 agents but only 3 do anything."
- Pre-scaling diagnostic before going from N to 2N agents.

If the crew works fine and the user just wants a general audit, use `/vstack-audit-crew` instead.

## Preflight

Two trace shapes are needed; if the user can produce both, the diagnosis is sharper.

**For Span-of-Control / Org-Structure:**
- Agent roster (`agents: [{agent_id, reports_to, decision_authority, ...}]`)
- Task description
- Incoming request rate (if known)
- Outcome of one bottleneck incident

**For Social Loafing / Superflocks:**
- Multi-agent task trace (who did what, in what order)
- Per-agent contribution metric if you have one (lines, tokens, completed sub-tasks)
- Routing decisions log (which agent got assigned each request)

If the user can only produce the first set, skip Social Loafing + Superflocks and use the deterministic + structural patterns only. The math is still informative.

## Workflow

### Step 1 — Deterministic metrics (Span-of-Control, always run first)

```
vstack_span_of_control with:
  crew_id: <crew name>
  task: <surfaced>
  agents: <agent nodes with reports_to + decision_authority>
  incoming_request_rate: <if known, else omit>
  outcome: <surfaced>
  success: <bool>
  mode: standard
```

This is the only pattern in the bundle that does deterministic math; the LLM is gated out of the metrics. Read out the six numbers:

- `max_span` — largest direct-report count
- `mean_span` — average
- `centralization_index` — 0-1, how concentrated authority is
- `hierarchy_depth` — levels in the graph
- `span_gini` — load inequality
- `decision_bottleneck_score` — composite

Compare to baselines via `vstack-config get baselines` if any exist; otherwise use the pattern's profile-pattern detector to assign a verbal category (`balanced_organic` / `centralized_bureaucracy` / `load_amplified_bottleneck` / etc).

### Step 2 — Org-Structure fit (qualitative)

```
vstack_org_structure with:
  <same trace shape>
  mode: standard
```

Org-Structure is the LLM-driven companion. It scores the six Galbraith-Mintzberg structural dimensions and produces a *fit-for-task-class* verdict. Where Span-of-Control answers "does the math work under load?", Org-Structure answers "is this the right structural type for this task class at all?"

Use both verdicts:

- Math broken + structure wrong-for-task → fundamental redesign, not a tuning fix
- Math broken + structure right-for-task → tune (load balance, decentralize, add layer)
- Math fine + structure wrong-for-task → restructure (split, merge, change reporting)
- Math fine + structure right-for-task → look at behavior (Step 3)

### Step 3 — Behavioral patterns (if traces support them)

If trace-quality supports it, run both:

```
vstack_social_loafing    # Latane-Williams-Harkins: agents contribute less when responsibility diffuses
vstack_superflocks       # Heffernan: a few agents hoard work while the rest starve
```

These two are mirror images: Social Loafing surfaces agents doing too *little*, Superflocks surfaces agents doing too *much*. A healthy crew sees neither; a stressed one usually sees both at once.

### Step 4 — Synthesize

```
## Bottleneck Diagnosis — <crew name>

**Quantitative snapshot** (Span-of-Control):
- max_span: X (sev: <s>)
- mean_span: X
- centralization_index: X (sev: <s>)
- decision_bottleneck_score: X (sev: <s>)
- profile_pattern: <name from analyzer>

**Structural fit** (Org-Structure Matrix):
- Six-dimension verdict: <one sentence>
- Right structure for this task class? <yes / no, with one-line reason>

**Behavioral signal** (if Step 3 ran):
- Social loafing: <severity + which agents>
- Superflocks: <severity + which agents>

**Root cause:** <one sentence connecting the quantitative + structural + behavioral findings>

**Two scale-up interventions:** (highest impact_estimate)
1. <intervention with target_locus + pattern source>
2. <intervention with target_locus + pattern source>

**One thing NOT to do:** <derived from the playbook anti-patterns; e.g. "do not just add more workers if Superflocks shows existing workers are starved">
```

Cap at ~450 words.

## Failure modes

- **Single agent.** Wrong skill — pivot to `/vstack-pick-pattern` with a Module 1 hint.
- **No `reports_to` in agent records.** Span-of-Control infers a flat structure. The metrics will be honest but uninformative. Ask the user to draw the actual reporting graph; even ASCII art is enough.
- **No `incoming_request_rate`.** Run anyway; Span-of-Control's load-amplification audit will be skipped but the structural metrics remain.
- **Span-of-Control + Org-Structure disagree.** This is informative, not an error. Surface both readouts and let the user decide; usually Org-Structure's verdict wins for "should we restructure" decisions, Span-of-Control's for "can we tune."

## Composition

- Upstream: `/vstack`, `/vstack-pick-pattern`, occasionally `/vstack-audit-crew`.
- Downstream: `/vstack-baseline` to track whether structural changes moved the metrics.
- Compose with: `/vstack-culture-check` if the structural problem is actually a culture problem in disguise (chain of command violated despite the diagram).

## What you don't do here

- Don't run the behavioral pair without trace substrate. Social Loafing + Superflocks need real contribution data.
- Don't recommend "add more agents" as a default fix. The whole point is that more agents made it worse.
- Don't run more than 4 patterns. Stop after Span + Org-Structure + 0/2 behavioral.
