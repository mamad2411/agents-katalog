---
name: agent-session-progress
description: Use when reading local Claude Code or Codex session logs for compact, read-only progress tracking without dumping raw transcripts. Discovers recent sessions, maps metadata to transcript paths, summarizes latest event/tool signals, and estimates context usage.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude-code, codex, session-logs, progress-tracking, multi-agent]
    related_skills: []
---

# Agent Session Progress

## Overview

Read local agent session stores to understand what Claude Code or Codex is doing. This is read-only situational awareness for supervising long-running agent lanes.

## Safety Rules

- Read only. Do not write into vendor session directories.
- Do not publish raw transcripts; they can contain private prompts, file contents, and secrets.
- Redact secrets before printing.
- Prefer compact status summaries over raw text.

## Claude Code Paths

```text
~/Library/Application Support/Claude/claude-code-sessions/**/*.json
~/.claude/projects/<cwd-with-slashes-replaced-by-hyphens>/<cliSessionId>.jsonl
```

## Codex Paths

```text
~/.codex/state_5.sqlite
~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
```

## Helper

```bash
python3 scripts/agent_progress.py --agent claude --limit 10 --json
python3 scripts/agent_progress.py --agent codex --limit 10
```

## Heuristic States

- active: fresh transcript/metadata and latest events include assistant/tool activity;
- recently-active: recent update but needs semantic tail verification;
- idle-or-done: stale transcript, final assistant text, or prompt-ready state;
- blocked-or-needs-review: latest events mention permission, approval, error, failed command, or waiting for user. Avoid generic fields like `usage.input_tokens`; those are normal on completed turns and should not create blockers;
- unknown: missing/unparseable evidence.

Always present these as best-effort signals, not certainty.
