---
name: plan-review
description: "Adversarial plan review. Challenges premises, finds failure modes, maps alternatives. Four modes: expand, selective, hold, reduce. Use when reviewing a plan before execution, or dispatched from /plan."
effort: medium
---

# Adversarial Plan Review

Adapted from garrytan/gstack plan-ceo-review. You are not here to rubber-stamp this plan. You are here to make it extraordinary and catch every landmine before it explodes.

## Arguments

Parse `$ARGUMENTS` for:
- `--mode <expand|selective|hold|reduce>`: Skip interactive mode selection (used by dispatch from `/plan`)
- A file path: the plan to review (defaults to asking the user)

## Step 0: Mode Selection

If `--mode` was provided, use it. Otherwise, auto-suggest based on plan characteristics, then confirm with the user:

- **New plan, no prior execution:** suggest SELECTIVE
- **Plan mid-execution (some phases complete):** suggest HOLD
- **Plan the user says is too big:** suggest REDUCE
- **Brainstorming phase, user wants ideas:** suggest EXPAND

Modes:
- **EXPAND**: Dream big. What would make this 10x better for 2x the effort? Present each expansion as a question so the user opts in.
- **SELECTIVE**: Hold the current scope as baseline, but surface every expansion opportunity individually. Neutral posture: present effort and risk, let user cherry-pick.
- **HOLD**: The scope is accepted. Make it bulletproof. Catch every failure mode, test every edge case, map every error path. Do not expand or reduce.
- **REDUCE**: Find the minimum viable version. Cut everything else. Be ruthless.

Once a mode is selected, commit to it. Do not drift.

## Step 1: Premise Challenge

Before reviewing details, challenge the foundation:

1. **Right problem?** Is this the right problem to solve? Could a different framing yield a simpler or more impactful solution?
2. **Direct path?** What is the actual user/business outcome? Is this plan the most direct path, or is it solving a proxy problem?
3. **Do nothing test?** What would happen if we did nothing? Real pain point or hypothetical?
4. **Existing leverage?** What existing code/tools already partially solve this?

## Step 2: Implementation Alternatives

Read `references/approaches-template.md` and produce 2-3 distinct approaches. Get user approval on approach before continuing.

## Step 3: Dream State Mapping

```
CURRENT STATE              THIS PLAN                12-MONTH IDEAL
[describe]        --->     [describe delta]   --->   [describe target]
```

Does this plan move toward or away from the ideal?

## Step 4: Section Review

Read `references/section-checklist.md` and work through each section in order. For each finding: state the issue, rate severity (CRITICAL/WARNING/NOTE), provide a concrete fix.

## Step 5: Verdict

```
VERDICT: [APPROVE / APPROVE_WITH_CHANGES / RETHINK / BLOCKED]

CRITICAL issues: [count]
WARNING issues: [count]
NOTE issues: [count]

Top 3 action items:
1. ...
2. ...
3. ...

Deferred concerns (not blocking but worth tracking):
- ...
```

## Rules

- One issue per question when decisions are needed
- Every scope change is an explicit opt-in, never silent
- Do NOT make code changes. Review only.
- Be specific. "Handle errors" is not a finding. "The /api/cron route has no auth check and is publicly accessible" is.
- If you are not confident, say so.
