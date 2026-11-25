---
name: research-log
description: Maintain a research log that acts as an advisor, not just a diary. Registers projects; records decisions with generalizable lesson extraction; saves session state; recalls cross-project lessons and prior solutions when stuck; checks proposed approaches against promoted anti-pattern rules; runs weekly review with lesson promotion and dashboard refresh. Use when the user asks to initialize a research-log project, record an experiment or decision, save session state, recall past lessons or how a blocker was solved before, check a planned approach against past mistakes, or review all projects.
---

# Research Log

This skill maintains a unified research-log workspace in `~/.research/` and uses it to actively
improve research, not merely to record it. The data model and all file schemas are defined in
`references/conventions.md` — read it first whenever you touch the store.

The skill earns its keep at three moments:

- **M1 — decision-time guardrail.** Surface relevant anti-patterns *before* the user commits to
  an approach. See "Decision guardrail" below — this fires from conversation, not only on command.
- **M3 — recall when stuck.** Search across all projects for prior lessons and solutions.
- **M4 — real-time drift.** Flag work that has drifted from the current Compass focus.

## Decision guardrail (M1) — always active

Whenever the user proposes a research approach — an architecture, model, loss function,
methodology, experimental design, or "let's do X" choice — **before agreeing, elaborating, or
helping execute it**:

1. Read `~/.research/rules.md` (small, promoted-rules-only; cheap to load).
2. Check whether any Rule's trigger/Check matches the proposed action.
3. If a Rule matches, surface it first: "You are about to {X}; this bit you in {projects} —
   {Check}." Include the evidence. Let the user decide; do not block.
4. If nothing matches, say nothing about rules and proceed normally.

This is a behavioral directive, not a hook. It applies in any registered project's working
directory. Keep it lightweight — only promoted Rules are checked, and only when an actual
approach choice is on the table (not for routine edits or questions).

## Workflow router

Read the matching workflow reference for the user's request:

- Project registration or onboarding → `references/initialize.md`
- Recording an experiment, debugging result, or design choice → `references/record.md`
- Saving current session context → `references/save-state.md`
- Recalling past lessons / how a blocker was solved before (M3) → `references/recall.md`
- Explicitly checking a planned approach against past mistakes (M1) → `references/check.md`
- Weekly review, dashboard refresh, lesson promotion, archive scan → `references/review.md`
- Current status of a hypothesis or experiment, the board, comparing experiments, attaching results or
  plots, or resuming the session working on an experiment → the `research-board` skill (cards under
  `projects/{slug}/cards/`). Decision reasoning and lessons stay here; when an entry concerns a
  card, add a `**Card**: {slug}:Q{n}/E{m}` line to the new journal entry.

## Working rules

- Match the current working directory against the Project Registry in `~/.research/dashboard.md`
  before acting on an existing project.
- Follow the file schemas defined in `references/conventions.md` exactly.
- Acquire the per-project lock (`~/.research/.locks/{slug}.lock`) before writing project state.
- Compass `← current focus` is the anchor for drift detection; keep exactly one.
- When recording a decision, always attempt lesson extraction; when a lesson recurs across ≥ 2
  projects, propose promoting it to a Rule and regenerate `rules.md`.
- Treat dashboard updates as review-time derived data unless a workflow says otherwise.
- When a workflow requires user approval before writing, draft first and wait for approval.
- Never write to a legacy `~/.research-log/` backup; it is read-only.
