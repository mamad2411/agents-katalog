---
name: agent-loop
description: Execute lean TODO tasks through native CLI models with independent product review and targeted repairs; no procedural contract chain for new work.
---

# Agent Loop: targeted product repair

The default loop lives inside one TODO task: maker -> deterministic checks ->
independent reviewer -> actionable REPAIR to maker -> retest -> ACCEPT.
For a single small task use `agent-graph/scripts/todo_pair.py --todo <todo.json>
--run-dir <absolute-evidence-dir>`. It reuses this loop without graph scheduling.
Use TODO Graph only for real parallel branches or dependencies.

Do not create a separate Loop contract or graph for each repair. Retain the
workspace, exact findings and relevant tests. No recursive Fleet, no audit of
the reviewer, no new architecture planning for a local defect.
Stop blind repetition after the same artifact and findings occur twice.
Diagnose infrastructure errors separately from product defects. Malformed review
must not trigger recoding. Token totals are telemetry; actual provider limits and
explicit owner limits are not bypassed.
An unchanged artifact and identical checks retain their successful test evidence
when only the review/report transport is repaired. A changed artifact invalidates
that evidence. Neither a valid report nor an ACK grants product acceptance.

Legacy search/training/certified loops remain available for their existing
scientific contracts. Do not silently migrate or weaken those contracts.
