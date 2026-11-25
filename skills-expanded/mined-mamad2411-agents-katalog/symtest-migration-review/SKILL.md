---
name: symtest-migration-review
description: >-
  This skill should be used when migrating symtest test configurations from
  the pre-1.4 flat layout to the 1.4 layered Schema v2 DSL (execution /
  expected / scheduling), especially after running `symtest migrate`. It
  covers the deterministic conversion workflow (`symtest migrate` →
  `symtest validate`), the manual review checklist for parts that mechanical
  conversion cannot decide (custom comparators, complex inheritance,
  workspace plugins, setup env semantics, import structures), and the
  equivalence-invariant verification (Normalized A == Normalized B). Trigger
  when the task involves converting old symtest test_cases.json/yaml files,
  reviewing migrated configs, or diagnosing validation failures after a
  schema migration.
---

# Symtest Config Migration Review (v1 flat → v2 layered)

## Overview

Symtest 1.4 replaced the flat config layout with the layered Schema v2 DSL.
The deterministic part of the conversion is automated by `symtest migrate`;
everything that requires judgment about project-specific intent is reviewed
by hand (this skill). The authoritative field mapping lives in
`references/migration_checklist.md`.

## When to Use

- Converting a pre-1.4 `test_cases.json` / `test_cases.yaml` to the v2 DSL
- Reviewing a config that `symtest migrate` just produced
- Diagnosing `symtest validate` failures after a migration
- Auditing a repository-wide config migration before committing

## Core Workflow

```
old config → symtest migrate → new schema → symtest validate → manual review
```

1. **Run the deterministic conversion**:
   ```bash
   symtest migrate old.json --output new.json
   ```
   Default output is `<stem>.v2<ext>` (e.g. `old.json` → `old.v2.json`).
   `migrate` recursively follows the whole `import` tree as a mechanical
   field move; it never expands (inlines) imports, resolves paths, or
   validates required fields:
   - Default: every file in the tree gets a `<stem>.v2<ext>` copy and import
     paths in migrated parents are rewritten to the `.v2` names, so the
     migrated tree is self-consistent for `symtest validate`.
   - `--in-place`: every file in the tree is overwritten in place (file
     names, formats and import paths unchanged; mutually exclusive with
     `--output`).

2. **Validate the result**:
   ```bash
   symtest validate new.json
   ```
   Fix reported errors before proceeding. Validation failures after migration
   usually mean the legacy config already had missing fields that v1 tolerated
   loosely (e.g. a sequence case without step-level `expected`).

3. **Apply the manual review checklist** (`references/migration_checklist.md`).
   Mechanical conversion cannot decide project intent — verify each item and
   fix the migrated file where needed.

4. **Prove equivalence before switching over**: run the legacy config and the
   migrated config through the framework and compare outcomes (statuses,
   assertion results, compared files). For framework-level confidence, the
   project's own test suite asserts the stronger invariant
   `Normalized(legacy) == parse(migrate(legacy))` per case
   (see `tests/unit/test_migrate.py`).

5. **Commit the migrated config only after** validation passes and the
   checklist is clear. Keep the legacy file out of the way (delete or move to
   a migration backup) so tooling cannot pick up the stale layout.

## Key Facts About `symtest migrate`

- Pure mechanical mapping: `command/args/timeout/retry_count/env/steps` →
  `execution`; `depends_on/resources` → `scheduling`; `expected` and all
  metadata (`name/description/tags/xfail_*/abstract/extends/variables/import`)
  stay at top level; `setup` is untouched.
- Idempotent: input already containing `execution` is passed through
  unchanged (deep copy).
- JSON/YAML in → same format out (chosen by output file extension).
- Imports are followed recursively (never expanded inline) so the migrated
  project keeps its file split: default mode writes `<stem>.v2<ext>` copies
  with import paths rewritten; `--in-place` overwrites every file in place
  (originals are not kept).
- Unknown top-level fields are preserved verbatim — `symtest validate` and
  this skill's checklist decide whether they are still meaningful.

## References

- `references/migration_checklist.md` — the item-by-item manual review
  checklist (custom comparators, inheritance, variables, setup env, imports,
  wire-shape consumers). Consult it for every migrated project.
