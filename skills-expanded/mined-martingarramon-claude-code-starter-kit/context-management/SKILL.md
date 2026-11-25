# Skill: Context Management

## When to Use
Activate when working on long sessions, large codebases, or tasks that risk exceeding
Claude's context window. Also use when starting a new session to efficiently load
relevant context.

## Core Principle
Context is a finite budget. Every token spent on stale context is a token unavailable
for reasoning. Manage context deliberately, not passively.

## Process

### 1. Session Start Protocol
Before doing anything in a new session:
- Read `memory/MEMORY.md` for current state and priorities
- Read `CLAUDE.md` for rules (this happens automatically)
- Check if any files referenced in memory have changed
- State what you know and what you need to learn before starting work

### 2. Progressive Context Loading
Don't read everything upfront. Load context as needed.
- Start with the files directly relevant to the current task
- Read adjacent files only when you hit a reference or dependency
- For large files, read the section you need, not the whole file
- Summarize what you've read to confirm understanding before proceeding

### 3. Context Bloat Detection
Watch for these signals that context is getting too large:
- You've read more than 10 files this session
- Responses are getting slower or less focused
- You're re-reading files you read earlier
- The conversation has been going for 30+ turns

### 4. Context Recovery Actions
When context is bloating:
- Summarize progress so far in 5-10 lines
- Write intermediate results to files instead of keeping them in conversation
- Use `/compact` if available to compress conversation history
- For parallel research, use subagents to isolate context

### 5. Memory Updates
At natural breakpoints (task complete, decision made, session ending):
- Update `memory/MEMORY.md` with new decisions and status
- Remove stale entries that are no longer true
- Add any new patterns learned to the Patterns section
- Keep memory under 80 lines total

## Anti-Patterns
- **Front-loading everything:** Reading 20 files before doing anything
- **Never updating memory:** Treating memory as read-only
- **Ignoring bloat signals:** Continuing a degraded session instead of compacting
- **Duplicate context:** Re-reading files already in the conversation
- **Storing temporary state in memory:** Debug notes and one-off observations don't belong

## Rules
- Memory is state, not a diary. Store facts, not narratives.
- When in doubt about context freshness, re-read the file. Stale assumptions cause bugs.
- If a session exceeds 40 turns, summarize and compact before continuing.
