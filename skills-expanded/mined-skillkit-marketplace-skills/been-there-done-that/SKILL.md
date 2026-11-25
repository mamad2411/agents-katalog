---
name: been-there-done-that
description: >
  Guides an agent to document developer progress objectively after completing
  a sprint, project phase, or milestone. Reads a global markdown file,
  detects git work sessions via 3-day gap analysis, writes factual entries
  (no sycophancy, no praise), and performs cross-entry progression analysis
  for portfolio and gig use.

  USE WHEN: User says "document my progress", "log what I did", "I just finished
  [sprint/project/phase]", "update btdt", or provides a repo path after completing work.

  WORKFLOW: Pre-flight → Session Detection → Collection → Analysis → Write → Confirm

  OUTPUT: Extends the user's global progress log (been-there-done-that.md) with a dated, factual entry
  placed at the correct position in a Year/Month/Date/Project tree.
  Default output language: English (ask user on first run if file is new).

  CRITICAL: Agent MUST stop and wait at every STOP gate. Do not proceed without
  explicit user confirmation. No assumptions. No skipping.
category: productivity
---

# Been There Done That

## Overview

This skill turns a finished sprint or project phase into a permanent, objective
record. It is not a celebration tool — it is a factual ledger of what was built,
what capability was gained, what blocked progress, and what shipped.

Entries are stored in a single global progress log file (named been-there-done-that.md by convention), organized
as a chronological tree. Over time, cross-entry analysis surfaces patterns:
recurring blockers, emerging domain depth, and portfolio-ready evidence statements.

---

## Workflow Decision Tree

```
User triggers skill
       │
       ▼
[Pre-Flight Check]  ──── missing info? ──→  STOP → ask user
       │
       ▼
[Phase 0: Session Detection]
  - Run git log on repo
  - Apply 3-day gap rule to find sessions
  - Infer clean project name from repo/remote
  ──── present sessions ──→  STOP-0 → user picks session + confirms name
       │
       ▼
[Phase 1: Auto-Draft + Confirm]
  - Read: commit messages, git diff, changed files list
  - Draft all 4 answers from git artifacts automatically
  - MODE FIRST: show draft with verbose explanation
  - MODE RETURNING: show draft with last entry as reference
  ──── show draft for all 4 fields ──→  STOP-1 → user confirms or corrects
       │
       ▼
[Phase 2: Analysis]  (skip if file has 0 entries)
  - Compare new entry to existing entries
  - Detect: new tech, recurring blockers, complexity escalation
  ──── show brief analysis ──→  STOP-2 → user confirms accuracy
       │
       ▼
[Phase 3: Place & Write]
  - Compute tree position from session.end date
  - Generate entry (factual, no praise)
  - Show preview
  ──── show preview ──→  STOP-3 → user approves
       │
       ▼
[Phase 4: Done]
  - Write/extend file at correct tree position
  - Confirm success
```

---

## Pre-Flight Check

Run these checks before any git commands. STOP on each unresolved item.

**CHECK 1 — Repo path**
```
Is a repo path provided OR is agent currently inside a git directory?
  YES → use it
  NO  → ask: "Which repo did you just finish working on? Provide path."
  → STOP until resolved.
```

**CHECK 2 — Global file**
```
BEFORE asking the user anything, search these locations in order:

  LOOKUP SEQUENCE (stop at first match):
    1. Any path explicitly provided by user in current message
    2. $CLAUDE_BTDT_PATH environment variable (if set)
    3. ~/.claude/been-there-done-that.md          ← primary default
    4. ~/been-there-done-that.md
    5. ~/Documents/been-there-done-that.md
    6. ~/notes/been-there-done-that.md
    7. <repo_path>/been-there-done-that.md

  IF FOUND at any location:
    → Read it immediately. Parse tree. Note last entry date.
    → Do NOT ask user about file location. Continue to CHECK 3.

  IF NOT FOUND anywhere:
    → Ask once: "No been-there-done-that.md found.
                 Default location: ~/.claude/been-there-done-that.md
                 Press Enter to confirm, or type a different path."
    → STOP until resolved.
```

**CHECK 3 — Language (first-run only, if file does not exist)**
```
  Ask: "What language should entries be written in? (default: English)"
  → Record answer. Do not ask again.
```

---

## Phase 0: Session Detection

### Extract git data

```bash
# All commits: timestamp | hash | message (newest first)
git -C <repo_path> log --format="%at|%H|%s" 2>/dev/null

# Remote URL (for project name inference)
git -C <repo_path> remote get-url origin 2>/dev/null

# Current branch
git -C <repo_path> branch --show-current 2>/dev/null

# File change stats for selected session range
git -C <repo_path> diff --stat <oldest_hash>..<newest_hash> 2>/dev/null
```

### Apply 3-day gap rule

