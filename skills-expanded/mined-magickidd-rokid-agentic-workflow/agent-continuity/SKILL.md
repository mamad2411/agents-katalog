---
name: agent-continuity
description: Use when starting or resuming a non-trivial Codex/Cursor/Claude task, especially long-running design, coding, testing, handoff, or multi-agent work. Performs a lightweight new-session continuity check, finds or creates a task ledger, and prevents stale-file assumptions without forcing per-action checks.
---

# Agent Continuity

Use this skill at the start of a new conversation or when resuming a task that may outlive the current context.

## Default Mode

Use the lightweight session check by default. Do not run strict freshness checks before every action unless the task is high-risk or multiple agents are actively editing the same files.

## Session Start

1. Read the active project instructions (`AGENTS.md`, `CLAUDE.md`, or `.cursor/rules/*.mdc`) when present.
2. Run a quick status check:
   ```bash
   python ~/.codex/skills/agent-continuity/scripts/session_check.py --root .
   ```
3. If the task is non-trivial, find or create a ledger under `Docs/AgentWork/`.
4. Before first editing a target file in this session, reread that file from disk.
5. If the file changed since the ledger's last record, reconcile the latest content before editing.

## Task Ledger

Create a ledger for tasks that are long-running, cross-file, design-heavy, multi-agent, or explicitly requested by the user.

Default path:

```text
Docs/AgentWork/<task-slug>-<YYYY-MM-DD>.md
```

Minimum sections:

```markdown
# <Task Name> - Agent Task Ledger

> Status: in-progress
> Created:
> Last updated:
> Agents:

## Goal

## Current State
- Phase:
- Next step:

## Confirmed Facts

## Decisions
| Time | Decision | Reason | Scope |
|---|---|---|---|

## Files
| Time | File | Action | Notes |
|---|---|---|---|

## Changes
| Time | Change | Files | Verification |
|---|---|---|---|

## Open Items
- [ ]

## Handoff
```

## Update Rules

- Update the ledger after meaningful decisions, code changes, verification results, blockers, or handoff points.
- Keep entries short and factual. Do not copy the whole conversation.
- Replace outdated current-state text instead of appending conflicting versions.
- If another agent changed the same file, treat the latest file content and git status as the source of truth.

## Handoff

Before pausing, switching agents, or finishing a partial task, write:

- current goal
- completed work
- files changed
- verification run
- known risks
- next step

## Installation

Codex:

```bash
ln -s ~/.codex/vendor_imports/skills/<vendor-skills-repo>/agent-continuity ~/.codex/skills/agent-continuity
cp ~/.codex/vendor_imports/skills/<vendor-skills-repo>/_global_rules/agent-continuity-protocol.mdc ~/.codex/rules/
```

Cursor:

```bash
cp ~/.cursor/skills/_global_rules/agent-continuity-protocol.mdc ~/.cursor/rules/
```
