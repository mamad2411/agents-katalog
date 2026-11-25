---
name: agent-memory
description: Persistent memory system for AI coding agents. Use when you need to save facts about the user, store interaction preferences, log session events, or search previously saved memories. Triggers on remembering, saving context, recalling past decisions, or when the user says "remember this". Also use proactively when the user shares personal info, project context, or preferences worth persisting across sessions.
---

# Agent Memory

Persistent, structured memory for AI coding agents. A local SQLite database with semantic search that gives your agent long-term recall across sessions: facts about people and projects, learned interaction preferences, and daily session logs.

All agents on the machine share one database at `~/.agent-memory/memory.db`. Whatever one agent learns, every other agent knows.

## How It Works

Three layers:

1. **Hook** — `mem-context-hook` fires before every message, injects a `=== MEMORY CONTEXT ===` block with tiered disclosure: soul + user_info + preferences in full, everything else as a compact index. Use `mem query` to fetch full content from the index.
2. **CLI** — `mem` with subcommands that agents call to read and write memory
3. **Database** — `~/.agent-memory/memory.db` with four tables: facts, soul, daily_logs, embeddings

## CLI Quick Reference

```
mem fact <category> <subject> "<content>" [--desc "<description>"]  Save/update a fact (auto-embeds)
mem soul <aspect> "<content>"                                      Save/update an interaction preference
mem log "<note>"                                                   Append to today's session log
mem search "<query>"                                               Semantic search (keyword fallback)
mem query "<sql>"                                                  Raw SQLite query
mem status                                                         Show database stats
mem export                                                         Export all data as JSON
```

The `--desc` flag provides a short one-liner (under 80 chars) shown in the memory context index. Without it, the hook truncates content to 80 chars.

## Cookbook

Each operation has a detailed guide. **Read the relevant cookbook file before executing.**

| Task | Cookbook | Use When |
|------|---------|----------|
| Install | [cookbook/install.md](cookbook/install.md) | First-time setup, `mem` not found, new machine |
| Save | [cookbook/saving.md](cookbook/saving.md) | Deciding what/when/how to save facts, soul, or logs |
| Search | [cookbook/searching.md](cookbook/searching.md) | Finding previously saved information |
| Rules | [cookbook/rules.md](cookbook/rules.md) | Understanding constraints and best practices |

**When saving or searching memory, read the matching cookbook file first, then act.**

## Quick Decision Tree

```
User shares personal info, people, project context, or preferences?
  → Read cookbook/saving.md, save as fact or soul

User corrects your behavior or expresses a working preference?
  → Read cookbook/saving.md, save as soul

Significant event happens (task complete, decision made)?
  → mem log "<what happened>"

Need to recall something from a past session?
  → Read cookbook/searching.md, search first before asking the user

mem command not found?
  → Read cookbook/install.md, install from scratch
```

## Self-Improvement

This skill improves through observation. After each usage:

### Recording Observations

Edit `observations.json` in this skill folder and append to the `observations` array:

**Success:**
```json
{
  "id": <next_id>,
  "timestamp": "<ISO 8601>",
  "action": "fact|search|soul|log",
  "task": "what you tried to do",
  "success": true,
  "error": null,
  "context": "what triggered this",
  "user_feedback": null
}
```

**Failure:**
```json
{
  "id": <next_id>,
  "timestamp": "<ISO 8601>",
  "action": "fact|search|soul|log",
  "task": "what you tried to do",
  "success": false,
  "error": "what went wrong",
  "context": "what triggered this",
  "user_feedback": "any correction from user"
}
```

### Analyzing Observations

Read `observations.json` and look for patterns:
- Recurring errors (same mistake multiple times)
- Related user feedback (same correction repeatedly)
- Confusion themes (similar struggles across agents)

### Proposing Amendments

When you find a pattern (≥3 related observations), propose an improvement:

Edit `amendments.json` and append to the `amendments` array:

```json
{
  "id": <next_id>,
  "timestamp": "<ISO 8601>",
  "status": "proposed",
  "observation_ids": [<list of relevant observation IDs>],
  "section": "which part of SKILL.md",
  "current_instruction": "the current text",
  "proposed_instruction": "your improved text",
  "rationale": "why this change will help",
  "evidence": "which observations support this"
}
```

### Applying Amendments

When user approves a proposal:

1. **Edit SKILL.md** - Apply the proposed change
2. **Update amendment status** in `amendments.json`:
   ```json
   {
     "status": "applied",
     "applied_at": "<ISO 8601>"
   }
   ```
3. **Add version entry** to `amendments.json`:
   ```json
   {
     "version": "<increment>",
     "date": "<date>",
     "summary": "<what changed>",
     "amendment_id": <id>
   }
   ```

### Review Process

**View pending proposals:**
- Read `amendments.json`
- Filter for `status: "proposed"`

**View version history:**
- Read `amendments.json`
- Check `version_history` array

**View recent issues:**
- Read `observations.json`
- Filter for `success: false`

### Cookbook

Read [cookbook/self-improvement.md](cookbook/self-improvement.md) for detailed guidance on the observation and improvement cycle.
