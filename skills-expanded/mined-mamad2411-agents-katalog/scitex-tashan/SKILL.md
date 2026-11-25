---
name: scitex-tashan
description: "Use when operating the Tashan (他山) project workflows: project info lookup and seed intake object types, batches, records, and stocks."
metadata:
  requires:
    bins: ["scitex"]
  cliHelp: "scitex project tashan --help"
---

# Scientex Tashan Project Workflows

**Before starting, read `../scitex-shared/SKILL.md` for auth, safety, and OpenAPI rules.**

Use this skill for Tashan (他山) project-scoped APIs under `scitex project tashan ...`. Other projects have their own skill packages.

## Info

```bash
scitex project tashan info -f json
```

## Seed Intake

```bash
scitex project tashan seed object-types list -f json
scitex project tashan seed object-types create '<JSON_OR_FILE>' -f json
scitex project tashan seed object-types get <CONFIG_ID> -f json
scitex project tashan seed object-types update <CONFIG_ID> '<JSON_OR_FILE>' -f json

scitex project tashan seed batches list -f json
scitex project tashan seed batches create '<JSON_OR_FILE>' -f json
scitex project tashan seed batches get <BATCH_ID> -f json
scitex project tashan seed batches import-manifest <BATCH_ID> --file <PATH> -f json
scitex project tashan seed batches create-intake-task <BATCH_ID> --record-id <RECORD_ID> -f json

scitex project tashan seed records list --batch-id <BATCH_ID> --status <STATUS> -f json
scitex project tashan seed records public --batch-id <BATCH_ID> -f json
scitex project tashan seed records get <RECORD_ID> -f json
scitex project tashan seed records update <RECORD_ID> '<JSON_OR_FILE>' -f json
scitex project tashan seed records complete <RECORD_ID> -f json

scitex project tashan seed stocks list -f json
scitex project tashan seed stocks get <STOCK_ID> -f json
```

## Schema

Inspect `<SCIENTEX_BASE_URL>/openapi.json` before preparing create/update JSON.

Relevant schemas:

- `SeedObjectTypeConfigCreate`
- `SeedObjectTypeConfigUpdate`
- `SeedIntakeBatchCreate`
- `SeedIntakeRecordUpdate`
- `IntakeTaskRequest`

JSON inputs may be inline JSON strings or local JSON file paths.

## Rules

- Confirm before creating or updating object types, batches, and records.
- Confirm before completing intake records.
- Prefer `-f json` for all project workflows.
- Do not use this skill for user administration, signup, password recovery, or audit/log endpoints.
