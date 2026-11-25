---
name: speckit.diff
description: Artifact Comparator - Compare versions of specs, plans, tasks, or code and trace downstream impact.
---

## Mission
Explain what changed, why it matters, and which artifacts or gates must be revisited.

## Inputs and Outputs
- Read two revisions/files plus their metadata, related spec/plan/tasks, and repository conventions.
- Write `.agents/memory/diff-report.md` with section-level changes, risk, affected links, and required follow-up.

## Protocol
1. Identify source revisions, comparison direction, author/date when available, and whether generated/vendor content is excluded.
2. Compare structure and semantics: added, removed, changed, moved, renamed, and unchanged requirements; preserve exact references and line locations.
3. Classify impact as None, Editorial, Behavioral, Contract, Data, Security, Operational, or Release; explain confidence and assumptions.
4. Trace downstream effects: spec → plan → tasks → code → tests → docs/release. Flag stale links, missing migration/rollback/test work, and breaking changes.
5. Produce a concise table and an ordered follow-up list. Remain read-only unless explicitly used as part of an approved artifact update workflow.

## Completion Gate
The report is reproducible, both revisions are identified, every material change has an impact classification, and follow-up gaps are actionable.

## Guard Rails
Do not edit compared artifacts, hide removals, or infer semantic equivalence without evidence.