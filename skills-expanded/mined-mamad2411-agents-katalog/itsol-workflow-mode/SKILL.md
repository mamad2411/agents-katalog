---
name: itsol-workflow-mode
description: "Resolve governed/direct/autonomous-planned authority for plans, code changes, delegation, or mode changes."
---

# ITSOL Workflow Mode

Canonical authority contract for planning, implementation, bugfix, delegation, and mode transitions. Bounded administration—repository inspection, `.itsol.md` setup, or a local commit of an already verified slice—reuses prior state and does not create plans, delegation, review, QA, or a new completion gate. Delivery scale is separate: broad work uses `itsol-initiative-delivery` with `delivery_scope: initiative`; it is never a fourth mode.

## Resolve

Apply, in order:

1. platform safety and authority rules;
2. root and most-specific `.itsol.md` defaults plus every matching path/operation restriction;
3. an explicit, unambiguous user selection;
4. an allowed repository default;
5. `governed` fallback.

Intersect repository restrictions. If they exclude the requested mode, report the matched rules and ask the user to choose an allowed mode; never silently downgrade.

- `governed`: full planning workflow or no explicit mode;
- `autonomous-planned`: user delegates plan decisions and continuation without approval pauses;
- `direct`: user explicitly omits Business, Technical, and Technical Fix Plans.

Do not infer autonomy from `continue`, `do it`, silence, or an unqualified `accept everything`.

## Required state

Propagate all seven fields through task context, plans, compaction, handoffs, and subagent packets:

```yaml
workflow_mode: governed | autonomous-planned | direct
mode_source: explicit-user-task-instruction | repo-default | fallback-default
decision_authority: user | delegated
scope: current-task
artifact_state: draft | approved | ready-for-execution | not-required
execution_mode: pending | inline | subagents | auto
protected_constraints: []
```

Missing, incomplete, inconsistent, or restriction-conflicting state is `blocked`; a child must not infer authority. Keep `Approved` (the user saw and accepted this exact artifact) distinct from `Ready for execution` (delegated authority after proportionate review). `draft` permits creating and updating planning artifacts within the requested scope; it does not authorize implementation or protected actions.

## Mode behavior

**governed** — run Discovery, Decision, plan-writing, proportionate self-review, explicit approval of each specific plan, and execution-mode gates. Plans remain `Draft` until approved; `execution_mode` remains `pending` until the user chooses.

**autonomous-planned** — create the normal plan artifacts as `Draft`; self-review proportionately, use isolated review only when policy or material risk warrants it, resolve concrete findings, choose the documented recommendation, mark artifacts `Ready for execution`, and continue without approval pauses. Never call this user approval. Ask only for an equally plausible material choice affecting behavior, permissions, data, rollout, or architecture.

**direct** — no persistent Business/Technical/Fix Plans, plan reviews, Decision Gates, plan paths, approvals, or execution-mode approval. Use `artifact_state: not-required`; retain bug evidence, focused domain review, proportionate verification, implementation review, and final self-review. No mode requires TDD or RED/GREEN; use test-first development only on explicit user request.

Workflow mode controls ceremony, not scope or external authority. Destructive data work, unrequested production publication/deployment, out-of-scope secrets, external messages/purchases, and security weakening require separate authorization. Ordinary in-scope edits, tests, local builds, and reversible configuration do not.

## Repository policy

Stable defaults belong in root or most-specific `.itsol.md`:

```yaml
workflow:
  default_mode: governed
  allowed_modes: [governed, autonomous-planned, direct]
  restrictions:
    - match: {path: infra/production}
      allowed_modes: [governed]
```

Do not create or change `.itsol.md` merely because a task selects a mode. Persist policy only when explicitly requested or included in approved scope.

## Transitions and gates

Apply mode changes only to remaining work and retain completed artifacts. Moving to `governed` pauses at the next missing gate; moving to an autonomous mode removes future approval pauses but keeps reviewed artifacts; moving to `direct` stops requiring new plan artifacts while retaining history. Summarize the transition and remaining gates; never erase plan history.

In `governed`, present options and wait for the user's selection before locking a plan. In `autonomous-planned`, record options, choose a safe recommendation, and continue. In `direct`, decide from repository evidence without recreating plan gates under another name.

## Consumers

- Router/bootstrap resolve mode before functional, bugfix, planning, implementation, or delegation gates.
- Intake/planning branch by mode; only `governed` requires full discovery and user approval pauses.
- Feature/debugging accepts `approved`, `ready-for-execution`, or `not-required` only for the matching mode.
- Self-review rejects false `Approved` claims and material findings, but not valid delegated readiness.
- Subagent packets include all seven fields and return `blocked` for invalid state.
- Repo memory supplies defaults/restrictions before resolution; domain skills defer prerequisites here.
- Final handoff reports mode, source, authority, review/verification evidence, unresolved risks, and separate action authorization.

Use exact plan metadata when applicable:

```text
Status: Approved | Ready for execution
Workflow Mode: governed | autonomous-planned
Authorization: explicit user approval | delegated by user for this task
```

Direct execution records `artifact_state: not-required` and needs no plan artifact.
Governed approval transition: `artifact_state: draft` → `artifact_state: approved` after valid user approval; autonomous continuation uses `ready-for-execution`.
