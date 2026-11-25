---
name: retrospective
description: Self-improving loop — after completing work, sub-agents analyze the conversation to extract signals (corrections, improvised steps, what worked first try, what failed). Proposes updates to project learnings and skill effectiveness. Every session makes the next one better.
invoke_when: Use when running /retro, ending a session naturally, or after completing a significant piece of work. Never runs mid-task — only after work is done.
---

# Retrospective

## Core Principle

**You can't design a skill from nothing. You can only improve after doing work.** Every conversation produces signal — corrections the user made, steps that were improvised, things that worked on first try. The retrospective extracts that signal and turns it into permanent improvements.

## When to Run

- User explicitly runs `/retro`
- After completing a multi-turn feature build
- When the user says something like "that went well" or "that was rough"
- At natural session end (before writing session summary)

**Never interrupt work to run a retrospective.** Wait until the work is done.

## The Retrospective Process

### Phase 1: Extract Signals

Review the entire conversation and categorize every notable moment:

| Signal Type | What to Look For | Example |
|-------------|-----------------|---------|
| **Corrections** | User said "no", "not that", "wrong", "I meant..." | "No, use PostgreSQL not SQLite" |
| **Redone Work** | Something built, then rebuilt differently | Built REST first, user wanted GraphQL |
| **Improvised Steps** | Steps not in any plan that were needed | Had to add CORS middleware — no skill covered it |
| **First-Try Success** | Things that worked immediately, no corrections | TDD flow produced passing tests on first run |
| **Skill Hits** | Which Shipworthy skills were invoked and helped | intent-to-spec caught missing requirements |
| **Skill Misses** | Situations where a skill should have helped but didn't | No skill warned about CORS for frontend+API |
| **User Preferences** | Patterns in how the user wants to work | Prefers explicit confirmation before database changes |
| **Anti-Patterns** | Patterns that caused failures or wasted time | Built with SQLite, had to redo with PostgreSQL |
| **Captured Signals** | Auto-captured events from hooks (`.shipworthy/.session-signals`) | 3 security warnings, 2 dependency additions, 5 commits |

### Phase 1.5: Read Captured Signals

If `.shipworthy/.session-signals` exists, read it. This file contains automatically captured events from hooks during the session — security warnings, dependency additions, git operations, pattern detections, fence violations.

Format: `TIMESTAMP|HOOK|CATEGORY|DETAIL` (one per line)

Group signals by category:
- **security**: Secrets detected, eval usage, .env writes → candidates for regression fence
- **pattern**: console.log, `:any`, missing validation → candidates for regression fence
- **dependency**: New packages added → candidates for architecture spec or learnings
- **git**: Commits, amends, force pushes → context for session summary
- **migration**: Database changes → candidates for learnings
- **fence-violation**: Regression fence rules violated → confirm fence rule is still needed

Use these signals to AUGMENT conversation analysis, not replace it. Signals capture what hooks saw; conversation analysis captures corrections, decisions, and preferences that hooks can't see.

### Phase 2: Map to Skills

For each signal, determine which Shipworthy skill is relevant:

```
Correction: "Don't use console.log" → using-shipworthy (non-negotiable #1)
  - Was the skill invoked? Yes/No
  - Did it prevent the issue? Yes/No
  - If No: Why did it fail? (ignored, not triggered, wrong advice)

Improvised: "Added rate limiting" → No skill covers this adequately
  - Gap identified: rate limiting not in api-design-standards
  - Proposed fix: Add rate limiting section to api-design-standards skill
```

### Phase 3: Propose Changes

Present findings as a reviewable table:

```
## Retrospective Findings

| # | Type | Finding | Proposed Action | Affects |
|---|------|---------|----------------|---------|
| 1 | Correction | User prefers PostgreSQL over SQLite for production | Save to project learnings | .shipworthy/learnings/ |
| 2 | Skill Miss | No CORS guidance when building frontend+API | Add CORS section to api-design-standards | skills/ |
| 3 | First-Try | TDD flow for API endpoints was smooth | No change needed (skill working well) | — |
| 4 | Improvised | Had to set up Docker manually | Consider container-security skill earlier in routing | using-shipworthy |
| 5 | Preference | User wants explicit approval before DB migrations | Save to project learnings | .shipworthy/learnings/ |

Approve all? Or select specific items (e.g., "approve 1, 2, 5"):
```

### Phase 4: Apply Approved Changes

For each approved finding:

**Project Learnings** → Save to `.shipworthy/learnings/[topic].md`:
```markdown
---
description: [One-line summary of what this learning covers — used by INDEX.md for quick scanning]
last_updated: YYYY-MM-DD
---

# [Topic] Learnings

## Preferences
- [What the user/team prefers]

## Patterns That Work
- [What succeeded and should be repeated]

## Patterns That Failed
- [What was tried and didn't work — avoid repeating]
```

The `description` field is critical — it appears in `.shipworthy/INDEX.md` and is the only thing visible when deciding which learning file to read. Make it specific: "Team prefers PostgreSQL with Drizzle ORM" not "Database stuff".

**Skill Updates** → Propose a specific diff to the skill file. Show the exact change. Do NOT auto-apply to skill files — only to learnings files. Skill file changes require explicit confirmation because they affect all future sessions.

**Memory Updates** → If using Claude Code's auto-memory, propose a memory for significant preferences discovered. The retrospective skill works WITH auto-memory, not instead of it:
- Auto-memory captures small corrections in real-time
- Retrospective captures patterns across an entire work session
- Auto-dream consolidates both overnight

**Regression Fence Updates** → When corrections, anti-patterns, or patterns-that-failed are identified (from conversation OR from captured signals), propose adding them to `.shipworthy/regression-fence.md`:

