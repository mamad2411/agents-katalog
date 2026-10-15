---
name: project-pivot-planner
description: Plan mid-project direction changes when consistent negative results or novelty challenges require scope narrowing, angle change, or kill decisions. Use after multiple result-diagnosis cycles fail to recover the original claim. Distinct from research-idea-validator (project start) and result-diagnosis (per-experiment).
argument-hint: "[project-dir] [--mode narrow|angle|kill|reframe] [--trigger <trigger>]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Project Pivot Planner

Decide what to do when the original research direction is not working. This skill is for mid-project decisions — after enough evidence exists to rule out engineering bugs and still the core claim is not holding.

Use this skill when:

- multiple experiments consistently fail to support the core claim despite fixing engineering bugs
- an adversarial reviewer successfully argues that the main contribution is not novel
- the primary baseline unexpectedly closes the gap to the proposed method
- a related work publication makes the original contribution redundant
- advisor/committee feedback consistently questions the project's direction
- the project has been in result-diagnosis for more than 2–3 cycles without resolution

Do not use this skill for per-experiment debugging — use `experiment-debugger`. Do not use this skill when the issue is a specific surprising result — use `result-diagnosis`. Do not use this skill for new project validation — use `research-idea-validator`.

Pair this skill with:

- `research-idea-validator` when a pivot produces a substantially new research direction that needs fresh validation
- `result-diagnosis` to confirm the pattern of failures that triggers a pivot decision
- `research-project-memory` to record pivot decisions and update phase dashboard, claims, and actions
- `paper-positioning-planner` when a pivot changes the paper's primary contribution or archetype
- `experiment-design-planner` when the pivot requires a new experiment plan

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
```

## Core Principles

- A pivot decision requires evidence, not just frustration. Distinguish engineering failures from scientific failures.
- Narrow before killing: most failed ML projects have a defensible narrower claim.
- The cost of staying on a dead direction is often higher than the cost of pivoting.
- A pivot should be made once with full information, not incrementally under pressure.
- Document the pivot decision with the evidence that drove it — this protects the project in future advisor meetings and rebuttals.
- A kill decision is a valid research outcome when it is evidence-based and documented.

## Step 1 — Gather Evidence of Failure

Read:

- `memory/claim-board.md`: which claims are challenged, weakened, or unresolved
- `memory/risk-board.md`: open high-severity risks
- `memory/action-board.md`: repeated failed actions
- `memory/evidence-board.md`: evidence that contradicts or fails to support main claims
- recent experiment reports in `docs/reports/` or `code/docs/reports/`
- `result-diagnosis` outputs when available

Summarize:

- how many experiments have been run on the main claim
- what the strongest result is and how far it is from the claimed contribution
- whether the failure pattern is consistent (same direction) or noisy (sometimes works)
- whether advisor/reviewer feedback explicitly challenges the core direction

## Step 2 — Classify the Failure Pattern

Choose one primary pattern:

- `insufficient-gap`: method works, but the performance gap over baselines is too small to be a contribution
- `claim-not-supported`: the method does not actually do what the paper claims (mechanistically or empirically)
- `novelty-challenged`: the contribution exists but is not novel enough for the target venue
- `baseline-closed`: a baseline or related work published during the project closes the original gap
- `method-failure`: the method does not work reliably under realistic conditions
- `scope-too-broad`: the original scope is too ambitious but a subset would work

Record the evidence for this classification.

## Step 3 — Evaluate Pivot Options

For each of the following options, record whether it is viable given the current evidence:

### Option A: Narrow the Claim
Reduce the scope to a setting, dataset, regime, or sub-problem where the method reliably works.
- What is the narrowest defensible claim?
- Is the narrowed claim still publishable at the target venue?
- What additional experiments (if any) are needed to support the narrowed claim?

### Option B: Change the Angle
Reframe the contribution as a different kind of claim: change from performance to insight, from method to analysis, or from empirical to negative result.
- What story does the existing evidence support?
- Does the angle change require a new paper archetype?
- What is the cost in writing and repositioning?

### Option C: Pivot to a New Direction
Use existing infrastructure (code, data, baselines) for a related but different research question.
- What new question can the existing assets answer?
- Does the new direction need fresh idea validation?
- What is the timeline cost of switching?

### Option D: Kill the Project
Stop active development and document findings as a negative result or technical report.
- Is there a publishable negative result (methodologically sound null result with clear implications)?
- What assets can be reused in future work?
- What should be documented for the team or for future reference?

## Step 4 — Make the Pivot Decision

Recommend one option with a rationale. The recommendation should include:

- the chosen option (narrow / angle / new direction / kill)
- the evidence that drove this choice
- the new primary claim (or statement that no publishable claim is available)
- what stops (experiments, writing tasks, compute) after this decision
- what starts next (experiments, repositioning, new paper contract)
- a target venue reassessment if the archetype or scope changes

## Step 5 — Update Project Memory

After the pivot decision is made:

- Update `memory/claim-board.md`: mark old claims as `pivoted`, add new narrowed claims
- Update `memory/phase-dashboard.md`: update current phase and milestone
- Update `memory/decision-log.md`: record the pivot decision with evidence and rationale
- Update `memory/action-board.md`: close actions that are no longer relevant, add new actions
- Update `memory/risk-board.md`: resolve risks that are no longer active, add pivot-triggered risks
- Update `research-project-memory` if used: update the project direction and phase

Route to:
- `paper-positioning-planner`: if angle or archetype changes
- `experiment-design-planner`: if new experiments are needed for the narrowed claim
- `research-idea-validator`: if pivoting to a substantially new direction

## Final Sanity Check

Before finalizing:

- the failure pattern is documented with specific evidence, not just impressions
- all four pivot options were evaluated (not just the preferred one)
- the chosen option has a specific new primary claim or a kill decision
- memory updates cover claims, decisions, actions, and phase dashboard
- next steps are concrete and assigned
