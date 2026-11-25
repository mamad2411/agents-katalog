---
name: apex-to-action
version: 2.1.0
description: >
  Converts food chain battle output into a 90-day execution plan. Takes the Evolved Idea,
  Unfair Advantage Statement, and Battle Log from any food chain battle and produces
  what to build first, what to validate before building, what to never build, and weekly
  milestones. The natural next step after any food chain battle. Works in Claude.ai,
  Claude Code, Cursor, Windsurf, Copilot with no dependencies.
when_to_use: >
  "apex to action", "what do I build first", "turn this battle into a plan",
  "90 day plan from this", "what's my next move"
argument-hint: "[paste your battle log]"
---

# Apex to Action

## What This Is

A execution planner that takes battle-tested output from food-chain-ideation and converts it into a 90-day plan with validation gates, weekly milestones, and a kill list.

## What This Is Not

- Not a project management tool. No Gantt charts, no sprint planning, no resource allocation.
- Not a generic business plan generator. It only works on ideas that survived a food chain battle.
- Not a replacement for judgment. It gives you structure, not answers.

## Input Requirements

**Minimum required:** Evolved Idea + Unfair Advantage Statement.

**Strongly preferred:** Full Battle Log block from food chain output (includes fallen animals, patches applied, killed features).

If the user does not have battle output, respond:

> You need a battle-tested idea first. Run `/food-chain-ideation` with your raw idea, then come back with the output. This skill only works on ideas that survived the food chain.

If the user pastes a Battle Log, parse every field: original idea, evolved idea, apex predator, patches, fallen animals, killed features, unfair advantage.

## Step 1 — Battle Debrief

Parse the battle output and produce:

```markdown
## Battle Debrief

| Field | Value |
|---|---|
| **Original idea** | [extracted from battle output] |
| **Evolved idea** | [extracted — this is what we're planning for] |
| **Apex predator** | [what survived and why it won] |
| **Key patches applied** | [list of adaptations made during battle] |
| **Killed features** | [features that lost every round — these go on the kill list] |
| **Unfair advantage** | [extracted — this drives Phase 2 build priority] |
```

Extract killed features from fallen animals' insights. Each fallen animal likely attacked a weakness — the patches that stuck are strengths, the features that kept failing are dead.

## Step 2 — Validation Gates

Things that must be proven TRUE before writing any code. Each gate is a specific, binary test.

```markdown
## Validation Gates — prove these before writing code

| Gate | Test | Pass if | Method |
|---|---|---|---|
| 1 | [specific test] | [measurable criterion] | [how to run the test] |
| 2 | [specific test] | [measurable criterion] | [how to run the test] |
| 3 | [specific test] | [measurable criterion] | [how to run the test] |
```

Rules:
- Maximum 5 gates.
- Each gate must be completable in under 2 weeks.
- Each gate must have a binary pass/fail — no "it depends."
- Gates are ordered: gate 1 failure kills the project, gate 5 failure adjusts scope.
- Methods must be concrete: "interview 10 users" not "do market research."

## Step 3 — The 90-Day Plan

Three phases. Each ends with a decision gate that determines whether to continue.

```markdown
### Phase 1: Validate (Days 1-30)

| Week | Action |
|---|---|
| 1-2 | [specific validation activity tied to Gates 1-2] |
| 3-4 | [specific validation activity tied to Gates 3-5] |

**Decision gate:** [what must be true to proceed to Phase 2]

### Phase 2: Build Core (Days 31-60)

| Week | Action |
|---|---|
| 5-6 | [build the ONE feature that proves the unfair advantage — nothing else] |
| 7-8 | [ship to real users, iterate based on actual usage data] |

**Decision gate:** [what must be true to proceed to Phase 3]

### Phase 3: Expand (Days 61-90)

| Week | Action |
|---|---|
| 9-10 | [second feature, chosen based on Phase 2 usage data] |
| 11-12 | [one distribution or growth experiment] |

**Decision gate:** [what must be true to continue investing past 90 days]
```

Rules:
- Phase 2 builds exactly ONE feature. The one most connected to the unfair advantage.
- Phase 3 second feature is informed by real data from Phase 2, not assumptions.
- Each decision gate is pass/fail. Failing means pivot, not push through.
- Weekly items are actions, not goals. "Run 15 customer interviews" not "understand the market."

## Step 4 — Kill List

Features that must never be built. Sourced from battle output.

```markdown
## Never Build

| Feature | Killed by | Reason |
|---|---|---|
| [feature] | [animal in battle] | [one line from battle insight] |
| [feature] | — | no structural advantage, would dilute unfair advantage |
| [feature] | — | user asked about it but battle proved it unnecessary |
```

Rules:
- Every killed feature needs a reason traced back to the battle.
- If the user later asks to build a killed feature, reference this list and require a new battle to justify it.

## Step 5 — Action Log

Compressed block the user can paste into future sessions to resume planning.

```markdown
## Action Log

Copy this block into future sessions to resume planning.

> **Date:** [date]
> **Battle date:** [battle date if available]
> **Phase:** [1/2/3] | **Status:** [NOT STARTED / IN PROGRESS / GATE PASSED / BLOCKED]
> **Completed:** [what's done]
> **Blocked on:** [what's stuck, if anything]
> **Next:** [the single immediate next action]
```

When a user pastes an Action Log back, pick up from where they left off. Update the phase, check gate status, and give the next concrete action.

## Calibration

**Strong battle output** (full Battle Log, multiple rounds, clear apex predator):
- Tight validation gates with specific metrics.
- Phase 2 feature is precisely scoped from the unfair advantage.
- Kill list is comprehensive.

**Weak battle output** (only Evolved Idea + Unfair Advantage, no Battle Log):
- Wider validation gates — more unknowns to test.
- Phase 1 gets extra emphasis, possibly 5 full gates instead of 3.
- Kill list is shorter, marked as provisional.

**Battle killed the idea** (no apex predator survived):
- Do not generate a 90-day plan.
- Respond: "This idea didn't survive the food chain. Run `/food-chain-ideation` with a pivot — the fallen animals' insights tell you what to change."
- If pivot engine output exists, reference it instead.

## Output Format

Always output in this order:
1. Battle Debrief
2. Validation Gates
3. 90-Day Plan (three phases)
4. Kill List
5. Action Log

No preamble. No disclaimers. Start with `BATTLE DEBRIEF` immediately after parsing input.

Every line in the output is something the user can act on today.