```
## Proposed Regression Fence Entries

| # | Rule | Source | Why |
|---|------|--------|-----|
| 1 | NEVER use SQLite for production in this project | Correction: user switched to PostgreSQL | Concurrent write failures |
| 2 | ALWAYS validate webhook payloads in src/routes/ | Signal: route-no-validation detected 3x | Unvalidated inputs cause 500s |
| 3 | NEVER use console.log in src/api/ — use pino | Signal: console.log detected 5x | Structured logging required |

Add to regression fence? (approve all / select / skip)
```

**Triage rules for fence vs other destinations:**
- **Regression fence** → Mistakes that cost time and would repeat. Imperative format: "NEVER X because Y" or "ALWAYS X because Y". Anchor to file paths when possible.
- **Learnings** → Preferences, patterns that work, decisions. Descriptive format.
- **Auto-memory** → User-level preferences that span all projects (not project-specific).
- **Architecture spec** → Stack constraints, mandatory rules (update via `architecture-awareness`).

When adding to the regression fence:
1. Read existing `.shipworthy/regression-fence.md` (create if it doesn't exist with the header)
2. Check for duplicates — don't add a rule that already exists in different words
3. Count existing entries — if at 20, identify the oldest (by date) for removal
4. Append new entries with today's absolute date (YYYY-MM-DD)
5. Regenerate `.shipworthy/INDEX.md`

### Phase 4.5: Clear Session Signals

After processing signals into learnings, fence entries, and session summary:
- Delete `.shipworthy/.session-signals` — it has been fully processed
- This prevents re-processing the same signals at the next session start
- If the user skipped all proposed entries, still clear the signals (they've been reviewed)

### Phase 5: Update Session Summary

After the retrospective, enhance the session summary (`.shipworthy/sessions/[date].md`) with:
```markdown
## Retrospective
- Signals extracted: [count]
- Corrections: [count]
- Skill hits: [list]
- Skill gaps: [list]
- Learnings saved: [count]
```

### Phase 5.5: Consolidate Memory (when needed)

**Trigger:** Run this phase when `.shipworthy/learnings/` has more than 5 files OR `.shipworthy/sessions/` has more than 10 files. Skip otherwise.

When triggered, offer consolidation to the user:

```
## Memory Consolidation

Your project memory has grown. Proposing cleanup:

| Action | Details |
|--------|---------|
| Merge learnings | [file-a.md] and [file-b.md] cover the same topic → merge into [combined.md] |
| Prune sessions | [N] session files found, keeping 10 most recent, deleting [list] |
| Update stale entries | [file.md] references [function/file] that no longer exists → remove entry |
| Fix relative dates | [file.md] says "last week" → converting to YYYY-MM-DD |

Approve consolidation? (approve all / select items / skip)
```

**Consolidation rules:**
1. **Merge by topic, not by date** — two files about database patterns should become one file, even if written months apart
2. **Preserve the most specific version** — if one file says "use PostgreSQL" and another says "use PostgreSQL with connection pooling via pgBouncer", keep the specific one
3. **Delete entries that contradict current code** — if a learning says "we use Express" but package.json shows Fastify, remove the stale entry
4. **Convert all relative dates to absolute** — "yesterday", "last week", "recently" → YYYY-MM-DD based on the file's modification date
5. **Regenerate INDEX.md** after any consolidation changes

## Learnings Directory Structure

```
.shipworthy/
├── learnings/                    # What this project has taught us
│   ├── database-preferences.md   # "Use PostgreSQL, not SQLite for this project"
│   ├── api-patterns.md           # "Always add CORS, always add rate limiting"
│   ├── deployment-notes.md       # "Docker compose for local, K8s for prod"
│   └── team-conventions.md       # "PR reviews required, squash merge only"
```

## The Flywheel

```
Session 1: Build feature → Hooks capture signals → /retro → Save learnings + fence entries
Session 2: Start work → Auto-retro processes signals → Fence + learnings loaded → Fewer corrections
Session 3: Start work → Rich fence + learnings → Near-zero corrections
...
Session N: One-shot execution. System knows your patterns. Hooks confirm patterns hold.
```

## Rules

1. **Never auto-apply skill changes** — only learnings. Skill changes are proposed, reviewed, and explicitly approved.
2. **Never run mid-work** — retrospectives only happen after work is complete.
3. **Keep learnings concise** — each file under 50 lines. These are patterns, not documentation.
4. **Don't duplicate auto-memory** — if something is already captured by Claude's auto-memory system, reference it instead of duplicating.
5. **Learnings are project-scoped** — they live in `.shipworthy/learnings/` and apply to this project. User-level preferences go to Claude's auto-memory.
6. **Always show the table** — never silently save learnings. The user must see what was learned and approve it.
7. **Dedup before writing** — before creating a new learning file, list existing files in `.shipworthy/learnings/`. If an existing file covers the same topic, update it instead of creating a new one. Two files about the same topic is worse than one well-maintained file.
8. **Always use absolute dates** — write `2026-04-01`, never "today" or "last week". Relative dates become meaningless in future sessions. Use the current date at time of writing.
9. **Regenerate INDEX.md** — after writing, updating, or deleting any file in `.shipworthy/`, regenerate `.shipworthy/INDEX.md` by listing all files with their frontmatter descriptions. This keeps the index fresh for mid-session discovery.
10. **Regression fence entries are imperative** — write "NEVER use SQLite" not "We discovered that SQLite doesn't work well." The fence is loaded as direct commands that survive context decay.
11. **Always read .session-signals** — captured signals are free data from hooks. Don't ignore them just because the conversation also has the information. Signals capture what hooks saw; conversation captures what the user said.
12. **Clear signals after processing** — delete `.shipworthy/.session-signals` after the retrospective completes, even if no entries were approved. The signals have been reviewed.
