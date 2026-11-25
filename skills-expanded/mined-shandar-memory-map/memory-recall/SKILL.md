---
name: memory-recall
description: >
  Load and summarise the cross-project memory index at the start of a session, or whenever the
  user asks what Claude remembers about their work. Use this skill when the user says things like
  "what do you remember", "what's the context", "what's the current state", "show me the memory
  map", or "what do you know about my projects"; and "where did I/we leave off" or "catch me up"
  only when no project is named and the current folder has no STATUS.md. To restore one project
  from its STATUS.md ("catch me up on [project]", "[project] status"), use memory-map. Also trigger
  proactively at the start of any new conversation if a memory store exists — surface the current
  state and pending items without being asked, so the user does not have to re-orient Claude.
  Pairs with memory-map (which writes memory) and memory-prune (which cleans it). Together they
  form a complete memory loop across Claude sessions.
---

# Memory Recall

Load and intelligently summarise stored memory so a session can pick up exactly where the
last one ended.

Works in **claude.ai** (reads via `memory_user_edits` view) and **Claude Code**
(reads `~/.claude/memory.md`). Detected automatically.

---

## Scope

**Check first (Claude Code).** Before anything else, run `test -f STATUS.md` in the cwd. If it
exists and the request was an open "where did I/we leave off", "catch me up", or "what was I
doing", switch to the memory-map skill in READ mode and stop here.

- No project named and no `STATUS.md` in the cwd → this skill: the cross-project briefing.
- A project is named, or the cwd has a `STATUS.md` → memory-map READ mode restores that project.
- When this skill runs anyway (for example "what do you remember") in a Claude Code folder that
  has a `STATUS.md`, mention it in the briefing so the user can ask for the full project restore.

---

## Step 0 — Detect environment

| Signal | Environment | Load |
|--------|-------------|------|
| `memory_user_edits` tool is available | claude.ai | `references/claude-ai.md` |
| Not available / running in terminal | Claude Code | `references/claude-code.md` |

Read the relevant reference file before proceeding.

---

## Core Protocol

### Step 1 — Read the full memory store

Use the environment-appropriate read command (see references) to fetch all stored entries.

### Step 2 — Sort entries by relevance to the current request

Memory entries fall into priority tiers:

**Tier 1 — Always surface:**
- `CURRENT STATE SNAPSHOT` (what's live, what's imminent)
- Anything tagged "PENDING" or "next" in entries

**Tier 2 — Surface if the user asked for context:**
- Project deliverables, decisions, frameworks
- Recent event details, dates, links

**Tier 3 — Surface only if directly relevant to the immediate query:**
- Historical context, completed work, design tokens
- Personal/operating preferences (PWP, communication style)

### Step 3 — Present the recall

Match the format to the trigger:

**Proactive recall (start of session, no specific question):**

```
Picking up where we left off:

Current state — [from CURRENT STATE SNAPSHOT entry, paraphrased]

Pending items:
→ [item 1]
→ [item 2]
→ [item 3]

Active projects: [list]

Say "show me the full memory map" to see everything stored.
```

**On-demand recall ("what do you remember?"):**

```
Memory map — [N] entries stored

CURRENT STATE
[paraphrase]

PROJECTS
→ [project 1]: [one-line status]
→ [project 2]: [one-line status]

DELIVERABLES
[count] documents, [count] emails, [count] events

PREFERENCES
[note operating style, tools, communication preferences]
```

**Specific recall ("what do you remember about X?"):**

Filter to entries matching X. Present as a focused brief, not a dump.

---

## Hard rules

- Never read sensitive entries aloud unless the user explicitly asked about that topic
- Never invent or extrapolate beyond what's stored — if memory is silent on a topic, say so
- If memory is empty, say it cleanly: *"No stored memory yet. I'll start tracking once we build something together."*
- Don't surface low-tier entries proactively — they create noise
- Always offer the path to "show me everything" rather than dumping all entries by default

---

## Pairs with

- **memory-map** — writes new memory at session close
- **memory-prune** — cleans stale entries when memory gets cluttered

Together: write → recall → prune. The full memory loop.
