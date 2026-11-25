---
name: diff-project
description: Shows what changed in dotforge since the project's last sync, to decide whether running /forge sync is worthwhile.
---

# Diff Project

Show what changed in dotforge since the last synchronization of the current project.

## Step 1: Identify project baseline

1. Read `$DOTFORGE_DIR/registry/projects.local.yml`
2. Find the current project by `path` (compare with `$PWD`)
3. Get `dotforge_version` and `last_sync`
4. If no `dotforge_version` is registered (null), report:
   ```
   Project not synced — no baseline to compare against.
   Run /forge sync to establish baseline.
   ```
   And stop.

## Step 2: Verify local manifest

Run `bash "$DOTFORGE_DIR/scripts/forge-doctor.sh" . --json`. It compares every file in `.claude/.forge-manifest.json` against disk and returns `intact` / `drifted` (locally modified) / `missing` (deleted) / `unmanaged` (present but never installed by dotforge). Use `dotforge_version` from the manifest as the baseline — more precise than the registry — and list drifted/missing files in the report; those are the ones a sync would have to merge rather than overwrite.

If manifest does NOT exist, continue to Step 3 using git log.

## Step 3: Detect changes in dotforge

Run in `$DOTFORGE_DIR/`:

```bash
git log --oneline v<version>..HEAD -- template/ stacks/
```

Where `<version>` is the tag corresponding to the project's `dotforge_version`.

If the tag does not exist, use `last_sync` as reference:
```bash
git log --oneline --since="<last_sync>" -- template/ stacks/
```

If there are no relevant commits, report:
```
dotforge has no changes in template/stacks since v<version>.
Project is up to date.
```

## Step 4: Show change summary

For each modified file in template/ or relevant stacks/ for the project:

```
═══ DIFF dotforge: v<previous> → v<current> ═══
Project: <name> (last sync: <date>)

Files modified in dotforge:
  template/hooks/block-destructive.sh — <diff summary>
  template/rules/_common.md — <diff summary>
  stacks/python-fastapi/rules/backend.md — <diff summary>

Local files with modifications (vs manifest):
  .claude/rules/_common.md — hash differs from deployed
```

Filter stacks/ to show only the stacks used by the project (read from registry).

## Step 5: Recommend action

If there are relevant changes:
```
Recommendation: run /forge sync to incorporate these changes.
```

If there are only cosmetic changes or changes in unused stacks:
```
Changes do not affect this project. Sync is not necessary.
```

## Installation

This skill is installed automatically if the `skills/` symlink already exists in `~/.claude/skills/`. If not, create the symlink:
```bash
ln -sf $DOTFORGE_DIR/skills ~/.claude/skills
```
