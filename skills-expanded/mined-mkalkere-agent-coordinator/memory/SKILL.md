---
name: memory
version: 1.0.0
description: Persist and recall context across sessions — critical for continuity
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - memory:read
    - memory:write
  requires_approval: false
---

# Memory

Persist and recall context across sessions. Memory is how agents maintain continuity — without it, every session starts from zero.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `memory_store` or `memory_retrieve` is invoked, the executor reads from or writes to the agent's memory directory (`.os/agents/{name}/memory/` for L1, `.os/memory/shared/` for L2). The tool schema in tool.yaml defines the external contract; the executor handles file I/O directly.

## When to Use

- **Session start**: Load context from previous sessions (required)
- **During work**: Save decisions, learnings, and discoveries as they happen
- **Before session end**: Write summary of what was accomplished (critical)
- **When asked to remember**: Explicitly requested by user or another agent
- **After mistakes**: Record what went wrong and how to avoid it

## Methodology

### 1. Session Start — Load Context

At the start of every session, load memory in this order:
1. Read `memory/INDEX.md` — tells you what exists and what to load
2. Read `memory/DURABLE.md` — long-term decisions and preferences
3. Read today's daily log (`memory/daily/YYYY-MM-DD.md`)
4. Read yesterday's daily log for recent context

### 2. During Work — Save Proactively

Save memories **before you lose them**. Don't wait until session end.

**Always save (to daily log):**
- Decisions made and why
- Problems encountered and solutions
- User feedback or corrections
- New patterns discovered
- Files created or modified

**Save to DURABLE.md:**
- User preferences that apply to all sessions
- Architectural decisions
- Patterns that should always be followed
- Anti-patterns to avoid

### 3. Memory Types

| Type | Use For | Example |
|------|---------|---------|
| **Episodic** | Events, what happened | "PR #23 was rejected due to SQL injection" |
| **Semantic** | Facts, knowledge | "This project uses pytest with fixtures" |
| **Procedural** | How-to, processes | "To deploy: run make build then make deploy" |

### 4. Memory Levels

| Level | Location | Visibility | Use For |
|-------|----------|-----------|---------|
| **L1** | `.os/agents/{name}/memory/` | Agent-private | Working notes, task context |
| **L2** | `.os/memory/shared/` | All agents | Project conventions, shared decisions |

### 5. Session End — Write Summary

Before session ends, update the daily log with:
- What was accomplished
- Key decisions made
- Learnings and insights
- Files changed
- What's pending for next session

## Output Format

```
## Memory Operation

### Store
- Type: [episodic/semantic/procedural]
- Level: [L1/L2]
- Tags: [tag list]
- Content: [summary of what was stored]

### Retrieve
- Query: [search query]
- Results: [N matches found]
- Most relevant: [summary of top result]
```

## Quality Criteria

- Context is loaded at session start (not skipped)
- Decisions are saved with reasoning (not just the decision)
- Memories are tagged for easy retrieval
- Daily log is updated before session ends
- Durable memory contains only long-term knowledge
- Sensitive data (credentials, secrets) is never stored in memory
- Memory is concise — key information, not verbose transcripts

## Common Mistakes

- **Not saving before context loss**: Context compaction or session end can erase everything. Save proactively when context feels full, when major decisions are made, or when switching tasks.
- **Saving too much**: Storing every detail creates noise that drowns out important information. Save decisions, learnings, and patterns — not implementation details (code is the source of truth).
- **Not loading at session start**: Starting a session without reading memory means losing all accumulated knowledge. Always load INDEX.md first.
- **Wrong memory level**: Storing project-wide conventions in L1 (agent-private) means other agents can't see them. Use L2 for shared knowledge.
- **Missing tags**: Memories without tags are hard to retrieve. Always add relevant tags for future search.
- **Storing secrets**: Never store API keys, passwords, or tokens in memory files. They persist on disk and may be shared.

## Completion

A memory operation is complete when:
- Store: Content is written to the correct location with appropriate type, level, and tags
- Retrieve: Relevant memories are found and returned, or no matches are reported
- Session end: Daily log is updated and durable memory reflects any new long-term knowledge