Parse timestamps. A **session boundary** exists when:
```
gap between consecutive commits > 259200 seconds (3 days)
```

For each session compute:
```
session.id       = sequential letter, OLDEST FIRST
                   A = oldest session, last letter = most recent session
session.start    = earliest commit date in group (ISO 8601)
session.end      = latest commit date in group
session.commits  = count
session.messages = list of commit subjects (for context display)
```

CRITICAL — label assignment:
  git log outputs newest commits FIRST. Reverse the list before assigning letters.
  A = chronologically first session (oldest work)
  Last letter = most recent session (what user most likely just finished)
  Always mark the most recent with "← most recent"

### Infer project name

```
1. Take: folder name OR last path segment of git remote URL
2. Strip prefixes: frontend- backend- api- service- mobile- web- app-
3. Strip suffixes: -main -dev -staging -master -prod -v1 -v2 -branch
4. Title-case remainder

Examples:
  "frontend-fstrack-tractor-dev"  →  "FSTrack Tractor"
  "yagura"                        →  "Yagura"
  "PT-GGF-internal-app-v2"       →  "Internal App"  ← flag as ambiguous
```

### STOP-0 (Mandatory)

```
🔍 Repo detected: <raw_name>
📁 File: <path> (exists with N entries | will be created)

Work sessions detected (oldest first):

  [A] Nov 12 – Nov 15, 2025  (8 commits)
      Commits: "initial setup", ...
  [B] Jan 28 – Feb 20, 2026  (23 commits)  ← most recent
      Commits: "fix auth flow", "add realtime", ...

Which session did you just finish? (default: most recent = B) [A/B/...]
Project name → "<clean_name>"  — confirm or type a new name:
```

**→ STOP. Do not proceed until user responds.**

---

## Phase 1: Auto-Draft + Confirm

**Agent reads the repo first. Never ask blank questions.**

### Step 1.1 — Read git artifacts for the selected session

```bash
# Full diff stat for the session range
git -C <repo_path> diff --stat <session.oldest_hash>..<session.newest_hash> 2>/dev/null

# Commit messages in the session (oldest to newest)
git -C <repo_path> log --reverse --format="%s" <session.oldest_hash>^..<session.newest_hash> 2>/dev/null

# Files changed, for stack inference
git -C <repo_path> diff --name-only <session.oldest_hash>..<session.newest_hash> 2>/dev/null

# README or main entry file if present (cap at 100 lines)
head -100 <repo_path>/README.md 2>/dev/null
```

### Step 1.2 — Auto-draft all 4 fields

Using commit messages, diff stats, and file list — draft answers WITHOUT asking.

**Drafting rules per field:**

```
FIELD 1 — WHAT WAS DONE:
  Source: commit messages (group by theme) + diff stat summary
  Pattern: "[verb] [system] — [scope detail]"
  Example input:  "feat: add WebSocket heartbeat", "fix: auth token refresh", "v2.1 release"
  Example draft:  "Implemented WebSocket heartbeat mechanism and auth token refresh.
                   Released v2.1 with multi-ecosystem scanning support."

FIELD 2 — NEW CAPABILITY:
  Source: commit messages containing "feat:", "add", "implement", "first", "new", "support"
         + file extensions not seen in prior entries (if file exists)
  Draft the most technically specific "first time" action visible in the diff.
  If nothing clearly new → draft: "[NEEDS INPUT] What capability did you gain?"

FIELD 3 — BLOCKED BY:
  Source: commit messages containing "fix:", "workaround", "hotfix", "revert", "debug", "issue"
  Also check: repeated fix commits targeting same file/module = likely pain point
  If no fix/debug commits → draft: "None significant."

FIELD 4 — SHIPPED:
  Source: commit messages containing "release", "deploy", "v[0-9]", "publish", "merge", "live"
  Also check: tags in session range
  git -C <repo_path> tag --sort=creatordate | tail -5
  Draft: version tag + branch + any URL found in README
  If nothing concrete → draft: "[NEEDS INPUT] What is the deliverable state?"
```

### Step 1.3 — Determine mode

```
MODE FIRST    → progress log does not exist OR has 0 entries
MODE RETURNING → progress log exists AND has ≥1 entry
```

### STOP-1 (Mandatory)

Present the auto-drafted entry for confirmation. Do NOT show empty fields.
Fields marked `[NEEDS INPUT]` must be filled by user before proceeding.

**Format:**

```
📋 Draft entry for <session.start> – <session.end> · <project_name>
   Based on: <N> commits, <files_changed> files changed, branch: <branch>
[MODE RETURNING only: Last entry: <date> · <project> — <one-line summary>]

── Draft ──────────────────────────────────────────────
Done:
  <auto-drafted field 1>

New capability:
  <auto-drafted field 2>  [or: [NEEDS INPUT]]

Blocked by:
  <auto-drafted field 3>

Shipped:
  <auto-drafted field 4>  [or: [NEEDS INPUT]]
───────────────────────────────────────────────────────

Confirm, correct, or fill in [NEEDS INPUT] fields.
Type OK to confirm, or paste corrections:
```

