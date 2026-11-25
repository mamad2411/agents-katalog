---
name: okr-drafting
description: Use this skill when the user asks to draft, structure, or revise objectives and key results. Trigger phrases include "draft OKRs", "write objectives and key results", "set goals for the quarter", "armar los OKRs", "OKRs for the team", "turn this into OKRs". Produces objectives as bets with measurable evidence, not a task list. Works in English and Rioplatense Spanish.
---

# okr-drafting

> **Anchor:** Objectives are outcomes; key results are evidence the outcome happened. Every objective is a bet.

## When to use

Use this skill when the user needs to draft or restructure a set of objectives and key results for a team, a function, or a quarter. Works for:

- A new quarter or cycle that needs aligned objectives before work starts.
- An existing draft that reads like a project list and needs to be reframed as outcomes.
- A single goal that needs a tight brief with a baseline, a target, and kill criteria.

Do not use when:

- The user is sequencing the work that moves toward a goal. Use `roadmap-from-data` instead, which sequences work toward goals.
- The user is proposing a single bet pre-scoping. Use `feature-proposal`, which handles a single bet.

## Philosophy

OKRs are a portfolio of bets written down. Each objective names an outcome the team is betting it can cause, and each key result is the evidence that the outcome happened. Treating OKRs as a list of deliverables is a category error that turns a goal-setting practice into a status report.

Two concepts from the handbook apply directly. **Output vs outcomes:** an objective states what should change in user behavior or system state, never what the team will produce. A shipped feature is output; the behavior change it causes is the outcome. **Product as a portfolio of bets:** the set of objectives is a portfolio. Each one carries a size and a confidence level, and the team holds committed bets separately from aspirational ones so a missed stretch does not read as a failure.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: OKR, KPI, baseline, target, backlog, sprint, stakeholder, rollout, feature flag, AB test. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the OKRs, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Write each objective as an outcome statement, not a project

An objective names a state of the world the team wants to be true at the end of the cycle. "Ship the new onboarding flow" is a project. "New users reach first value without help" is an outcome. If the objective names a thing the team will build, rewrite it as the change that thing is supposed to cause.

### Step 2. Make each key result a measurable change with a baseline and a target

A key result has three parts: the metric, where it stands today (the baseline), and where it should stand at the end (the target). "Improve activation" is not a key result. "Activation rate from 24 percent to 40 percent" is. If there is no baseline, name that gap and propose how to measure it before the cycle starts.

### Step 3. Name the bet and its size

Each objective is a bet. State what the team is betting it can cause and how big the bet is: small (high confidence, incremental), medium (real uncertainty), or large (a stretch the team is not sure it can reach). The size tells the reader how to weigh a miss.

### Step 4. Write kill or rethink criteria per objective

For each objective, write what signal would cause the team to stop or rethink it mid-cycle. An objective with no kill criteria is a one-way door. State the signal and how long the team waits before checking.

### Step 5. Hold at most three objectives

More than three objectives means the team has not chosen. Force the cut. If a fourth feels essential, it is either a key result of an existing objective or evidence that the team is trying to do two quarters at once.

### Step 6. Separate committed from aspirational

Mark each objective committed or aspirational. Committed objectives are bets the team expects to land and will be held to. Aspirational objectives are stretches where partial progress is the point. Mixing them lets a missed stretch read as a failure and a sandbagged commitment read as a win.

### Step 7. Reject key results that are task lists

If a key result reads like a to-do item ("launch X", "complete Y", "deliver Z"), it is measuring output, not outcome. Rewrite it as the change the task is supposed to cause, or move it to a delivery plan and replace it with the metric that proves the task worked.

## Templates

- `templates/en/okr-set.md`: a full set of objectives and key results for a cycle.
- `templates/en/goal-brief.md`: a one-objective brief with baseline, target, and kill criteria.
- `templates/es/okr-set.md`: un set completo de objetivos y key results para un ciclo.
- `templates/es/goal-brief.md`: un brief de un solo objetivo con baseline, target y criterios de corte.

## Related skills

- `roadmap-from-data`: use it to sequence the work that moves toward these objectives, not to set the objectives themselves.
- `feature-proposal`: use it when the work is a single bet pre-scoping rather than a portfolio of objectives.
- `prd-authoring`: use it to spec a feature once an objective points at a specific build.
- `exec-brief`: use it to summarize a set of OKRs and their progress for a leadership audience.

## Anti-patterns

This skill must never produce:

- An objective that names a project or a deliverable instead of an outcome.
- A key result with no baseline and no target.
- A key result that is a task list item dressed as a metric.
- A set with more than three objectives.
- A set that mixes committed and aspirational bets without labeling which is which.
- An objective with no kill or rethink criteria.
- An objective whose key results, if all hit, would not prove the objective happened.
- A set that uses "the team" or "users" as the only subject, with no specific audience.
- OKRs that mix English and Spanish inconsistently within a single objective.
- A set that cites "industry best practice" without a concrete internal reason.

## Checklist before delivery

- [ ] Every objective is an outcome statement, not a project.
- [ ] Every key result names a metric, a baseline, and a target.
- [ ] Each objective names the bet and its size.
- [ ] Each objective has kill or rethink criteria that are concrete and time-bounded.
- [ ] The set has at most three objectives.
- [ ] Committed and aspirational objectives are labeled.
- [ ] No key result is a task list item.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] The set reads cleanly to a stranger who was not in prior planning.
