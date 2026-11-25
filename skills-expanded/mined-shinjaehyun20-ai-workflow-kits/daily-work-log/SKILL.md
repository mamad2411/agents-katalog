---
name: daily-work-log
description: Record a date-bounded work log from evidence with status, owner scope, blockers, and next actions. Use before an evidence-backed weekly report.
---

# Daily Work Log

Read `../../../../WORK_LOG_CONTRACT.md` before writing.

## Goal

```text
work date -> source coverage -> evidence-backed items -> local save -> read-back
```

## Workflow

1. Lock the date, timezone, sources, log target, and verifier.
2. Check whether the target log exists. Preserve it and make the smallest item-level update.
3. Record source coverage. Do not convert unavailable sources into no-work findings.
4. For each item, include status, what changed, evidence, confirmed owner scope, and next action.
5. Keep artifacts, automation outputs, and human work attribution separate.
6. Save locally and read the file back for headings, date, item status, evidence, and next action.
7. State explicitly that no external send, publish, or approval occurred unless it did.

## Weekly Report Handoff

The logs in the requested date range are priority input for `weekly-report-evidence`. A later report must still reconcile the prior plan and supplementary sources.

## Do Not

- infer completion from timestamps;
- write missing facts from memory;
- claim generated output as personal performance;
- rewrite unrelated content;
- treat save as send, publish, or approval.
