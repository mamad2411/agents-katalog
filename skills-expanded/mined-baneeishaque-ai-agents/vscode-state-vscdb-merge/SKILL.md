---
name: vscode-state-vscdb-merge
description: Base — compare key-value pairs in VS Code state.vscdb SQLite databases between two Git refs; reports stash-only/HEAD-only/common-modified key counts and — only after explicit user authorization — merges stash-only keys into HEAD.
category: VS Code / IDE Configuration
---

# VS Code state.vscdb Merge Skill (v1)

> **Skill ID:** `vscode-state-vscdb-merge`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **base skill**: it owns a single generic primitive — key-level
comparison and selective merge of VS Code's `state.vscdb` SQLite database
between two Git refs. The layering test (*"Could a different domain ever need
the same primitive?"*) is YES: stash-triage needs it (comparing stash vs HEAD
state.vscdb), VS Code environment comparisons need it, and git bisect on
settings needs it. Inlining this into any single composer would split the SSOT.

Known composers and consumers:
- [`git-stash-triage`](../git-stash-triage/SKILL.md) — invokes this skill's
  script during Phase 4d (Selective File Restoration) for per-file analysis
  of `state.vscdb` files that differ between stash and HEAD.

Bidirectional discoverability: the composer links back here in its
`## Related Skills` section.

## Description

When VS Code's `state.vscdb` files differ between two Git refs (e.g., a stash
vs HEAD), a raw `git diff` shows only binary noise. This skill extracts both
versions, reads their `ItemTable` key-value pairs, and reports:

- Keys present only in Ref A (stash-only)
- Keys present only in Ref B (HEAD-only)
- Keys in both with the same value
- Keys in both with different values

**The script is READ-ONLY by default** — it analyzes and reports without
modifying any files. An optional `--merge` flag creates a new database with
stash-only keys merged into a copy of HEAD's database, but this step requires
explicit user authorization.

## When to Apply

Apply this skill when:

- A `state.vscdb` file differs between a stash and HEAD during stash triage.
- You need to audit which VS Code settings/state keys changed between two
  commits or branches.
- Setting up a new VS Code environment and want to compare against a known
  good state.
- Running `git bisect` on VS Code state regressions.

Do NOT apply when:

- You need a generic SQLite comparison tool (not VS Code-specific schema) —
  use `sqlite3` CLI directly.
- The database file is not a VS Code `state.vscdb` (different schema).

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Python | 3.9+ |
| Access | Read access to the target repository |

## Step-by-Step Procedure

### 1. Resolve the database path

Identify the relative path of the `state.vscdb` file within the repo. Common
paths include:

- `User/globalStorage/state.vscdb`
- `User/workspaceStorage/<workspace-hash>/state.vscdb`
- `User/profiles/<profile-id>/globalStorage/state.vscdb`
- `User/globalStorage/storage.curated.json` (JSON, not SQLite — use json diff)

> [!NOTE]
> The script handles SQLite `.vscdb` files only. For JSON files like
> `storage.curated.json`, use a regular diff tool.

### 2. Resolve Ref A

- **Stash**: pass `--stash 0` (or `stash@{0}`, or a message substring).
- **Commit / branch / tag**: pass `--ref-a <ref>`.

### 3. Run the analysis (read-only)

```bash
python3 .agents/skills/vscode-state-vscdb-merge/scripts/analyze-state-vscdb.py \
    --repo /path/to/repo \
    --db-path "User/globalStorage/state.vscdb" \
    --stash 0
```

### 4. Review the report

The report shows key counts and (for small sets) the actual key names and
values. Example:

```text
Keys only in Ref A (stash):   15
Keys only in Ref B (HEAD):    3
Keys in both, same value:     460
Keys in both, DIFFERENT value: 2

--- Keys only in Ref A (stash) ---
  storage.serviceWorker
  extensionsIdentifiers/disabled
  ...
```

### 5. Decide next steps (user gate)

