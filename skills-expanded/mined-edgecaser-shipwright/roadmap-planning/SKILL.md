---
name: roadmap-planning
description: "Creates outcome-based product roadmaps using the Now/Next/Later framework with prioritization via RICE scoring. Helps PMs communicate what the team is working on, why, and what comes next, without falling into the trap of date-driven feature lists."
category: strategy
default_depth: standard
---

# Roadmap Planning

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Creates outcome-based product roadmaps using the Now/Next/Later framework with prioritization via RICE scoring. Helps PMs communicate what the team is working on, why, and what comes next, without falling into the trap of date-driven feature lists.

## When to Use

- Quarterly planning and roadmap updates
- Communicating product direction to stakeholders and leadership
- Aligning engineering, design, and business teams on priorities
- Transitioning from output-based ("ship feature X") to outcome-based roadmaps

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick stakeholder update or status share | Define Outcomes, Apply Now/Next/Later (overview only) |
| **Standard** | Quarterly planning or cross-functional alignment | All sections |
| **Deep** | Annual planning, multi-team coordination, or board-level roadmap | All sections + initiative-level risk assessment, capacity modeling per team, scenario variants (optimistic/pessimistic staffing) |

**Omit rules:** At Light depth, skip Prioritize with RICE, Dependency Mapping, and the Not Doing section. Produce only the Now/Next/Later overview with outcomes and metrics.

## Framework

### Step 1: Define Outcomes, Not Outputs

Each roadmap item should be an outcome or initiative, not a feature:

| Avoid (Output) | Prefer (Outcome) |
|---|---|
| "Build Gantt chart view" | "Help PMs communicate timelines to stakeholders" |
| "Add Slack integration" | "Reduce context-switching during triage" |
| "Redesign onboarding" | "Increase Day-7 retention from 35% to 50%" |

### Step 2: Prioritize with RICE

Score each initiative:

```markdown
| Initiative | Reach | Impact | Confidence | Effort | RICE Score |
|---|---|---|---|---|---|
| [Initiative 1] | [users/quarter] | [0.25/0.5/1/2/3] | [%] | [person-weeks] | [calculated] |
```

**Scoring guide:**
- **Reach:** How many users/customers will this affect per quarter?
- **Impact:** Minimal (0.25), Low (0.5), Medium (1), High (2), Massive (3)
- **Confidence:** How sure are you? (100% = high evidence, 50% = gut feel)
- **Effort:** Person-weeks of work (all disciplines)

**RICE = (Reach × Impact × Confidence) / Effort**

### Step 3: Apply Now / Next / Later

```markdown
## Now (Current Quarter, Committed)
High confidence. Actively being worked on. Clear success metrics.

### [Initiative 1]
- **Outcome:** [What success looks like]
- **Metric:** [How we measure it]
- **RICE:** [Score]
- **Status:** [In progress / Starting soon]
- **Dependencies:** [Cross-team deps, if any]

### [Initiative 2]
...

## Next (Next Quarter, Planned)
Medium confidence. Scoped but not started. May shift based on learnings from "Now."

### [Initiative 3]
- **Outcome:** [What success looks like]
- **Metric:** [How we measure it]
- **RICE:** [Score]
- **Open questions:** [What we still need to validate]

## Later (Future, Exploring)
Low confidence. Directionally interesting but not yet committed. Treated as hypotheses.

### [Initiative 5]
- **Hypothesis:** [Why we think this matters]
- **Trigger to promote:** [What would move this to "Next"]
- **RICE:** [Rough estimate]
```

### Step 4: Add Context for Stakeholders

```markdown
## Roadmap Context

### Strategic Bets This Serves
- Bet 1: [link to strategy]
- Bet 2: [link to strategy]

### What We're NOT Doing (and Why)
- [Requested item], Reason: [why it's not on the roadmap]
- [Requested item], Reason: [why it's deferred]

### How to Read This Roadmap
- "Now" = committed, high confidence
- "Next" = planned, may shift
- "Later" = directional, not a promise
- This is NOT a date-driven Gantt chart
```

### Step 5: Dependency Mapping

```markdown
## Dependencies
| Initiative | Depends On | Team/System | Risk Level | Mitigation |
|---|---|---|---|---|
| [Initiative 1] | [API v3 release] | Platform team | High | [Parallel workstream] |
| [Initiative 2] | [Design system update] | Design | Low | [Can use current system] |
```

## Minimum Evidence Bar

**Required inputs:** A list of candidate initiatives with enough context to articulate outcomes (not just feature names), and a rough sense of team capacity.

**Acceptable evidence:** Customer research, usage analytics, strategic bets from a strategy session, engineering sizing estimates, stakeholder requests with business rationale.

**Insufficient evidence:** If initiatives are described only as feature names with no outcome or metric, produce a partial artifact with outcome-less items marked `[TBD, requires: measurable outcome and success metric]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Now-quarter items (committed work with known metrics and dependencies)
- **Hypotheses:** Later-horizon items and RICE scores built on unvalidated assumptions, must be labeled with confidence level and promotion trigger

## Output Format

Produce a Roadmap Document with:
1. **Roadmap Summary**, visual Now/Next/Later overview
2. **Prioritization Table**, RICE scores for all initiatives
3. **Initiative Details**, outcome, metric, status, dependencies for each
4. **Strategic Alignment**, which bets each initiative supports
5. **Not Doing**, conscious exclusions with rationale
6. **Dependencies**, cross-team dependencies and risks

**Shipwright Signature (required closing):**
7. **Decision Frame**, Recommended Now-quarter commitment with trade-off (scope vs. confidence), confidence with evidence quality, owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, Initiatives with unvalidated RICE inputs, unresolved dependencies, missing engineering estimates
9. **Pass/Fail Readiness**, PASS if every Now item has an outcome, metric, and owner, and at least one Later item has a promotion trigger; at Light depth, PASS if Now/Next/Later overview is present with outcomes and metrics for each item, RICE scoring, dependencies, and Not Doing section are not required; FAIL if Now items lack metrics or the roadmap is a feature list with no outcomes
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Date commitments for "Later" items**, Now can have dates; Later should not
- **Feature lists disguised as roadmaps**, Every item needs an outcome and metric
- **No "Not Doing" section**, Stakeholders need to know what was considered and declined
- **Stale roadmaps**, Update at least quarterly; a 6-month-old roadmap is fiction
- **Prioritization without evidence**, RICE with 20% confidence is still better than HiPPO

## Weak vs. Strong Output

**Weak:**
> "Now: Build Slack integration. Next: Build email integration. Later: Build Teams integration."

A feature list with time labels, no outcomes, no metrics, no rationale for sequencing.

**Strong:**
> "Now: Reduce context-switching during triage (metric: avg switches/session from 4.2 to <2, RICE: 1,840). Next: Expand async collaboration for distributed teams (metric: % decisions made outside meetings from 15% to 40%). Later: Unified notification layer, hypothesis: consolidating alerts will reduce missed actions; promote to Next if Q3 survey confirms notification fatigue >50%."

Each item states an outcome, a measurable target, and Later items include promotion criteria.
