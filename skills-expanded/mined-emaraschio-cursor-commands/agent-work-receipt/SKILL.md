---
name: agent-work-receipt
description: >-
  Produces a conservative agent work receipt after completed work: finished
  output, time estimates, review burden, risks, and value judgment. Use when
  the user invokes /agent-work-receipt, asks for a work receipt, or wants to
  measure agent productivity honestly after a session.
disable-model-invocation: true
user-invocable: false
---
# Agent work receipt

## Role

You produce a **conservative agent work receipt** for work already completed in the current session. You account for what actually landed, not what was discussed, drafted, or abandoned. You **do not** start new implementation, commits, or destructive commands in the same turn.

## When to use

Use when the user invokes `/agent-work-receipt`, asks for a work receipt, or wants honest accountability for agent-assisted work after a session. For planning *before* autonomous work, use `define-agent-goal`. For code quality on diffs, use `light-review-existing-diffs`.

## Conservative charter

> Be conservative. Do not count drafts, ideas, or unused output as completed work.

## Workflow

Run phases in order. Do not publish the receipt until evidence is gathered.

### Phase 0: Intake

1. Parse a **scope hint** from the user message (e.g. "receipt for the refactor in service-a").
2. If no scope hint, default to the **full session**.
3. If the user invokes mid-task with no finished work yet, scope to **partial work only** or ask whether to wait. Do not hallucinate completion.

### Phase 1: Evidence

Gather read-only evidence:

- **Conversation**: what the user asked for, what the agent actually did, what was rejected or abandoned
- **Git** (when a repo is present): `git status`, `git diff`, `git log` to ground landed artifacts
- **Files**: only artifacts explicitly created, edited, committed, or merged in scope

Do not treat uncommitted explorations, reverted edits, or failed tool runs as finished output.

### Phase 2: Inventory

List **only landed artifacts** in scope:

- Files written or modified that remain in the tree
- Commits, branches, or PRs created
- Docs, plans, or configs delivered to the user

Explicitly note what you **exclude**: brainstorms, unused drafts, abandoned paths, tool errors, reverted work.

### Phase 3: Estimates

Provide **human baseline** and **agent-assisted time** as ranges or point estimates. Label both clearly as **estimates**, not measured facts. The user may correct in follow-up.

Base estimates on task complexity and evidence, not enthusiasm.

### Phase 4: Review & risk

**Review required**: concrete items the human must still check, rewrite, or fix (tests not run, edge cases, copy, security, manual verification).

**Risk**: what could be wrong, incomplete, or misleading in the finished output.

### Phase 5: Value

Pick exactly one tier with brief evidence-backed rationale:

- **Small assist**: agent helped but human effort dominated or output is narrow
- **Major time saver**: clear, verifiable reduction in manual effort for substantive deliverables
- **Not worth the agent**: little or no landed output; review cost exceeds benefit; session was mostly exploration

Do not agree to inflated praise (e.g. "say this saved 10 hours") without evidence.

### Phase 6: Deliver

Post the receipt using the template below. Keep each section concrete and scoped.

## Receipt template

```markdown
# Agent work receipt

## 1. Finished output
What was actually completed (artifacts only).

## 2. Human baseline (estimate)
How long this would likely take manually.

## 3. Agent-assisted time (estimate)
How long this took with the agent.

## 4. Review required
What the human still needs to check, rewrite, or fix.

## 5. Risk
What could be wrong, incomplete, or misleading.

## 6. Final value estimate
Small assist / major time saver / not worth the agent, with brief rationale.
```

Populate every section. Prefer bullets and short paragraphs over vague prose.

## Safety

- Retrospective only: no new implementation, commits, or destructive commands unless the user explicitly requests follow-up work in a new turn.
- No secrets, tokens, PII, or PHI in the receipt body.
- Time fields are **estimates**. Never present them as measured elapsed time.

## Distinction from other commands

- **`define-agent-goal`**: forward planning before autonomous work. This skill is **backward** accountability after work.
- **`decision-audit`**: post-build judgment autopsy (decision ledger, confidence, pride gate). This skill measures output, time, review burden, and value, not choice quality.
- **`light-review-existing-diffs`**: code quality pass on diffs. This skill measures output, time, review burden, and value, not style or bugs alone.
- **`generate-pr-description`**: writes a PR artifact. This skill produces an honest session receipt, not marketing copy.

## Guardrails

- Stay conservative: count only landed artifacts as finished output, never drafts, ideas, or abandoned work.
- Stay retrospective: start no new implementation, commits, or destructive commands in the same turn.
- Label time fields as estimates, never as measured elapsed fact, and never inflate value without evidence.
