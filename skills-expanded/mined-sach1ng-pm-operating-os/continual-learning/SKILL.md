---
name: continual-learning
description: "Mine chat transcripts for decisions, exec updates, strategy shifts, feedback themes, and user preferences. Write structured entries to memory/, then update AGENTS.md with curated preferences and facts. Cursor-first ingestion pipeline."
---

# Continual Learning

Ingestion pipeline for PM-OS memory. Reads chat transcripts, classifies what it finds, writes structured entries to `memory/`, and updates `AGENTS.md` with curated preferences and facts. Cursor-first.

## When to Use

- "Run continual learning" / "mine my chats" / "update memory"
- On a schedule (e.g. end of week) to keep memory current
- After a batch of important conversations (strategy sessions, PRD reviews, planning)

## Inputs

- **Transcript root:** `~/.cursor/projects/<workspace-slug>/agent-transcripts/`
- **Existing memory:** `AGENTS.md` + `memory/` subdirectories
- **Incremental index:** `.cursor/hooks/state/continual-learning-index.json`

## Workflow

### 1. Load state

1. Read existing `AGENTS.md`.
2. Load incremental index (if present).
3. Discover transcript files. Process only:
   - new files not in the index, or
   - files whose mtime is newer than the indexed mtime.

### 2. Extract and classify

For each new/changed transcript, extract high-signal items and classify each into one of these categories:

| Category | What to look for | Write to |
|----------|-----------------|----------|
| **Decision** | User made or confirmed a product decision (PRD approval, scope change, launch/kill, prioritization shift, stakeholder alignment) | `memory/decisions/` |
| **Exec update** | User drafted or discussed an executive status update, SLT summary, or program update | `memory/exec-updates/` |
| **Strategy shift** | User discussed or changed strategic direction, pillars, positioning, or goals | `memory/strategy-reviews/` |
| **Feedback insight** | User analyzed customer feedback, VOC themes, or support trends | `memory/feedback/` |
| **User preference** | Recurring correction or stated broad rule about how the AI should behave | `AGENTS.md` → Learned User Preferences |
| **Workspace fact** | Durable fact about the workspace, tools, file paths, or workflows | `AGENTS.md` → Learned Workspace Facts |

**Skip:** one-off task instructions, transient details (branch names, commit hashes, temp errors), secrets/tokens/credentials, and anything not actionable in future sessions.

### 3. Write to memory

For each extracted item (except preferences/facts), write a structured entry to the appropriate `memory/` subdirectory:

**Decisions** → `memory/decisions/YYYY-MM-DD_short-slug.md`

```markdown
# [Decision title]

**Date:** YYYY-MM-DD
**Source:** continual-learning (transcript extraction)
**Type:** [PRD approval | Scope change | Launch/Kill | Prioritization | Alignment | Other]

## Decision
[1-2 sentences: what was decided]

## Context
[What prompted this]

## Alternatives Considered
[If discussed in transcript, otherwise omit]
```

**Exec updates** → `memory/exec-updates/YYYY-MM-DD.md`

```markdown
# Exec Update — YYYY-MM-DD

**Source:** continual-learning (transcript extraction)

## Summary
[Key points from the update]
```

**Strategy shifts** → `memory/strategy-reviews/YYYY-MM-DD_topic.md`

```markdown
# Strategy: [topic]

**Date:** YYYY-MM-DD
**Source:** continual-learning (transcript extraction)

## What changed
[Description of the shift]

## Rationale
[Why, if discussed]
```

**Feedback insights** → `memory/feedback/YYYY-MM-DD.md`

```markdown
# Feedback Insights — YYYY-MM-DD

**Source:** continual-learning (transcript extraction)

## Themes
[Themes identified]
```

Also write a log entry to `memory/learning-log/YYYY-MM-DD.md`:

```markdown
# Continual Learning Run — YYYY-MM-DD

**Transcripts processed:** [count]
**Items extracted:** [count by category]

## Items written
- [category] → [path]: [1-line summary]
```

### 4. Update AGENTS.md

After writing to memory, update the Learned sections in `AGENTS.md`:

- **Learned User Preferences** — recurring corrections, stated broad rules
- **Learned Workspace Facts** — durable facts about workspace, tools, workflows

Rules:
- Update matching bullets in place (don't duplicate)
- Add only net-new bullets
- Deduplicate semantically similar bullets
- Max 12 bullets per section
- Plain bullet points only — no evidence tags, no metadata

### 5. Write back index

Update `.cursor/hooks/state/continual-learning-index.json`:
- Store latest mtimes for all processed files
- Remove entries for files that no longer exist on disk

## Inclusion bar

Keep an item only if all are true:

- Actionable in future sessions
- Stable across sessions
- Repeated in multiple transcripts, or explicitly stated as a broad rule
- Non-sensitive

## Exclusions

Never store:

- Secrets, tokens, credentials, private personal data
- One-off task instructions
- Transient details (branch names, commit hashes, temporary errors)

## Incremental Index Format

```json
{
  "version": 1,
  "transcripts": {
    "/abs/path/to/file.jsonl": {
      "mtimeMs": 1730000000000,
      "lastProcessedAt": "2026-02-18T12:00:00.000Z"
    }
  }
}
```