- **If stash has unique keys** and you want to preserve them: run with `--merge`.
- **If HEAD already has everything** you need: no action — the stash is
  superseded for this file.
- **If HEAD has keys you want to keep**: the default merge preserves all HEAD
  keys (including HEAD-only and HEAD's version of common-modified keys),
  inserting only stash-only keys.

### 6. Merge (only after explicit user authorization)

```bash
python3 .agents/skills/vscode-state-vscdb-merge/scripts/analyze-state-vscdb.py \
    --repo /path/to/repo \
    --db-path "User/globalStorage/state.vscdb" \
    --stash 0 \
    --merge \
    --output /path/to/HEAD-merged.state.vscdb
```

The merged database is written to a NEW file (default: `HEAD-merged.state.vscdb`
in the current directory). It contains all HEAD keys plus stash-only keys.
Neither the original HEAD database nor the working tree is modified.

### 7. Apply the merged database (manual step)

After the user authorizes replacement:

```bash
cp /path/to/HEAD-merged.state.vscdb /path/to/repo/User/globalStorage/state.vscdb
```

### 8. Verify

Re-run the analysis without `--merge` to confirm the working tree database now
contains the expected key count.

## Script Reference

`scripts/analyze-state-vscdb.py`

| Flag | Description |
|---|---|
| `--repo` (required) | Path to the Git repository |
| `--db-path` (required) | Relative path within repo to the `state.vscdb` file |
| `--stash` or `--ref-a` (required) | Ref A: stash index/ref/message-substring, or any Git ref |
| `--ref-b` | Ref B (default: HEAD) |
| `--merge` | Apply merge (insert stash-only keys into HEAD copy) — requires explicit user authorization |
| `--output` | Output path for merged database (default: `./HEAD-merged.state.vscdb`; only meaningful with `--merge`) |
| `--json` | Emit machine-readable JSON report instead of human-readable text |

**Exit codes:**

| Exit | Meaning |
|---|---|
| 0 | Analysis complete (or merge successful) |
| 1 | No differences found (databases identical) — exit code 0 is also returned but with "identical" message |
| 2 | Usage error / git error / SQLite error |

## Related Skills

- **[Git Stash Triage](../git-stash-triage/SKILL.md)** — invokes this skill
  during Phase 4d (Selective File Restoration) for per-file analysis of
  `state.vscdb` files.
- **[Git Ref Content Audit](../git-ref-content-audit/SKILL.md)** — bulk
  blob-equality audit between two refs (includes stash^3 untracked tree);
  complements this skill's key-level analysis of SQLite files.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`git-stash-triage`](../git-stash-triage/SKILL.md) §4d | Calls `scripts/analyze-state-vscdb.py --stash N --db-path <path> --json` during per-file triage of `state.vscdb` files; presents the JSON key-comparison report for user review; only invokes `--merge` after explicit user authorization. |

## Anti-Patterns

| Anti-pattern | Why it's wrong | Correct alternative |
|---|---|---|
| Running `--merge` without user authorization | The user must review the analysis (stash-only keys, HEAD-only keys, modified keys) before deciding to merge. | Run analysis first, present report, get explicit user authorization for merge. |
| Showing raw `git diff` for state.vscdb files | Binary diff is noise — shows no meaningful information about which keys changed. | Use this skill's `--json` analysis to show per-key differences. |
| Manually editing state.vscdb with SQLite after comparison | Direct SQLite mutations bypass the copy-first safety mechanism and risk corrupting the working tree. | Use `--merge` to create a separate output file, then `cp` after user authorization. |

## Traceability

- Initial design driven by a live stash-triage session where 15 stash-only
  keys were identified in `globalStorage/state.vscdb` and merged into HEAD
  after per-key user review. The session also identified an additional 23
  stash-only keys in a workspaceStorage state.vscdb and 9 stash-only keys
  in a profile's globalStorage state.vscdb — confirming the pattern is
  workspace-wide and reusable across all VS Code state.vscdb instances.

---

<!-- Generated by the Skill Factory (skill-factory v1) -->
