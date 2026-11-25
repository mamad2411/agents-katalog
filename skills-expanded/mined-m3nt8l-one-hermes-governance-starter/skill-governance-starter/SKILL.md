---
name: skill-governance-starter
description: Use when maintaining generic Hermes skill governance with one content-driven steward, exact-digest review, provenance-aware transactional edits, lean ecology analysis, and deterministic verification.
version: 1.1.0
author: Hermes Governance Starter
license: MIT
metadata:
  hermes:
    tags: [skills, governance, stewardship, validation, maintenance]
    related_skills: [memory-governance-starter, kanban-governance-starter]
    lifecycle: starter
    risk_level: repo_mutation_gated
    approval_required_for: [protected_source_mutation, destructive_cleanup, credential_changes]
---

# Skill Governance Starter

## Overview

Keep reusable procedures valid, focused, provenance-aware, and reviewable with one recurring owner.

Use a content-only manifest, stable-change debounce, one evidence-bound review, exact-digest acknowledgment, and quiet no-op ticks. Broad ecology analysis is recommend-only; it does not become a second maintenance loop.

## When to Use

- Auditing or maintaining a skill library.
- Creating or patching reusable workflows.
- Splitting oversized skills into a concise router plus references.
- Consolidating duplicate or fragile procedure text.
- Replacing overlapping audit/watchdog jobs with one change-driven steward.
- Verifying that a proposed edit is exact-revision, reversible, and public-safe.

## Procedure

1. Bootstrap `scripts/skill_steward.py` against the intended governance root.
2. Schedule only its `check` command for this skill surface.
3. On `wakeAgent: true`, inspect the exact relative-path diff and validation summary.
4. Classify each target as local, bundled/upstream, generated, or unknown provenance.
5. Prefer a clean acknowledgment when no source change is justified.
6. For local edits, use `scripts/skill_edit.py`: load, propose, validate, apply, receipt.
7. Rerun deterministic validation and inspect the diff.
8. Obtain independent review for material behavior changes.
9. Acknowledge only the exact digest reviewed; never acknowledge across a digest conflict.
10. Keep proposals, backups, reports, receipts, and state out of source control.

See `../../../docs/skill-governance.md` for the complete operating model and command examples.

## Common Pitfalls

1. Running a recurring auditor and recurring maintenance agent over the same skills.
2. Waking on usage counters, reports, archives, caches, or other generated churn.
3. Treating every wake as a mandatory mutation or Kanban card.
4. Editing bundled/upstream skills locally instead of fixing the owned source.
5. Applying against a stale revision or acknowledging a replacement digest.
6. Letting governance prompts trigger generic post-turn memory/skill review recursively.
7. Publishing receipts, paths, routes, IDs, or private acceptance evidence.
8. Retiring an old scheduler entrypoint with a nonzero exit or stderr-only message.
9. Confusing validator acceptance with completion of every optional backlog item.

## Verification Checklist

- [ ] Exactly one recurring skill-governance owner exists.
- [ ] No-op and unstable-change checks return `wakeAgent: false`.
- [ ] Stable content changes wake once and retry without notification spam.
- [ ] Generated/runtime churn does not change the governed digest.
- [ ] Acknowledgment is bound to the current exact digest.
- [ ] Mutation targets are local, non-symlinked, and inside the allowed root.
- [ ] Apply and rollback are hash-guarded and produce content-free receipts.
- [ ] Deterministic tests and validation pass.
- [ ] Independent review is bound to the exact staged diff when publishing.
- [ ] No secrets, private paths, operator state, or generated artifacts are staged.
