---
name: session-file-ops-audit
description: Composer — audit ALL file operations (write, append, delete, copy, move) from an opencode session export; orchestrates `opencode-session-bash-block-extractor` + `opencode-session-bash-file-ops-classifier`.
category: Meta-Automation
---

# Session File Ops Audit (v1)

> **Skill ID:** `session-file-ops-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit ALL file operations recorded in an opencode session export.

This composer orchestrates a 2-stage pipeline:

1. **Extract** — delegate to
   [`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md)
   to find every `Tool: bash` block and extract its raw command string
2. **Classify** — delegate to
   [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md)
   to classify each command as a file operation (write, append, delete,
   copy, move) or `other`

Output: human-readable terminal report with summary table + detail per
operation type, plus optional JSONL export for machine consumption.

**Use this when** you need to answer: "What did this session's bash
commands do to the filesystem?" — comprehensive coverage including
write, delete, copy, and move operations.

## Composition Rationale

This composer exists because:

1. **Separation of concerns** — extraction (finding bash blocks) and
   classification (interpreting commands) are distinct problems with
   different reuse patterns
2. **Avoiding duplication** — each base skill is independently testable
   and reusable by other composers (audit, recovery, CI pipelines)
3. **Filterability** — the `--operation` flag lets users focus on
   dangerous operations (delete) or write-only operations

## Environment & Dependencies

| Requirement | Minimum | Verification |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| `opencode-session-bash-block-extractor` | 1.0.0 | Script found at resolved path |
| `opencode-session-bash-file-ops-classifier` | 1.0.0 | Script found at resolved path |

## Operational Logic

### Input

- **Session file**: Path to opencode session export (`.md` format)
- **Optional filter**: `--operation` to limit to specific op types

### Pipeline

```mermaid
flowchart LR
    A[Session .md] --> B[extract-bash-blocks.py]
    B --> C[classify-bash-file-ops.py]
    C --> D[Report + JSONL]
```

### Processing

1. `subprocess.run` → `extract-bash-blocks.py --session <path>`
2. Pipe stdout → `classify-bash-file-ops.py [--operation <type>]`
3. Parse classified JSONL from classifier stdout
4. Generate human-readable report with summary table + per-type detail
5. Optionally write JSONL to file

### CLI Contract

```bash
python3 scripts/audit-session-file-ops.py --session <path> \
    [--operation <type>] \
    [--output-jsonl <path>] \
    [--output-report <path>]
```

| Flag | Required | Description |
|---|---|---|
| `--session` | Yes | Path to opencode session export (.md) |
| `--operation` | No | Filter: overwrite, append, write, delete, copy, move, other, all (default: all) |
| `--output-jsonl` | No | Write classified operations as JSONL |
| `--output-report` | No | Write human-readable report to file |

### Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success — at least one matching operation found |
| 1 | No matching operations found |
| 2 | Dependency script not found or pipeline failure |
| 3 | Session file not found |

## Scripts

- [`scripts/audit-session-file-ops.py`](scripts/audit-session-file-ops.py) —
  Tier-1 Python CLI

## Related Skills

- [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) —
  Superseded predecessor (heredoc-write only, no compose pipeline)
- [`file-recovery-from-session`](../file-recovery-from-session/SKILL.md) —
  Uses bash-write-extractor directly for actual file recovery (unchanged)
- [`opencode-session-path-attribution`](../opencode/opencode-session-path-attribution/SKILL.md) —
  related — maps classified move/delete ops back to their session

## Composition by Higher-Level Skills

| Composer Skill | Purpose |
|----------------|---------|
| [`session-full-change-audit`](../session-full-change-audit/SKILL.md) | Higher-level composer covering all change sources (write, edit, bash ops, bash-write). Covers a superset of this skill's scope; shells out to base scripts directly for mergeable JSONL |

## Traceability

- Origin: Layer 3 (composer) of a 3-layer architecture
- Created 2026-07-04

## License

Internal use — OleoVista Aceros workspace.
