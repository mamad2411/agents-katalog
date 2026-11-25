---
name: schema-unify
description: Plan and verify safe consolidation of local brain page types or upstream gbrain schema packs.
---

# Schema Unify

Use this skill when the user asks to clean up page types, migrate to a canonical taxonomy, or inspect whether the brain schema has drifted.

This port is adapted from `garrytan/gbrain` at commit `814258dda67945ffec9457a1e73980e947b7e462`.

## Workflow

1. Identify the substrate:
   - repo-local file-backed `brain/`
   - upstream `gbrain` CLI database
   - another user-specified brain store
2. Run read-only discovery:
   - local: inspect frontmatter/type fields and run `python3 scripts/brain_doctor.py`
   - upstream CLI: `gbrain schema active`, `gbrain schema stats`, and `gbrain onboard --check --explain` when available
3. Produce a migration plan before applying anything:
   - current type inventory
   - target taxonomy
   - aliases or redirects
   - rollback path
   - validation commands
4. Apply only after explicit approval.
   - when an upstream protected migration handler defaults to a dry run, keep
     preview and apply distinct and pass its explicit apply flag only after
     approval
5. Verify and summarize what changed.

## Codex Adaptation

- This repo's current local brain substrate is lightweight Markdown, so the default path is audit-and-plan, not automatic database migration.
- Upstream protected handlers such as `unify-types` require explicit local approval and should not be launched from a remote or ambiguous context.

## Guardrails

- Do not bulk-retype pages without a dry-run inventory.
- Do not collapse semantically different page types just to reduce counts.
- Preserve legacy type information or a rollback note for every applied migration.
- Do not treat upstream `gbrain-base-v2` availability as proof that this repo should adopt it unchanged.
