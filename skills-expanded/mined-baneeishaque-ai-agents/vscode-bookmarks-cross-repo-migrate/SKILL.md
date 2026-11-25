---
name: vscode-bookmarks-cross-repo-migrate
description: >-
  Composer — migrate VS Code .vscode/bookmarks.json entries across repos:
  discover moved files, remap paths, merge via the vscode-bookmarks-merge
  base, write merged result, clean up source.
category: VS Code / IDE Configuration
---

# VS Code Bookmarks Cross-Repo Migration Skill (v1)

> **Skill ID:** `vscode-bookmarks-cross-repo-migrate`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **composer**: it does NOT re-implement bookmark merge logic.
It orchestrates two concerns:

1. **Domain-specific path remapping** — given that files have moved from a
   source repo to a target repo, discover the new relative path for each
   old bookmark path.
2. **Base merge primitive** — delegates the actual JSON merge, deduplication,
   and sorting to the [`vscode-bookmarks-merge`](../vscode-bookmarks-merge/SKILL.md)
   base skill (specifically its `scripts/merge-bookmarks.py`).

The composer's domain-specific value-add over the base alone: it handles the
cross-repo discovery problem — determining which files from the source
bookmark entries exist in the target repo and where — so the user does not
need to manually map paths.

Inlining the merge logic into this composer would duplicate the SSOT that
`vscode-bookmarks-merge` already owns.

Bidirectional discoverability: `vscode-bookmarks-merge` lists this composer
in its `## Composition by Higher-Level Skills` table.

## Description

### In scope

- Given a source repo path and a target repo path, open the source repo's
  `.vscode/bookmarks.json`.
- For each file entry in the source bookmarks, attempt to find the same
  file in the target repo by:
    - Checking if the file exists at the same relative path in the target repo.
    - If not found, checking common relocation patterns (e.g., files moved
    into a `docs/` subdirectory, renamed from `old-name` to `new-name`, etc.)
    - Reporting unmapped paths for manual resolution.
- Build a path remapping dictionary from old relative path to new relative
  path.
- Apply the remapping to the source bookmarks (creating a temporary file).
- Invoke the [`vscode-bookmarks-merge`](../vscode-bookmarks-merge/SKILL.md)
  base script to merge the remapped source into the target bookmarks file.
- Write the merged result to the target repo's `.vscode/bookmarks.json`.
- Optionally clean up the source repo's bookmark file (remove only the
  entries that were successfully migrated, or empty the file if all entries
  were moved).

### Out of scope

- Moving the actual files between repos — this skill assumes the files have
  already been moved.
- Complex path transformations beyond the common patterns documented in §4.
- Git operations (commit, push) — this skill operates only on working-tree
  files.

## When to Apply

Apply this skill when:

- Files have moved from repo A to repo B and the VS Code bookmarks in
  repo A point to stale paths.
- You need to merge bookmarks from one repo's `.vscode/bookmarks.json`
  into another's, with automatic path remapping.
- You are splitting a monorepo and want to preserve bookmark state.

Do NOT apply when:

- There is no target repo yet (use `vscode-bookmarks-merge` base directly
  if just merging two files).
- The migration of files between repos has not happened yet.
- You only need to edit or clean a single bookmark file.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |
| Access | Read access to both source and target repos |

---

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`json`, `sys`, `argparse`,
  `pathlib`, `subprocess`, `os`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Base Skill Dependency

This skill requires the base skill's script to be present:

```bash
ls .agents/skills/vscode-bookmarks-merge/scripts/merge-bookmarks.py
```

---

## 2. CLI Contract

Located at [`scripts/migrate-cross-repo.py`](./scripts/migrate-cross-repo.py).

```bash
python3 .agents/skills/vscode-bookmarks-cross-repo-migrate/scripts/migrate-cross-repo.py \
    --source-repo <path-to-source-repo> \
    --target-repo <path-to-target-repo> \
    [--dry-run] \
    [--clean-source] \
    [--remap-file <remap.json>]
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--source-repo` | Yes | — | Absolute path to the source repository. |
| `--target-repo` | Yes | — | Absolute path to the target repository. |
| `--dry-run` | No | — | Show what would happen without writing files. |
| `--clean-source` | No | — | After successful migration, remove migrated entries from source bookmarks (or empty if all moved). |
| `--remap-file` | No | auto | Path to a JSON remap dictionary (for manual overrides). |

### 2.2 Input

The source repo must have a `.vscode/bookmarks.json` file. The target repo
should have a `.vscode/bookmarks.json` file (it will be created if missing).

### 2.3 Output

The merged `.vscode/bookmarks.json` is written to the target repo. If
`--clean-source` is set, the source file is updated to remove migrated
entries.

### 2.4 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Migration completed successfully. |
| 1 | Input validation error. |
| 2 | Source or target repo path not found. |
| 3 | Base merge script not found. |
| 4 | One or more file paths could not be remapped (user must resolve manually). |

