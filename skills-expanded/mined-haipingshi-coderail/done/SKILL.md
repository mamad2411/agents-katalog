---
name: done
description: Finish a task the safe way: verify it, keep changes in scope, sync the docs, commit safe files, and state the next step. Run this instead of declaring done from memory.
---

# done

`coderail done` is the single completion authority. Run it once; it owns
verification, scope classification, task state, trace, progress, final Inspect,
and the exact task-scoped commit.

## Required order

Use the host workspace skill for plugin-root invocation. `workspace paths`
resolves the logical paths below in opted-in projects; never create fallback
legacy archives when a selected workspace is missing or interrupted.

1. Confirm the implementation, declared verification, and every acceptance
   result are ready. Put all required `--accept-status` values on the first call.
2. Run `python .coderail/coderail.py done`. Add `--owner-locale zh-CN` or `en`
   only when an explicit override is useful. Cheap argument, acceptance,
   inventory, and current-scope checks precede expensive verification.
3. If it fails, repair the named issue and rerun only when the task remains open.
4. If it succeeds, report its result without manually repeating TASKS, TRACE,
   Inspect, staging, or commit steps.

## Two projections

The successful localized command prints the Owner Receipt: 3-6 sentences about
new capability, evidence boundary, remaining gap, next step, and owner decision.
Do not add task IDs, paths, governance jargon, or unannotated English to it.

Lifecycle state, exact verification, paths, and Git receipts stay in
`docs/CODERAIL_STATUS.md` (Agent Blackboard) and `.coderail/reports/`
(Technical Report). `docs/DELIVERIES.jsonl` stores append-only product delivery
facts but never becomes lifecycle authority.

Locale resolution is explicit flag, saved preference, explicit host locale,
then deterministic English. Unknown but valid locales and renderer failures
produce a diagnostic fallback receipt. They do not rerun verification, commit,
or lifecycle writes and do not convert a successful transaction into failure.

## Rules

- Do not hide failed verification.
- Do not treat damaged delivery facts, unsafe scope, or an incomplete transaction
  as a presentation problem.
- Do not turn a failed gate into a narrative success.
- Do not create a second completion sequence after `coderail done` succeeds.
- Do not rerun a passing CI inside the same closeout transaction. Reuse is valid
  only through its checked receipt; invalid or absent evidence makes a direct
  lower-level entry run its own gates.
- Use the compact stage/count/time/result output for progress. Open the named
  `.coderail/reports/` log only when diagnosis needs the full output.
- Do not paste the Agent Blackboard or Technical Report into the Owner Receipt.
- Do not edit generated closeout state merely to make the report look cleaner.
