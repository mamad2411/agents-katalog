<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: session-tracker
description: >
  Session context tracking with OMC state bridge. Triggers automatically at session
  start or on "마지막 세션", "이전 작업", "어디까지 했지", "last session", "continue
  where I left off", "resume work" and similar. v3: Dual-writes to both OMC
  state (notepad/project-memory) and OpenClaw-CC persistent memory. Uses
  session-manager agent for cross-system continuity. Hooks auto-save on
  PreCompact and Stop events.
---

# Session Tracker — Cross-Session Continuity Skill

## Preamble

Before executing this skill:

1. **Load context from memory**:
   ```
   memory_search(query: "{skill-relevant-query}", associative: true, limit: 5)
   memory_search(tag: "{skill-name}", limit: 3)
   ```
   Review returned memories for relevant past context, decisions, and patterns.

2. **Check OMC state for active work**:
   ```
   state_get_status()
   ```
   If conflicting active tasks exist, warn the user before proceeding.

3. **Detect current branch** (for git-related skills):
   ```bash
   git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not-a-git-repo"
   ```

4. **Check proactive mode**:
   ```
   state_read("occ-proactive")
   ```
   If `"false"`: do NOT proactively suggest other OpenClaw-CC skills during this session.
   Only run skills the user explicitly invokes.

5. **Log skill activation**:
   ```
   memory_daily_log(type: "note", entry: "Skill activated: /{skill-name}")
   ```

## Role

Maintain session continuity across Claude Code conversations. Load previous
session context at start, track current session progress, and save session
summary at end.

## Session Start Workflow

### Step 1 — Load Previous Context

## Memory Context Loading

Before starting work, load relevant context from the 3-layer memory system:

```
# Search for related past work
memory_search(query: "{task description}", associative: true, limit: 5)

# Search by relevant tags
memory_search(tag: "{relevant-tag}", limit: 3)

# Check for recent related daily logs
memory_search_date(start: "{7 days ago}", end: "{today}", category: "daily-logs", limit: 5)
```

**Use retrieved context to**:
- Avoid repeating past mistakes
- Build on previous decisions
- Maintain consistency with established patterns
- Reference related knowledge graph nodes

If critical related memories exist, summarize them before proceeding:
```
Found {N} related memories:
- {memory_1 title}: {brief relevance}
- {memory_2 title}: {brief relevance}
```

```
memory_search(category: "sessions", limit: 1) → Most recent session
memory_get(id: last_session_id) → Full session details
```

### Step 2 — Display Context

```markdown
## Previous Session Summary
**Date**: {date}
**Duration**: {approximate}
**Key Work**: {summary}

### Unfinished Items
- [ ] {todo_1}
- [ ] {todo_2}

### Key Decisions Made
- {decision_1}
- {decision_2}

Ready to continue or start new work?
```

### Step 3 — Initialize Current Session

```
memory_store:
  category: "sessions"
  title: "Session {YYYY-MM-DD HH:MM}"
  content: "Session started. Previous context loaded from session #{prev_id}."
  tags: ["session", "{date}"]
  importance: 3
```

## During Session

### Auto-Track Events

Track these automatically during the session:

| Event | Action |
|-------|--------|
| Important decision | `memory_update(mode: "append", content: "Decision: ...")` |
| Task completion | `memory_update(mode: "append", content: "Completed: ...")` |
| Blocker encountered | `memory_update(mode: "append", content: "Blocked: ...")` |
| File created/modified | `memory_update(mode: "append", content: "Modified: ...")` |

### Periodic Checkpoint

Every 10-15 significant interactions, save a checkpoint:

```
memory_update(id: current_session_id, mode: "append",
  content: "Checkpoint: {summary of recent work}")
```

## Session End Workflow

### Step 1 — Generate Summary

Compile all tracked events into a session summary.

### Step 2 — Save & Log

## Memory Persistence

After completing the workflow, persist results to the 3-layer memory system:

### Required Actions

1. **Log completion to daily log**:
   ```
   memory_daily_log(type: "done", entry: "{skill-name}: {brief result summary}")
   ```

2. **Store significant findings** (importance ≥ 6):
   ```
   memory_store(
     category: "{appropriate category}",
     title: "{descriptive title}",
     content: "{structured result content}",
     tags: ["{skill-name}", "{project}", "{relevant-tags}"],
     importance: {6-10 based on significance}
   )
   ```

3. **Link to related memories** (if applicable):
   ```
   memory_link(source: "{new_memory_id}", target: "{related_id}", relation: "{related|derived|refines}")
   ```

### Category Routing

| Content Type | Category | Subcategory |
|-------------|----------|-------------|
| Bug fix / debugging | knowledge | debugging |
| Code review results | projects | {project-name} |
| Design decisions | projects | {project-name} |
| Research findings | knowledge | {topic} |
| Release / deploy | projects | {project-name} |
| Person-related info | people | — |
| Task / action item | tasks | — |

```
memory_update(id: current_session_id, mode: "replace",
  content: "{complete session summary with todos}")
memory_daily_log(entry: "Session completed: {one-line summary}", type: "done")
```

### Step 3 — Identify Carryover

List unfinished items for the next session:

```markdown
## Session Complete

### Accomplished
- {item_1}
- {item_2}

### Carry Forward
- [ ] {unfinished_1}
- [ ] {unfinished_2}

Session saved as memory #{id}.
```

## Session Memory Structure

```
sessions/
├── Session 2026-03-20 09:00.md
├── Session 2026-03-20 14:30.md
└── Session 2026-03-21 10:00.md
```

Each session file contains:
- Start time and previous session reference
- Chronological event log
- Decisions and rationale
- Files modified
- Unfinished items
- End summary

## Completion Status Protocol

Every skill must end with one of these status codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| **DONE** | All steps completed, evidence provided | Root cause found + fix verified, PR created, review finished |
| **DONE_WITH_CONCERNS** | Completed with warnings or caveats | Tests pass but coverage dropped, fix applied but can't fully verify |
| **BLOCKED** | Cannot proceed, requires user intervention | 3 failed attempts, missing permissions, external dependency down |
| **NEEDS_CONTEXT** | Missing information to continue | Unclear requirements, need user clarification |

### Escalation Rules

1. **3-strike rule**: After 3 failed attempts at any step, **STOP** and escalate to user.
   Do not continue guessing. Present what was tried and ask for direction.

2. **Scope escalation**: If fix/change touches 5+ files unexpectedly, pause and confirm
   with the user before proceeding.

3. **Security uncertainty**: If you are unsure about a security implication, **STOP** and
   escalate. Never guess on security.

4. **Verification requirement**: Never claim DONE without evidence.
   - "Should work" → RUN IT. Confidence is not evidence.
   - "Already tested earlier" → Code changed since. Test again.
   - "Trivial change" → Trivial changes break production.

### Output Format

```
═══════════════════════════════════════
Status: {DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT}
Summary: {one-line description of outcome}
Evidence: {test output, verification results, or blocking reason}
═══════════════════════════════════════
```
