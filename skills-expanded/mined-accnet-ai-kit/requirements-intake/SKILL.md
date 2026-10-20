---
name: requirements-intake
description: Turn a raw request into a clear feature brief with problem, scope, acceptance criteria, and open questions. Use at the very start of a feature to produce .ai-work/requirements/brief.md — the canonical intent that feeds Gate G1.
version: 0.1.0
tier: core
stack: [any]
owner: researcher
gates: [G1]
related: [.ai/modules/planning/intent-analysis.md, .ai/templates/feature-brief.md]
---

# Skill: requirements-intake

## Purpose
Capture WHAT the user wants before anyone plans HOW — a precise, testable brief so planning (G1) starts from intent, not guesses. Output lands in `.ai-work/requirements/` (the only tier the Researcher/user writes).

## When to use
The first step of any new feature or non-trivial change, before `plan`/`tasks.md`. Skip only for trivial fixes per the Sizing Gate.

For a clearly specified, low-risk basic edit, the Planner may use the direct
single-task fast path instead. It is not available for any uncertainty or
for API/auth/input/data/migration/dependency/deployment/cross-cutting work;
when in doubt, perform this intake.

## Procedure
1. **Restate the problem** in one sentence — the user need, not a proposed solution.
2. **Scope**: what's in, and explicitly what's OUT (the out-of-scope list prevents creep).
3. **Acceptance criteria**: verifiable, user-observable outcomes ("given/when/then"). These become the backbone of `tasks.md` and the tests.
4. **Constraints & context**: known systems, data, non-functionals (perf, security, compliance); link source material into `.ai-work/requirements/context/`.
5. **Open questions**: list blockers first; do not invent answers — flag for the user.
6. **Write** `.ai-work/requirements/brief.md` from `.ai/templates/feature-brief.md`; research goes in `.ai-work/requirements/research/`.
7. **Hold for clarification**: when any material field remains unclear, ask
   the user the smallest useful question and update the draft only after the
   answer. Do not finalize a plan or create tasks in that turn.
8. **Confirm twice**: present the resolved plan and obtain explicit plan
   approval; then ask separately whether the user wants a task DAG created.
   These are two decisions, not one inferred intent.

## Checklist
- [ ] Problem stated as a need, not a solution
- [ ] In-scope and out-of-scope both explicit
- [ ] Acceptance criteria are verifiable (given/when/then)
- [ ] Constraints/non-functionals captured
- [ ] Open questions/blockers listed (not guessed)
- [ ] Written to `.ai-work/requirements/` (never `.ai-work/`)

## Anti-patterns
- Jumping to a solution/design instead of the problem
- Vague acceptance ("works well") that can't be tested
- Guessing answers to open questions instead of asking
- Putting requirements in `.ai-work/` (they must stay regenerable in `features/`)

## Output
`.ai-work/requirements/brief.md` (+ research/ + context/) — the canonical intent that Gate G1 planning builds on.
