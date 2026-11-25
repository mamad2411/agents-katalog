---
name: save-context
description: Save the current conversation context as a persistent memory using CogmemAi so it survives compaction, session end, or model handoff. Use when the user says "save context", "save this conversation", "write this down", "don't lose this", "checkpoint", "save state", or when the context window is filling up and important facts may be evicted. Also use proactively before risky tool calls or long-running tasks where losing context would be costly.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [context, save, memory, mcp, session, compaction, developer-tools]
---

# Save Context with CogmemAi

This skill captures the live conversation state into CogmemAi so it survives context compaction, the end of the session, or a switch to a different agent.

## When to Use

Trigger on any of these signals:

- The user says "save context", "save this", "checkpoint", "write this down", "don't forget"
- The context window is approaching its limit and important facts risk being evicted
- About to run a destructive or expensive operation where losing the why would hurt
- A long planning or design discussion just produced decisions worth keeping
- Switching from one phase of work to another (e.g., planning to implementation)

## How to Save Context

Pick the right tool for the volume of information:

### Multi-fact context: `extract_memories`

When the conversation covers several distinct facts (decisions, preferences, constraints, file paths, bugs), call `extract_memories` once. It identifies and saves each fact with the right type, importance, and tags automatically.

Faster and more thorough than calling `save_memory` five times.

### Single fact: `save_memory`

When there's one specific thing to capture, use `save_memory` with:

- `content` — one or two sentences, concrete and self-contained
- `memory_type` — pick from: architecture, decision, preference, bug, dependency, pattern, context, identity, session_summary, task, correction, reminder
- `importance` — 1-10 (see the cogmemai-memory skill for the scoring guide)
- `scope` — `project` (default) or `global` if the fact applies everywhere
- `tags` — short labels for grouping related memories

### End-of-session wrap-up: `save_session_summary`

When wrapping up, call `save_session_summary` to capture what was accomplished, decisions made, and concrete next steps. The next session will see this immediately via `get_project_context`.

## What to Save

Save:

- Architecture and tech stack decisions ("auth uses Supabase", "DB is PostgreSQL 15")
- User preferences ("never auto-commit", "always use Bun instead of npm")
- File paths and project structure that took effort to discover
- Bug fixes with non-obvious root causes
- Patterns and conventions used in the codebase
- Constraints from the user's environment, deadlines, or stakeholders

Do not save:

- The current task you're actively working on (use a task instead via `save_task`)
- Information already in CLAUDE.md or project docs
- Speculation from skimming a single file
- Duplicates of memories you already wrote this session

## Concrete Examples

### Before context compaction

The user has been deep in a debugging session. The conversation is 80k tokens and may compact soon. Call `extract_memories` to preserve the root cause, the fix, and the verification steps so the next session can pick up cleanly.

### After a planning discussion

The user just decided to switch from REST to GraphQL for the new service. Call `save_memory` with:
- `memory_type: "decision"`
- `importance: 9`
- `content: "API for the orders service uses GraphQL (decided 2026-05-13). Why: client needs nested resource fetching in one request to keep mobile latency under 200ms."`

### Switching from planning to implementation

Planning produced 4 decisions, 2 constraints, and a list of file paths to touch. Call `extract_memories` once to capture all of them, then start the implementation phase with the planning context preserved.

## Why This Matters

CogmemAi memories survive everything that can erase your in-context knowledge:

- Context compaction inside the same conversation
- Session end and the next session start
- A handoff to a different model (Opus to Haiku, etc.)
- A new agent in a multi-agent workflow

Saving context is the single highest-leverage action you can take to prevent re-discovery work in the next session.

## Related Skills

- `cogmemai-memory` — full reference for memory management
- `session-start` — load saved context at the start of a session
- `remember-this` — quick save when the user explicitly asks
- `save-bugfix` — specialized save for "we fixed this before" debugging memories
