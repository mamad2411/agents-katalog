---
name: knowledge-organization
description: Organize project rules vs skills vs memory for
version: 0.1.0
author: Hermes
---

# Knowledge Organization for Hermes Agents

Maintain three separate stores for persistent knowledge, each with a distinct purpose and lifecycle. A rule belongs in exactly ONE store — putting it in the wrong place either makes it invisible to future sessions or turns it into a stale constraint.

## When to Use

- User gives a project-level rule ("always reorder by date after changing dates")
- User corrects where you stored information ("put that in AGENTS.md, not memory")
- Memory is running out of space and needs compaction
- You need to decide whether a fact belongs in AGENTS.md, a skill, or memory

## The Three Stores

| Store | Purpose | Scope | Examples |
|-------|---------|-------|---------|
| **AGENTS.md** | Project rules & conventions | Per-repo | Git discipline, formatting rules, sort order, build commands |
| **Skills** | Reusable workflows | Class of task | Resume editing workflow, MCP server setup, bug triage pattern |
| **Memory** | Personal facts & env quirks | Cross-session | User preferences, phone numbers, project-specific environment details |

## Construction Rules

### AGENTS.md (project rules)
- Written to the project root README or AGENTS.md
- Covers: commit discipline, directory structure, build commands, sort rules
- Source of truth: a user telling you a rule about their project → AGENTS.md
- Do NOT duplicate AGENTS.md rules in personal memory — they expire or drift

### Skills (procedural knowledge)
- Written via `skill_manage(action='create')`
- Covers: HOW to do a class of task (steps, commands, pitfalls)
- Named at the class level, never after a specific bug/feature/task
- Updated when the user corrects your approach in that class of task

### Memory (personal context)
- Written via the `memory` tool
- Covers: user identity, preferences, environment facts, project-specific URLs and credentials
- NOT for procedure or project rules
- Consolidated regularly: remove superseded entries, shorten verbose ones, reorder by importance

## Pitfalls

- **Do NOT put project rules in memory**: when the project evolves, memory either drifts or gets full. AGENTS.md is version-controlled and visible to every session that enters the repo.
- **Do NOT put session-specific task logs in memory**: use `session_search` to recall what happened in a past conversation. Memory is for durable facts, not progress tracking.
- **Memory priority order**: user preferences and corrections → environment facts → stable conventions. Least important entries get removed first during compaction.
- **One store, one purpose**: a single piece of information belongs in exactly one store. If a skill references a project rule, the skill says "see AGENTS.md", not "copy the rule here".

## Consolidation Checklist

When memory is at 85%+ capacity:
1. Remove entries superseded by AGENTS.md or skills
2. Remove session-specific task logs
3. Remove stale environment facts (broken tools, dead-ends)
4. Shorten verbose entries to essential facts
5. Re-rank by: user correction > identity/credential > env fact > convention
