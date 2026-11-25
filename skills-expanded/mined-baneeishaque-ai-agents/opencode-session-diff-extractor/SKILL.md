---
name: opencode-session-diff-extractor
description: Base — extract git diff blocks from opencode session export files (markdown format) via CLI; domain-agnostic primitive for any file recovery workflow.
category: Meta-Automation
---

# OpenCode Session Diff Extractor Skill

> **Skill ID:** `opencode-session-diff-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Extract `git diff` output blocks from opencode session export files (markdown
format with tool call/response structure). This is a **domain-agnostic base
primitive** — it knows nothing about AGENTS.md or any specific file. It parses
the session markdown, locates tool invocations where `command` contains
`git.*diff`, and emits the diff block in unified format to stdout or a file.

**Composition**: Consumed by `agents-md-recovery-from-session` (composer) for
AGENTS.md-specific recovery. Could be reused for any file recovery from session exports.

## Composition Rationale

This primitive exists as its own base skill because git diff blocks in
session exports have a distinct structure — they appear as output of
`Tool: bash` commands, but their format (unified diff starting with
`diff --git`) is entirely different from heredoc file writes or JSON
tool payloads. Parsing diff output requires detecting the diff header,
extracting hunks, and preserving line-level granularity. Making this a
standalone skill keeps the diff-specific regex and hunk-handling logic
isolated and reusable by any downstream consumer needing to apply
session-recorded diffs.

## Environment & Dependencies

| Requirement | Minimum | Verification |
|-------------|---------|--------------|
| Python | 3.12+ | `python3 --version` |
| opencode CLI | session export format v1 | N/A (parses exported markdown) |

```bash
python3 --version
```

## Operational Logic

### Input

- **Session file**: Path to opencode session export (`.md` format)
- **Optional file pattern**: Filter diffs to specific file path(s) (e.g., `AGENTS.md`, `.agents/skills/**/SKILL.md`)

### Processing

1. Read session file as text
2. Locate all tool call blocks where:
   - Tool = `bash` (or `command` in older exports)
   - Input `command` contains `git` and `diff`
   - Output contains a unified diff block (starts with `diff --git`)
3. For each matching block, extract the diff content (from `diff --git` to
   closing fence)
4. If file pattern provided, filter hunks to only those affecting matching paths
5. Emit concatenated unified diff to stdout

### Output

- **stdout**: Concatenated unified diff (suitable for `git apply`)
- **stderr**: Progress/diagnostic messages
- **Exit code**: 0 = success, 1 = no diffs found, 2 = parse error, 3 = file not found

### CLI Contract

```bash
python3 scripts/extract-session-diff.py --session <path> [--file-pattern <glob>] [--output <path>]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--session` | Yes | Path to opencode session export (.md) |
| `--file-pattern` | No | Glob pattern to filter diff hunks (e.g., `AGENTS.md`) |
| `--output` | No | Write diff to file instead of stdout |

## Composition by Higher-Level Skills

| Composer Skill | Purpose |
|----------------|---------|
| `agents-md-recovery-from-session` | Extract AGENTS.md diff → apply → verify alphabetical order → lint |

## Scripts

- [`scripts/extract-session-diff.py`](scripts/extract-session-diff.py) —
  Tier-1 Python CLI (see [Scripting Language Selection Rules §3.1](../../../ai-agent-rules/scripting-language-selection-rules.md))

## Related Skills

- [`opencode-session-write-extractor`](../opencode-session-write-extractor/SKILL.md) —
  Parallel base skill for `Tool: write` payload extraction
- [`opencode-session-edit-extractor`](../opencode-session-edit-extractor/SKILL.md) —
  Parallel base skill for `Tool: edit` payload extraction
- [`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md) —
  Parallel base skill for bash command extraction
- [`agents-md-recovery-from-session`](../agents-md-recovery-from-session/SKILL.md) —
  Composer that consumes this skill for AGENTS.md recovery
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Composer that includes this skill's output in unified change audits

## Traceability

- Origin: 2026-06-29 — recovery of AGENTS.md after `git checkout HEAD --
  AGENTS.md` lost 7 skill rows

## License

Internal use — OleoVista Aceros workspace.
