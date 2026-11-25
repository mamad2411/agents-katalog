---
name: agent-session-handover
description: Use this skill when the user asks one local AI agent to inspect, continue from, hand off, summarize, or compare another local agent session, especially Cursor agent transcripts under ~/.cursor/projects, Codex sessions under ~/.codex/sessions, and Claude Code transcripts under ~/.claude/projects.
---

# Agent Session Handover

Use this skill to read local JSONL session transcripts across agents without pretending there is live chat sync.

## Ground Rules

- Be explicit about the source: Cursor transcript, Codex session, Claude Code transcript, or another supplied JSONL path.
- Treat session access as file-based. Do not claim direct access to another app's in-memory conversation.
- Prefer digesting the last relevant messages over dumping whole transcripts.
- Do not write into original transcript files.
- Session transcripts can contain secrets, private paths, and tool output. Summarize only what is needed.
- Check file mtimes when recency matters; a "latest" file can still be stale.

## Quick Start

Set the script path:

```bash
export AGENTS_SKILLS_ROOT="${AGENTS_SKILLS_ROOT:-$HOME/.agents/skills}"
export SESSION_HANDOVER="$AGENTS_SKILLS_ROOT/agent-session-handover/scripts/agent_session_handover.py"
```

List recent sessions:

```bash
python3 "$SESSION_HANDOVER" list --source all --limit 10
python3 "$SESSION_HANDOVER" list --source cursor --limit 5
python3 "$SESSION_HANDOVER" list --source codex --limit 5
python3 "$SESSION_HANDOVER" list --source claude --limit 5
```

Read the latest session:

```bash
python3 "$SESSION_HANDOVER" latest --source cursor
python3 "$SESSION_HANDOVER" digest "$(python3 "$SESSION_HANDOVER" latest --source codex)" --last 12
python3 "$SESSION_HANDOVER" digest "$(python3 "$SESSION_HANDOVER" latest --source claude)" --last 12
```

Find a Claude Code session by its title. The `list` label is the session's
title (the name shown in Claude Code), so match on it and read that path:

```bash
python3 "$SESSION_HANDOVER" list --source claude --limit 20
python3 "$SESSION_HANDOVER" list --source claude --json \
  | python3 -c "import json,sys; rows=json.load(sys.stdin); print(next(r['path'] for r in rows if 'Conversion optimization' in r['label']))"
```

Read a known transcript:

```bash
python3 "$SESSION_HANDOVER" digest /path/to/session.jsonl --last 12
python3 "$SESSION_HANDOVER" show /path/to/session.jsonl --last 20
```

Prepare handoff text for another agent:

```bash
python3 "$SESSION_HANDOVER" handoff --from cursor --to codex --last 12 --task "Continue this work."
python3 "$SESSION_HANDOVER" handoff --from codex --to cursor --last 12 --task "Review the decision and adjust the Cursor plan."
```

## Workflow

1. Locate the session with `list` or use the path supplied by the user.
2. Run `digest` first. Use `show` only when exact wording matters.
3. State what file was read and whether it is current enough for the request.
4. Continue from the extracted context, or produce `handoff` text for the other agent.

## Supported Sources

- Cursor main agent transcripts: `~/.cursor/projects/*/agent-transcripts/*/*.jsonl`
- Cursor subagent transcripts: included only when `--include-subagents` is passed.
- Codex sessions: `~/.codex/sessions/**/*.jsonl`
- Codex archived sessions: `~/.codex/archived_sessions/*.jsonl`
- Codex thread names: resolved from `~/.codex/session_index.jsonl` when available.
- Claude Code transcripts: `~/.claude/projects/<project-slug>/*.jsonl`. The record
  kind is the top-level `type` (`user`/`assistant`); the role is `message.role`.
  The `list` label is the session's custom title, so a user request like
  "read the 'xxx' session in Claude" maps to the row whose label is `xxx`.

## When To Stop

Ask the user for a specific transcript path if:

- more than one recent session plausibly matches the request,
- the latest session belongs to a different project,
- the transcript format cannot be parsed safely.
