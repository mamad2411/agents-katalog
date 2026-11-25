---
name: edit-application-from-session
description: Composer — replay Tool: edit operations from an opencode session export onto existing on-disk files; uses `opencode-session-edit-extractor` to extract edit payloads (filePath, oldString, newString) → apply replacements → verify changes
category: Meta-Automation
---

# Edit Application from Session

## Composition Rationale

This composer exists because applying `Tool: edit` payloads from a
session export requires two distinct capabilities that are independently
reusable:

1. **Extraction** — finding `Tool: edit` JSON payloads in session
   markdown. Delegated to `opencode-session-edit-extractor` so audit,
   diff, and CI tools can reuse the same parsing.
2. **Apply + Verify** — reading each target file, performing the
   `oldString → newString` replacement, and confirming the replacement
   occurred. This is the composer's value-add.

Separating extraction from application means the same base extractor
serves both edit-replay and audit workflows.

## Composition by Lower-Level Skills

| Skill | Role |
| :--- | :--- |
| [`opencode-session-edit-extractor`](../opencode-session-edit-extractor/SKILL.md) | Extract `Tool: edit` JSON payloads |

## CLI

```bash
python3 scripts/apply-edits.py \
  --session <path-to-session-export.md> \
  [--file-pattern <glob>] \
  [--output-dir <dir>] \
  [--dry-run]
```

### Options

| Option | Description |
| :--- | :--- |
| `--session` | Path to OpenCode session export markdown (required) |
| `--file-pattern` | Glob to filter payloads by `filePath` (e.g. `**/*.md`) |
| `--output-dir` | Write modified copies to this directory (originals unchanged) |
| `--dry-run` | Preview edits to apply without modifying files |

### Exit codes

| Code | Meaning |
| :--- | :--- |
| 0 | All edits applied and verified |
| 1 | One or more edits failed |
| 2 | No edit payloads found |
| 3 | Session file not found or extractor script missing |

## Workflow

1. User provides a session export `.md` file containing `Tool: edit`
   blocks
2. Composer invokes `opencode-session-edit-extractor` as subprocess
3. Extractor returns JSONL payloads
   (`{"filePath", "oldString", "newString"}`)
4. For each payload, composer reads the target file, replaces
   `oldString` with `newString`, and writes back
   (or to `--output-dir`)
5. Composer verifies the replacement occurred and `newString` is present

## Verification

```bash
# Dry-run to preview
python3 scripts/apply-edits.py --session session-export.md --dry-run

# Apply edits in-place
python3 scripts/apply-edits.py --session session-export.md

# Apply edits to output directory (originals unchanged)
python3 scripts/apply-edits.py --session session-export.md --output-dir ./recovered
```

## Related Skills

- [`opencode-session-write-extractor`](../opencode-session-write-extractor/SKILL.md) —
  Parallel base skill for `Tool: write` extraction (used by
  `file-recovery-from-session`)
- [`file-recovery-from-session`](../file-recovery-from-session/SKILL.md) —
  Parallel composer for recovering `Tool: write` and bash heredoc files
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Higher-level composer that includes edit payloads in unified change
  audits
