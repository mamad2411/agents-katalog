---
name: migration-test-writer
description: "Migration test writer: reads a schema diff (old DDL vs. new DDL), identifies structural changes, and generates pre- and post-migration validation queries. Read-only. Audience: Senior. Trigger: /migration-test"
trigger: /migration-test
---

## What this is for

A schema migration is only safe if you can verify it worked. Most teams ship
migrations without validation queries - no row-count checks, no null-consistency
checks, no referential-integrity verification, no data-loss detection. This skill
reads a schema diff (old DDL vs. new DDL) and the LLM generates validation
queries that should pass before and after the migration.

The dominant failure mode is the silent data loss or constraint violation that
only surfaces in production after the migration has run.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/migration-diff.ps1 -ProjectDir "<path>" -OldSchema "v1/schema.sql" -NewSchema "v2/schema.sql"`

### Step 4

4. LLM reads the JSON output. For each diff entry:

### Step 5

- If `requiresPreCheck` is true: generate a pre-migration validation query

### Step 6

(verify assumptions before the migration runs).

### Step 7

- If `requiresPostCheck` is true: generate a post-migration validation query

### Step 8

(verify data integrity after the migration completes).

### Step 9

5. Confidence: `proven` (deterministic diff from DDL), `likely` (inferred

### Step 10

requirement), `suspected` (edge case).

### Step 11

6. Write `migration-validation-queries.sql` to the working directory.

## Usage

```
/migration-test                         # interactive, prompts for directory
/migration-test <dir>                   # scan with default v1/v2 schema paths
/migration-test <dir> -OldSchema <path> -NewSchema <path>  # custom schema paths
/migration-test -help                   # show usage
```

Returns JSON with `diff[]`: each entry `{type, table, column, old, new,
requiresPreCheck, requiresPostCheck}` plus `counts: {tablesCompared,
totalChanges, byType}`.

## Report Format

`migration-validation-queries.sql` with:
- Pre-migration validation queries (verify assumptions before migration)
- Post-migration validation queries (verify data integrity after migration)
- Each query annotated with the diff it validates
- Confidence column for every finding
- Open questions (suspected, needs human review)