**→ STOP. Do not proceed until user responds with OK or corrections.**
If user provides corrections → update draft → proceed to Phase 2.
If any [NEEDS INPUT] fields remain unfilled → re-ask only those fields.

---

## Phase 2: Cross-Entry Analysis

**Skip this phase entirely if been-there-done-that.md has 0 prior entries.**

Read all existing entries and compare against the new entry.
Detect and surface only what the data actually supports. Do not invent patterns.

```
DETECT:
  a) New tech/tool not seen in any prior entry   → "First time" flag
  b) Same blocker appearing in ≥2 entries        → "Recurring blocker" flag
  c) Domain concentration (≥3 entries same area) → "Emerging depth" flag
  d) Complexity change (compare scope over time)

GENERATE (only if data supports it):
  📊 Cross-entry note  → factual observation, 1 line max
  🎯 Portfolio note    → only if: solo delivery, production deployment,
                         or novel tech application. Never for routine work.
```

**Rules — non-negotiable:**
- One `📊` note maximum per entry
- One `🎯` note maximum per entry
- If data doesn't clearly support a note → write nothing
- Never write praise. Never write encouragement. Never predict future growth.

### STOP-2 (Mandatory)

```
Analysis for this entry:

  📊 This is your 2nd entry involving real-time systems (prev: WooMaps tracking)
  🎯 Portfolio note: Solo delivery, production-deployed at yagura.space

Does this look accurate? [Y / edit / skip]
```

**→ STOP. Do not proceed until user responds.**

---

## Phase 3: Place & Write

### Compute tree position

Use `session.end` date as the anchor.

```
Tree path: ## <YEAR> / ### <Month Name> / #### <YYYY-MM-DD> · <Project Name>

Tree order: ASCENDING (oldest at top of file, newest at bottom)
  - Years:  ascending (2024 above 2025 above 2026)
  - Months: ascending within year (January above February)
  - Dates:  ascending within month (01 above 15 above 28)

If that exact date node exists → append BELOW existing same-date entry
If date is new → insert in ascending order within the month block
If month is new → insert in ascending order within the year block
If year is new → append new year block at END of file
```

**New entries go toward the bottom of their section. The file grows downward.**

### Entry format

```markdown
#### <YYYY-MM-DD> · <Project Name>

**Session:** <start> – <end> · `<branch>` · <N> commits · <files_changed> files changed
**Stack:** <tech1>, <tech2>, ... (from answers + git diff)

**Done:**
<What was done — factual, specific, no adjectives of praise>

**New capability:**
<What user can do now — one concrete technical action, no vague learning>

**Blocked by:**
<Obstacles — factual. "None significant." if empty>

**Shipped:**
<Deliverable state — URL, branch, version, or status>

📊 <cross-entry observation, if any>
🎯 <portfolio note, if any>
```

### File structure

Tree is chronological ascending — oldest entries at the top, newest at the bottom.
Read top-to-bottom = read the history from start to now.

```markdown
# Been There Done That

## 2025
### November
#### 2025-11-14 · FSTrack Tractor
...

## 2026
### January
#### 2026-01-15 · WooMaps
...

### February
#### 2026-02-20 · Yagura
...
```

### STOP-3 (Mandatory)

```
Preview — entry to be written:

────────────────────────────────────────
#### 2026-02-20 · Yagura
...full entry...
────────────────────────────────────────

Write this to <file_path>? [Y / edit]
```

**→ STOP. Write ONLY after explicit Y.**

---

## Phase 4: Done

After writing:
1. Print: `✓ Entry written to <file_path>`
2. Show only the heading line added (date + project)
3. Stop completely. No summary. No praise. No "what's next".

---

## Anti-Patterns (Hard Rules)

These must never appear in any output this skill produces:

| Forbidden | Correct approach |
|---|---|
| "You've grown so much" | omit entirely |
| "Impressive work" | omit entirely |
| "V completed work of 3 devs" | "Solo delivery of X involving Y and Z" |
| "Getting better at Rust" | "Third entry involving Rust async patterns" |
| "worked on backend stuff" | "Implemented SQLx connection pooling for concurrent sessions" |
| Future praise / encouragement | omit entirely |

The document is a ledger, not a trophy cabinet.

---

## Additional References

- [references/git-commands.md](references/git-commands.md) — full git command reference for session extraction
- [references/tree-insertion-logic.md](references/tree-insertion-logic.md) — algorithm for inserting entries at correct tree position
- [references/analysis-patterns.md](references/analysis-patterns.md) — cross-entry pattern detection rules and examples
