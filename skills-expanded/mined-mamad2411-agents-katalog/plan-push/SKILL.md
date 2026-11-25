---
name: plan-push
description: >
  Push ready REQs to Linear as a parent issue (EPIC) plus child issues
  (REQs) with blockers and acceptance criteria. Use when the user says
  push to Linear, export issues, or runs /ultimate-sdd:push.
license: MIT
metadata:
  author: andrewr303
  version: "2.1"
---

Export the plan graph to Linear. Local files stay the source of truth.

**Supporting files:** `references/model.md`. Linear MCP: `Linear__save_issue` (create/update), `Linear__list_issues` to avoid dupes.

## Gate

- Only push REQs with readiness ≥ 4 unless the user says "push drafts too".
- Ask for Linear **team** if unknown.
- Dry-run first: print the issue tree, then create after confirm (skip confirm if they said "just push").

## Mapping

| Plan | Linear |
|---|---|
| EPIC-n | Parent issue `EPIC-n · <title>` |
| REQ-n | Child, `parentId` = EPIC issue |
| `blocked_by` | `blockedBy` on create |
| AC list | Markdown checklist in description |
| effort low/med/high | estimate 1 / 3 / 5 if the team uses estimates; else omit |
| priority P0/P1/P2 | Linear priority 2 / 3 / 4 |

Description body:

```
REQ-n (SPEC-k) · readiness n/5

## Acceptance criteria
- [ ] AC-1 …
```

## Dedup

If the REQ already has `linear: LIN-123`, update that issue instead of creating another. After create, write `linear: <identifier>` on the REQ.

## Fallback

If Linear MCP is unavailable, write `docs/plan/export/linear.md` with the same tree and stop. Do not pretend the issues exist.

## Guardrails

- Do not change REQ status to `in-progress` just because it was pushed.
- Do not push TASKs unless the user asked.
- Never put secrets in the Linear description.
