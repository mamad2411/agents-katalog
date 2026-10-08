---
name: "data-model-migration-review"
description: "Review persistence model changes, migrations, compatibility, backfills, and downgrade safety. Use when a user asks for migration review, schema change risk analysis, persistence compatibility checks, or as part of $full-test-suite deep-audit work."
---

# Data Model Migration Review

Inspect data model changes for correctness, compatibility, and safe rollout.

## Focus Areas

- forward and backward compatibility
- migration ordering and rollback risk
- partial backfill behavior
- decode or persistence breakage across versions

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
