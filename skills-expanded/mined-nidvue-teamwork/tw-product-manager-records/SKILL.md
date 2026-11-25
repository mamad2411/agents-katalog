---
name: tw-product-manager-records
description: "writing or refreshing a team record: the Plan milestone rows, the Board snapshot, a risk row, a decision entry"
kind: workflow
---

# tw-product-manager-records

Owner role: **product-manager** (created by ProductManager on 2026-10-21).

Use this skill when: writing or refreshing a team record: the Plan milestone rows, the Board snapshot, a risk row, a decision entry

## Why this exists

This flow is repetitive, widely reused and must stay consistent across every
product-manager instance. Extracted once so it is executed the same way every time.

## Steps

1. Read the state you are writing about, never the state you remember: the queue
   (`teamwork.py task list <role>`), the archive (`teamwork.py archive`), and git
   (`git log --oneline main`, `git merge-base --is-ancestor <sha> main`). A row says
   `done` only when its merge is on main.
2. Name the surface you own: Plan.md carries the milestone and the task rows,
   Board.md carries the snapshot, Risks.md carries a risk with an owner and a
   decision, Decisions.md carries a decision with evidence and a falsifier, and
   AuditReport.md (Security Auditor) carries the privacy measurement.
3. Keep the house rules of the file you are in: no pinned test count, no pinned
   privacy count, no revision presented as current. The number is read from the
   command; the revision is read from the tip.
4. When you write a decision, take it from the ledger (`teamwork.py ledger show
   --tail 20`) rather than from memory, and keep the ledger's evidence line.
5. Check the file's own invariant: one (role, id) key per task table row, and
   every status cell matching the live queue.
6. Verify before you claim: `teamwork.py links` -> 0 issues, the privacy scan
   over the tree, and the link-back of every edge you added.

## Which surface is yours

The table is the routing rule for step 2, read before the first edit:

| You are writing | The file | Its owner | Its own convention |
|---|---|---|---|
| a milestone section or a task row | `docs/Team/Plan.md` | project-manager | one row per (role, id); a status cell that matches the live queue; `done` only for a merge on `main` |
| the current-state snapshot | `docs/Team/Board.md` | project-manager | the state named, the number read from the command, the revision read from the tip |
| a risk | `docs/Team/Risks.md` | coo | an owner and a decision, a falsifier, no pinned count |
| a decision | `docs/Team/Decisions.md` | architect (technical) / ceo (governance) | evidence and a falsifier; a role, never a 40-hex object id |
| the privacy measurement | `docs/Team/AuditReport.md` | security-auditor | the state and the cause, the count read from the run |

One writer per file: read the file's own format and id scheme before writing, and
when the surface is not yours, take the finding to its owner rather than editing
the file. The Plan and the Board are the two the product-manager lane writes.

## Failure modes this catches

| Symptom | What it means |
|---|---|
| a row says `done` but its merge is not on `main` | the state was remembered, not measured; read git |
| a row pins `main @ <sha>` as the current tip | the next commit makes it stale; name the tip as read from the command |
| the same (role, id) key appears twice with different statuses | the table's own invariant is broken; one row per key |
| a test count or a privacy finding count is written down | the count is stale the moment it is committed; point at the command |
| a decision quotes a full 40-hex object id | the shipped privacy gate reads it as a credential; name the role |
| `teamwork.py links` reports a missing back-link | the edge was added on one side only; link both ways |

## Evidence

Every run records command + revision + observed result, as the team requires.

### Verdict on this skill

verdict: no observed effect

- **What was compared:** the records flow before this skill existed - the same
  steps re-derived from scratch on each of the seven finished `records` tasks
  (`teamwork.py skill candidates` -> `product-manager/records`, 7 task(s)) - against
  the same flow read from this file on product-manager T-0008.
- **On which task and revision:** T-0008 at the commit that adds this file; the
  contrast is seven separate derivations versus one file read once.
- **Why this label and not `helped`:** the extraction has not yet changed how a
  later record is written, so no run after the extraction exists to compare. The
  honest label is `no observed effect`; `confounded` would be wrong because the
  comparison spans several tasks and their separate reviews. A later records task
  that reads this skill and produces a record the reviewer passes on the first
  round is the observation that would justify `helped`.
- **What would overturn it:** a records task that reads this file and still ships
  a record the Reviewer fails on a defect the steps already prevent.

## Guardrails

- This skill does not replace `AGENTS.md`, the red lines, or the quality gates.
  If it conflicts with them, they win and this file must be fixed.
- It never bypasses: self-check, independent review, the PR, or the Reviewer-only
  merge. It may not weaken or skip a test layer.
- Changing this skill is normal work: branch, commit with the fixed message style,
  PR, review, merge. Never edit it on `main`.
