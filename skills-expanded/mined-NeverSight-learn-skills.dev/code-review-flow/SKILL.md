---
name: code-review-flow
description: >-
  Goal-scoped three-axis review (Standards + Spec + Routes) of work produced
  under .agents/temp/goals/<goal-id>/ (plans, GOAL Done when, file lane). Looked
  up by /goal after validate-flow. Not for auto-invocation — use /code-review for
  branch/main diffs the user asked for.
disable-model-invocation: true
---

# Code Review Flow

Standards + Spec + Routes review **of what this `/goal` is shipping** — not an arbitrary “diff vs main” unless that is also the goal’s fixed point.

Full Standards + Routes doctrine (taste-flow, architecture examples, smells, thermonuclear bar, out-loud codepath walk) lives in **`/code-review`** — follow those sections, but **Spec and scope are goal-bound** below so this skill can be tweaked independently.

## Preconditions

1. Resolve **`goal-id`**
2. Prefer after `/validate-flow` pass
3. Workers via `/orchestrate-flow` — this goal-id only
4. Ticket/PR context via **read-only** `/trackers-flow` when the goal has a Ticket

## Process

### 1. Pin the fixed point

Ask if missing. Prefer the commit/branch that started this goal’s implement wave; otherwise `main` / user override.

```bash
git rev-parse <fixed-point>
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

### 2. Spec source (goal first)

1. `.agents/temp/goals/<goal-id>/GOAL.md` + `GRILL.md` + `plans/INDEX.md` + completed `plans/NN-*.md`
2. Ticket brief from `/trackers-flow` if Ticket
3. Only then broader PR/docs if the goal points at them

Tell Task subagents: **read this goal-id’s paths only** — never another workspace. Focus findings on the goal’s **file lane** and acceptance criteria, not drive-by refactors outside the plans.

### 3. Parallel axes

Same three-axis pattern as `/code-review`:

- **Standards** — paste `/taste-flow` non-negotiables + thermonuclear rules from `/code-review`; cite architecture/taste examples
- **Spec** — quote GOAL Done when + plan AC; missing/partial, scope creep, wrong implementations
- **Routes** — top-down out-loud walk of paths in the goal’s file lane; loose callers, dead ends, missing links; tag critical/important/nit (see `/code-review` Routes)

**Model:** omit Task `model` (see `/orchestrate-flow`) — inherit parent.

### 4. Aggregate + hand-off

Present `## Standards`, `## Spec`, and `## Routes` separately. Keep Routes path summaries readable. Failures → fix → re-`/validate-flow` if behavior changed → continue `/goal` ACHIEVED (no tracker writes).

### 5. Behavior-lock recommendations (tell the user — do not run)

Same as `/code-review` §10: if the goal’s file lane ships complex hooks / business logic / facades without a durable behavior lock, list them under `## Needs /create-test` and **tell the user** to run `/create-test`. Never invoke it from this flow (no twin; never autonomous).

## Anti-patterns

- Using this for a casual “review my branch vs main” with no goal — use `/code-review`
- Solo-reviewing a large goal diff when workers can
- Writing/closing tickets
- Approving “it works” when the `/code-review` thermonuclear bar fails
- Auto-running `/create-test` instead of recommending it to the user
