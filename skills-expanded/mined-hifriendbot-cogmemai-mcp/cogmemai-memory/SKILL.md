---
name: cogmemai-memory
description: Persistent memory management for Ai coding assistants using CogmemAi. Use when the user mentions "memory", "remember this", "save this for later", "what do you know about", "project context", "session summary", "forget this", "clean up memories", or when starting a new session. Also use when discussing architecture decisions, preferences, bugs, or patterns worth preserving.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [memory, context, mcp, developer-tools, session-management]
---

# CogmemAi Memory Management

CogmemAi gives your Ai assistant persistent memory across sessions. This skill teaches you how to use it effectively — when to save, what to save, and how to keep your memory organized.

## Core Workflow

### Session Start
Always call `get_project_context` before responding to the user's first message. This loads your most important memories from previous sessions. Pass an optional `context` parameter describing the current task for better relevance.

### While Working
Save memories when you learn something important:
- Architecture decisions and tech stack details (importance: 8-10)
- User preferences for coding style, tools, workflow (importance: 7-9)
- Bug fixes, gotchas, and workarounds (importance: 6-8)
- Key file paths and project structure (importance: 7-9)
- Patterns and conventions used in the codebase (importance: 6-8)
- Dependency versions and constraints (importance: 5-7)

### After Significant Exchanges
Use `extract_memories` after important conversations instead of manually saving each fact. It automatically identifies what's worth remembering:
- After debugging a tricky bug — captures the root cause and fix
- After discussing architecture — captures decisions and trade-offs
- After the user explains their preferences — captures all stated preferences
- After a planning session — captures key decisions and constraints

This is faster and more thorough than manual `save_memory` calls for multi-fact exchanges.

### Session End
When the session ends or the user says goodbye, save a session summary capturing what was accomplished, decisions made, and next steps.

## When to Save a Memory

Save immediately when:
- The user tells you a preference ("always use tabs", "never auto-commit")
- You discover an architecture decision ("auth uses JWT", "DB is PostgreSQL 15")
- You fix a bug and the fix is non-obvious
- You learn a project convention ("components use PascalCase", "tests in __tests__/")
- The user makes a decision ("we'll use Redis for caching")

Do NOT save:
- Temporary task details (what you're working on right now)
- Information already in CLAUDE.md or project docs
- Speculative conclusions from reading a single file
- Duplicate information you've already saved

## Importance Scoring Guide

| Score | Use For | Examples |
|-------|---------|---------|
| 9-10 | Core architecture, identity | "This is a Next.js 14 app with App Router", "User is a senior engineer" |
| 7-8 | Key decisions, preferences | "Always use Bun instead of npm", "Auth uses Supabase" |
| 5-6 | Patterns, conventions, bugs | "CSS uses BEM naming", "Login bug was a race condition" |
| 3-4 | Minor context | "Prefers dark mode in VS Code", "Last deployed on Friday" |
| 1-2 | Trivial | Rarely useful — usually not worth saving |

## Memory Types

Choose the right type for better retrieval:

- **identity** — Who the user is, their role, team
- **preference** — Coding style, tool choices, conventions
- **architecture** — System design, tech stack, file structure
- **decision** — Why X was chosen over Y
- **bug** — Known issues, fixes, workarounds
- **dependency** — Version constraints, package notes
- **pattern** — Reusable patterns, conventions
- **context** — General project context
- **session_summary** — What was accomplished in a session
- **task** — Persistent tasks with status and priority tracking
- **correction** — Wrong approach to right approach patterns
- **reminder** — Next-session nudges that auto-expire

## Scoping

- **project** (default) — Specific to this codebase. Architecture, bugs, file paths.
- **global** — Applies everywhere. User preferences, identity, tool choices.

Use `promote_memory` to move a project memory to global scope when you discover it applies universally.

## Workflows

### Project Onboarding
When starting work on a new project for the first time:

1. Call `get_project_context` to check for existing memories
2. If none exist, read the project's README, package.json, or equivalent
3. Use `ingest_document` to extract key facts from documentation
4. Save 3-5 high-importance memories about the tech stack and structure
5. Save the user's stated preferences for this project

### Memory Health Check
Periodically (or when the user asks), review memory quality:

1. Check the `health_score` from `get_project_context` — a 0-100 score showing overall memory health
2. Call `get_analytics` to see usage patterns — it automatically tunes importance and archives stale memories
3. Review "never recalled" memories — delete ones that aren't useful
4. Use `consolidate_memories` to merge related facts into comprehensive summaries
5. Use `link_memories` to connect related facts
6. Use `get_stale_memories` to find outdated memories that need review

### Task Tracking
Use tasks for work that spans multiple sessions:

1. `save_task` to create a task with status (todo, in_progress, done, blocked) and priority
2. `get_tasks` at session start to see what's pending
3. `update_task` as you make progress
4. Tasks persist across sessions and compaction — nothing gets lost

### Corrections and Reminders
- Use `save_correction` when you discover a wrong approach — stores the wrong-to-right pattern so the mistake isn't repeated
- Use `set_reminder` to surface a nudge at the start of the next session (auto-expires after delivery)

### Context Recovery After Compaction
When Claude Code compacts your context (you'll see a summary of the previous conversation):

1. Call `get_project_context` immediately to reload memories
2. Pass the current task as context for better relevance
3. Continue working — your memories bridge the gap

### Searching for Specific Knowledge
When you need to find something specific from past sessions:

1. Use `recall_memories` with a natural language query
2. Filter by `memory_type` or `category` if you know the type
3. Results are intelligently ranked for maximum relevance

## Best Practices

- **Keep memories concise** — Complete sentences, 1-2 lines each. Not paragraphs.
- **Use descriptive subjects** — "auth_system", "database_setup", "css_conventions" — not "note1"
- **Save immediately** — Don't wait until the end of a session. Save as you learn.
- **Use extract_memories for multi-fact exchanges** — When a conversation covers multiple important topics, use `extract_memories` instead of multiple `save_memory` calls. It's faster and catches facts you might miss.
- **Update, don't duplicate** — Use `update_memory` to revise existing memories rather than creating duplicates. The system detects conflicts automatically.
- **Use bulk_update for maintenance** — When cleaning up memory types, categories, or importance scores across many memories, use `bulk_update` instead of individual calls.
- **Use tags** for grouping related memories across types (e.g., tag "auth" on architecture, bug, and decision memories about authentication)

## Common Mistakes

- Setting everything to importance 10 — Reserve 9-10 for core architecture only
- Saving raw code as memory content — Save the *fact*, not the code ("Login component uses useEffect for auth check", not the actual useEffect code)
- Forgetting to call `get_project_context` at session start — This is the single most important action for continuity
- Saving session-specific state — "Currently working on the login bug" will be stale next session
