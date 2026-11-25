---
name: file-recovery-from-session
description: Composer — recover files written via `Tool: write` or `Tool: bash` heredocs during an OpenCode session; uses `opencode-session-write-extractor` and `opencode-session-bash-write-extractor` to extract payloads → write to disk → verify content integrity
category: Meta-Automation
---

# File Recovery from Session

## Composition Rationale

This composer exists because file recovery from session exports requires
two distinct capabilities that are independently reusable:

1. **Extraction** — finding `Tool: write` and `Tool: bash` heredoc
   payloads in session markdown. This is delegated to base primitives
   so other tools (audit, CI, diff) can reuse the same parsing logic.
2. **Write + Verify** — writing content to disk at the correct path and
   confirming byte-level integrity. This is the composer's value-add.

Separating extraction from recovery means the same base extractors
serve both recovery and audit workflows.

## Composition by Lower-Level Skills

| Skill | Role |
| :--- | :--- |
| [`opencode-session-write-extractor`](../opencode-session-write-extractor/SKILL.md) | Extract `Tool: write` JSON payloads |
| [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) | Extract `Tool: bash` heredoc file writes |

## CLI

```bash
python3 scripts/recover-files.py \
  --session <path-to-session-export.md> \
  [--mode write|bash|all] \
  [--file-pattern <glob>] \
  [--output-dir <dir>] \
  [--dry-run]
```

### Options

| Option | Description |
| :--- | :--- |
| `--session` | Path to OpenCode session export markdown (required) |
| `--mode` | Source of file writes: `write` (Tool: write), `bash` (bash heredocs), or `all` (both, default) |
| `--file-pattern` | Glob to filter payloads by `filePath` (e.g. `**/*.md`) |
| `--output-dir` | Redirect all recovered files to this directory (uses basenames) |
| `--dry-run` | Preview files to recover without writing to disk |

### Exit codes

| Code | Meaning |
| :--- | :--- |
| 0 | All payloads written and verified |
| 1 | One or more payloads failed to write or verify |
| 2 | No payloads found |
| 3 | Session file not found or extractor script missing |

## Workflow

1. User provides a session export `.md` file
2. Composer invokes the appropriate base extractor(s) as subprocess(es)
3. Extractor returns JSONL payloads (`{"filePath": "...", "content": "..."}`)
4. Composer writes each payload to disk at its original path
   (or `--output-dir`)
5. Composer verifies content integrity by comparing file sizes

## Verification

After recovery, verify with standard tools:

```bash
# Check file sizes match
python3 scripts/recover-files.py --session session-export.md --mode all --dry-run

# Then perform recovery
python3 scripts/recover-files.py --session session-export.md --mode all
```

## Related Skills

- [`opencode-session-edit-extractor`](../opencode-session-edit-extractor/SKILL.md) —
  Parallel base skill for `Tool: edit` extraction (used by
  `edit-application-from-session`)
- [`edit-application-from-session`](../edit-application-from-session/SKILL.md) —
  Parallel composer for applying `Tool: edit` payloads
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Higher-level composer that includes write + bash-write payloads in
  unified change audits
