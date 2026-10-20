---
name: docs-package
description: Assemble the final handover documentation package - architecture overview, setup guide, API reference, runbooks, onboarding path. Phase 6 core skill.
---

# /docs-package

Owner: **docs-lead**; prose by **tech-writer**; runbook review by **sre-lead**.

## Sequence
1. Assemble into `docs/`:
   - Architecture overview: chosen variant, component-to-service mapping, key ADR index.
   - Setup guide: clean-clone to running-locally, every step executed to verify.
   - API reference: generated from `architecture/contracts/` (never hand-duplicated).
   - Runbooks: top failure modes, deploy/rollback, backup/restore, incident escalation.
   - SLO doc, observability guide (where to look when it breaks).
   - Onboarding path: read-this-first ordering for a new developer.
2. Completeness test: a new developer can set up, run, test, and deploy using docs/ alone —
   walk the path, log any step that required tribal knowledge, fix the doc.
3. Every doc: audience header, date + commit footer. Stale drafts marked superseded, not deleted.
4. Adopt mode: reconcile with the current-state report — one truth.
5. Improvement backlog attached (`/improvement-backlog`) so the maintaining team inherits the
   forward view.

## Output
docs/ tree complete; walk-the-path verification log; Handover gate inputs ready.