---

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Verify Both Repos Exist

```bash
ls "/path/to/source-repo/.vscode/bookmarks.json"
ls "/path/to/target-repo/.vscode/bookmarks.json"
```

### 3.3 Step 3 — Dry-Run Migration

```bash
python3 .agents/skills/vscode-bookmarks-cross-repo-migrate/scripts/migrate-cross-repo.py \
    --source-repo /path/to/source-repo \
    --target-repo /path/to/target-repo \
    --dry-run
```

Review the remapping report and merged output.

### 3.4 Step 4 — Execute Migration

```bash
python3 .agents/skills/vscode-bookmarks-cross-repo-migrate/scripts/migrate-cross-repo.py \
    --source-repo /path/to/source-repo \
    --target-repo /path/to/target-repo
```

### 3.5 Step 5 — Clean Up Source (Optional)

```bash
python3 .agents/skills/vscode-bookmarks-cross-repo-migrate/scripts/migrate-cross-repo.py \
    --source-repo /path/to/source-repo \
    --target-repo /path/to/target-repo \
    --clean-source
```

### 3.6 Step 6 — Verify Result

Open both repos' `.vscode/bookmarks.json` and confirm:

- Target has the expected merged entries.
- Source (if cleaned) has only unmapped entries or is empty.
- All bookmarks reference files that exist in their respective repos.

---

## 4. Path Remapping Strategy

The migration script uses the following strategy when remapping paths:

### 4.1 Same-Path Match (Fast Path)

If the source bookmark's relative path exists at the same relative path in
the target repo, use it as-is.

### 4.2 Common Relocation Patterns

If the direct path does not exist, the script checks these common patterns:

1. **Docs prefix**: Source path `oleovista-acer-teams-chats/opencode-session-exports/...`
   → check `docs/opencode-session-exports/...` in target.
2. **Root-level move**: Files that were in a subdirectory in source repo but
   are now at the repo root in target (e.g., `subdir/file.md` → `file.md`).
3. **Subdirectory nesting**: Files at repo root in source that moved into
   a subdirectory in target.

### 4.3 Manual Remap Override

If any paths cannot be automatically remapped, the script lists them and
exits with code 4. The user can provide a manual remap file via
`--remap-file` with the format:

```json
{
  "old/path/in/source.md": "new/path/in/target.md"
}
```

---

## 5. Edge Cases & Constraints

- **Missing bookmark file in target**: Created with `{"files": []}`.
- **Empty source bookmarks**: No migration needed.
- **No remappable paths**: Script exits with code 4 and lists unmapped paths.
- **---clean-source without merge**: Ignored if merge fails.
- **Cross-repo paths**: Source and target must be independent repos (or
  different directories). The script does NOT handle Git submodule paths.

---

## 6. Prohibited Actions

- The Agent MUST NOT re-implement the merge-dedupe-sort algorithm inline —
  delegate to the [`vscode-bookmarks-merge`](../vscode-bookmarks-merge/SKILL.md)
  base script.
- The Agent MUST NOT modify files outside the two repos' `.vscode/` directories.
- The Agent MUST NOT run this skill if the file migration between repos has
  not yet occurred — the remapping will produce incorrect results.

---

## 7. Script Reference

[`scripts/migrate-cross-repo.py`](./scripts/migrate-cross-repo.py) performs:

1. Parse `--source-repo`, `--target-repo`, `--dry-run`, `--clean-source`,
   `--remap-file`.
2. Read source repo's `.vscode/bookmarks.json`.
3. For each file entry, attempt path remapping via §4 strategy.
4. Create a temporary remapped source bookmark file.
5. Shell out to the base script:

   ```bash
   python3 <base>/scripts/merge-bookmarks.py \
       --source <temp-remapped.json> \
       --target <target>/bookmarks.json \
       --output <target>/bookmarks.json
   ```

6. If `--clean-source`: update the source bookmark file by removing entries
   that were successfully remapped (or empty if all were moved).
7. Clean up temporary files.

---

## 8. Composition by Higher-Level Skills

*(None — this skill is a top-level composer. It does not feed into any higher
composer.)*

---

## Related Skills

- [`vscode-bookmarks-merge`](../vscode-bookmarks-merge/SKILL.md) — base
  primitive for the actual JSON merge, deduplication, and sorting.
- [`json-diff-cli`](../json-diff-cli/SKILL.md) — for previewing differences
  between source and target bookmarks before migration.

---

## 10. Traceability

- **Created**: 2026-07-14
- **Source**: cross-repo VS Code bookmark migration from `oleovista-acers` to `ai-suite`.
- **Design rationale**: Separated as a composer skill because the path
  remapping logic is domain-specific (depends on knowledge of how files were
  relocated), while the merge logic is a generic primitive.
