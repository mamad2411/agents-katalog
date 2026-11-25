<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: retro
description: >
  Engineering retrospective with git + memory data analysis. Triggers on
  "retro", "회고", "weekly retro", "이번 주 리뷰", "what did we ship",
  "엔지니어링 회고", "주간 회고", "지난주 리뷰".
  Analyzes commits, memory activity, work patterns. Persistent history
  with trend tracking.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# /retro — Engineering Retrospective

Comprehensive retrospective analyzing git history, memory activity, and work patterns.
Persistent history with trend tracking.

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

## Arguments

- `/retro` — default: last 7 days
- `/retro 24h` — last 24 hours
- `/retro 14d` — last 14 days
- `/retro 30d` — last 30 days
- `/retro compare` — compare current vs prior same-length window

Parse argument. Default 7d. Validate format: number + d/h/w, or "compare".

---

## Step 1 — Data Collection (parallel)

Detect default branch:
```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || echo "main")
```

Compute midnight-aligned start date for day/week windows.

Run ALL commands in parallel:

```bash
# 1. Commits with stats
git log origin/$DEFAULT_BRANCH --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. Per-commit LOC breakdown
git log origin/$DEFAULT_BRANCH --since="<window>" --format="COMMIT:%H|%aN" --numstat

# 3. Timestamps for session detection
git log origin/$DEFAULT_BRANCH --since="<window>" --format="%at|%aN|%ai|%s" | sort -n

# 4. File hotspots
git log origin/$DEFAULT_BRANCH --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. PR numbers
git log origin/$DEFAULT_BRANCH --since="<window>" --format="%s" | grep -oE '#[0-9]+' | sort -n | uniq

# 6. Per-author commit counts
git shortlog origin/$DEFAULT_BRANCH --since="<window>" -sn --no-merges
```

Additionally, query memory:
```
memory_search_date(start: "{window_start}", end: "{today}", category: "daily-logs", limit: 50)
memory_search(tag: "done", limit: 20)
memory_search(tag: "decision", limit: 10)
memory_stats()
```

If task-scheduler available:
```
task_history()
```

---

## Step 2 — Metrics Table

| Metric | Value |
|--------|-------|
| Commits to default | N |
| Contributors | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC | N |
| Test LOC ratio | N% |
| Active days | N |
| Sessions detected | N |
| Avg LOC/session-hour | N |
| Memories created | N |
| Knowledge graph nodes | N |
| Skills used | list |

Per-author leaderboard:
```
Contributor         Commits   +/-          Top area
You (name)              32   +2400/-300   src/
collaborator            12   +800/-150    tests/
```

---

## Step 3 — Commit Time Distribution

Hourly histogram (local time):
```
Hour  Commits  ████████████████
 09:    4      ████
 14:    8      ████████
 22:    5      █████
```

Call out peak hours, dead zones, late-night patterns.

---

## Step 4 — Work Session Detection

45-minute gap threshold between commits. Classify:
- **Deep sessions** (50+ min)
- **Medium sessions** (20-50 min)
- **Micro sessions** (<20 min)

Calculate total active time, average session length, LOC/hour.

---

## Step 5 — Commit Type Breakdown

Categorize by conventional prefix (feat/fix/refactor/test/chore/docs):
```
feat:     20  (40%)  ████████████████████
fix:      27  (54%)  ███████████████████████████
refactor:  2  ( 4%)  ██
```

Flag if fix ratio > 50% — may indicate review gaps.

---

## Step 6 — Hotspot Analysis

Top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test vs production files in list

---

## Step 7 — Memory & Decision Analysis

From memory data:
- Key decisions made this period (from tag: "decision")
- Completed tasks (from tag: "done")
- Memory health: total memories, new this period, archived

---

## Step 8 — Focus Score + Ship of the Week

**Focus score:** % of commits touching single most-changed directory.
Higher = deeper work. Lower = scattered.

**Ship of the week:** Highest-impact PR/change.

---

## Step 9 — Streak Tracking

```bash
# Consecutive days with commits
git log origin/$DEFAULT_BRANCH --format="%ad" --date=format:"%Y-%m-%d" | sort -u
```

Count backward from today.

---

## Step 10 — Prior Retro Comparison

Search memory for previous retro:
```
memory_search(tag: "retro", limit: 1)
```

If found, show trends:
```
                    Last        Now         Delta
Test ratio:         22%    →    41%         ↑19pp
Sessions:           10     →    14          ↑4
Commits:            32     →    47          ↑47%
```

If first retro: "First retro recorded — run again next week to see trends."

---

## Step 11 — Save & Report

Save retro to memory:
```
memory_store(
  category: "daily-logs",
  title: "Retro: {date range}",
  content: "{full retro JSON metrics}",
  tags: ["retro", "weekly-review"],
  importance: 7
)
memory_daily_log(type: "done", entry: "Weekly retro completed: {tweetable summary}")
```

---

## Step 12 — Narrative Output

Structure:

**Tweetable summary** (first line):
```
Week of {date}: {commits} commits, {LOC}k LOC, {test_ratio}% tests, {sessions} sessions | Streak: {N}d
```

### Metrics Table (Step 2)
### Time & Session Patterns (Steps 3-4)
### Shipping Velocity (Steps 5-6)
### Memory & Decisions (Step 7)
### Focus & Highlights (Step 8)
### Your Week (personal deep-dive with praise + growth areas)
### Top 3 Wins
### 3 Things to Improve (specific, anchored in data)
### 3 Habits for Next Week (practical, <5 min to adopt)

---

## Notify

## Messenger Notification

Send notifications for significant events via messenger:

### When to Notify

| Event | Platform | Priority |
|-------|----------|----------|
| Task/pipeline completed | telegram | Normal |
| Verification failed | telegram | High |
| Long-running task done (10+ min) | telegram | Normal |
| Critical error or blocker | telegram | High |
| PR created / release shipped | all | Normal |
| Importance ≥ 8 memory created | telegram | Normal |

### Notification Format

```
messenger_send(
  platform: "telegram",
  message: "[{skill-name}] {status_emoji} {brief description}\n\n{details if relevant}"
)
```

**Status Emojis**:
- Completed successfully: ✅
- Completed with warnings: ⚠️
- Failed / blocked: ❌
- Needs attention: 🔔

### Do NOT Notify

- Routine memory operations
- Intermediate progress steps
- Read-only operations (search, list, status)

```
messenger_send(platform: "telegram", message: "{tweetable summary}\n\nFull retro available in memory.")
```

## Tone

- Encouraging but candid
- Specific — always anchor in actual commits/data
- Skip generic praise — say exactly what was good
- Frame improvements as leveling up, not criticism
- ~2000-3500 words total

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
