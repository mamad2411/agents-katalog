---
name: fable-6-report
description: >-
  Report v6.1 — partial ≠ completed; open tracks listed; phases_skipped documented.
version: 6.1.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Report (v6.1)

**Playbook:** `Workflow/report/PLAYBOOK.md`

## Report gates

| objective_status | Campaign status |
|------------------|-----------------|
| `achieved` | `completed` |
| `partial` | `in_progress` — list open tracks in REPORT.md |
| exhausted | `completed` + `evidence/exhaustion.json` |

Report ONLY when `achieved` OR exhaustion documented — **not** on partial alone.

## Partial report must include

- Objectives achieved (evidence paths)
- Objectives still open (e.g. RCE, remaining cred spray)
- Skipped phases → `evidence/phases_skipped.json` or REPORT § Skipped Phases

## FORBIDDEN

- `status: completed` when `objective_status: partial`
- Finding laundry list without chain to objective
- Cleartext credentials in report body
