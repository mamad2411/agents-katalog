<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: daily-routine
description: >
  Daily routine automation skill with OMC integration. Triggers on "오늘 할일",
  "데일리", "모닝 브리핑", "오늘 일정", "할일 정리", "하루 마무리", "이번주 요약",
  "today's tasks", "daily", "morning briefing", "today's schedule", "organize tasks",
  "wrap up the day", "end of day", "weekly summary", "weekly review" and similar.
  v3: Polls messenger at start, includes OMC team status, uses comms-agent for
  notifications, syncs with OMC state.
---

# Daily Routine — Daily Routine Automation Engine

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

Automate the 4 routines that structure the user's day (morning briefing, task
management, evening review, weekly retrospective) using the memory-manager and
messenger-bot MCP tools. Registering as a cron job in task-scheduler enables
fully autonomous execution.

## Workflow 1: Morning Briefing

Trigger: Automatic execution on weekdays at 09:00, or on "morning briefing", "today's briefing" request

### Step 1 — Collect Yesterday's Summary

```
memory_search:
  category: "daily-logs"
  limit: 1
→ Retrieve daily log from yesterday
→ Summarize main activities in 3 lines
```

### Step 2 — Collect Incomplete Tasks

```
memory_search:
  tag: "todo"
  limit: 20
→ Sort results descending by importance
→ Group in order: priority-high > priority-mid > priority-low
```

### Step 3 — Collect Today's Scheduled Events

```
memory_search:
  tag: "{today's date, e.g. 2026-03-21}"
  limit: 10
→ Sort meetings, deadlines, events chronologically
```

### Step 4 — Industry News Collection (Optional)

```
web_search:
  query: "{user's areas of interest} latest news"
→ Web3 security, AI agents, startup-related
→ Top 3 results only, summarized in one line each
→ This step is optional; skip if network request fails
```

### Step 5 — Generate & Send Briefing

Fill in the morning briefing template from `references/routine-templates.md` with the collected data.

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
messenger_send:
  platform: "telegram"
  message: "{generated briefing markdown}"
```

Also record the briefing in the daily log:

```
memory_daily_log:
  entry: "Morning briefing generated and sent"
  type: "note"
```

## Workflow 2: Task Management

### Add Task

When the user mentions a task, store it as follows:

```
memory_store:
  category: "tasks"
  title: "{task title}"
  content: "{detailed description (if any)}"
  tags: ["todo", "priority-{high|mid|low}", "{project name}"]
  importance: {high=9, mid=7, low=6}
```

Record confirmation after saving:

```
memory_daily_log:
  entry: "Task added: {task title}"
  type: "todo"
```

### Mark Task Complete

```
memory_update:
  id: {relevant memory ID}
  mode: "metadata"
  tags: ["done", ...existing tags with "todo" removed]

memory_daily_log:
  entry: "{task title} completed"
  type: "done"
```

### Task Review

Run on "organize tasks", "today's tasks" request:

```
memory_search:
  tag: "todo"
  limit: 30
→ Sort descending by importance
→ Visualize with icons: priority-high (🔴), priority-mid (🟡), priority-low (🟢)
→ Mark overdue items with ⚠️
```

## Workflow 3: Evening Review

Trigger: Automatic execution daily at 21:00, or on "wrap up the day", "evening review" request

### Step 1 — Retrieve Today's Daily Log

```
memory_search:
  category: "daily-logs"
  limit: 1
→ Retrieve full log for today's date
```

### Step 2 — Classify Completed / Incomplete

```
memory_search:
  tag: "done"
  category: "tasks"
  limit: 20
→ Collect items completed today

memory_search:
  tag: "todo"
  limit: 20
→ Collect items still incomplete
```

### Step 3 — Identify Carryover Items

Among incomplete items:
- `importance >= 7` → Automatically carry over (keep as tomorrow's task)
- `importance < 7` → Suggest to user whether to carry over
- Items incomplete for 3+ days → Show ⚠️ warning

### Step 4 — Generate Review

Fill in the evening review template from `references/routine-templates.md` with the data.

Record the review in the daily log:

```
memory_daily_log:
  entry: "Daily review complete — Completed {N}, Incomplete {M}, Carried over {K}"
  type: "note"
```

## Workflow 4: Weekly Retrospective

Trigger: Automatic execution on Sundays at 20:00, or on "weekly summary", "weekly review" request

### Step 1 — Retrieve This Week's Daily Logs (7 days)

```
memory_search:
  category: "daily-logs"
  limit: 7
→ Collect Monday–Sunday logs in chronological order
```

### Step 2 — Progress by Project

```
memory_search:
  category: "projects"
  limit: 20
→ Filter by updated_at within this week
→ Group by project and summarize progress
```

### Step 3 — Decision Log

Extract `type: "decision"` entries from daily logs and compile them.

### Step 4 — Plan for Next Week

Based on incomplete tasks and project progress, propose the Top 3 priorities for next week.

### Step 5 — Generate & Send Retrospective

Fill in the weekly retrospective template from `references/routine-templates.md` with the data.

```
messenger_send:
  platform: "telegram"
  message: "{generated weekly retrospective markdown}"
```

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
memory_store:
  category: "daily-logs"
  title: "Weekly Retrospective — Week {N}"
  content: "{retrospective markdown}"
  tags: ["weekly-review", "{year-month}"]
  importance: 6
```

## Cron Registration Examples

Call `task_create` on the task-scheduler MCP to register automated execution:

### Morning Briefing (Weekdays 09:00)

```
task_create:
  name: "Morning Briefing"
  prompt: "Generate morning briefing and send via Telegram"
  cron: "0 9 * * 1-5"
  allowedTools: ["memory-manager", "messenger-bot"]
  tags: ["routine", "morning"]
  enabled: true
```

### Evening Review (Daily 21:00)

```
task_create:
  name: "Evening Review"
  prompt: "Write end-of-day review"
  cron: "0 21 * * *"
  allowedTools: ["memory-manager"]
  tags: ["routine", "evening"]
  enabled: true
```

### Weekly Retrospective (Sundays 20:00)

```
task_create:
  name: "Weekly Retrospective"
  prompt: "Generate weekly retrospective and send via Telegram"
  cron: "0 20 * * 0"
  allowedTools: ["memory-manager", "messenger-bot"]
  tags: ["routine", "weekly"]
  enabled: true
```

## Available Tools Table

| Task | MCP Tool | Notes |
|------|----------|-------|
| Retrieve daily log | `memory_search` | category:"daily-logs" |
| Retrieve tasks | `memory_search` | tag:"todo" |
| Retrieve schedule | `memory_search` | tag:date |
| Save task | `memory_store` | category:"tasks" |
| Mark task complete | `memory_update` | mode:"metadata" |
| Record log | `memory_daily_log` | Emoji auto-added by type |
| Memory status | `memory_stats` | For weekly retrospective stats |
| Send message | `messenger_send` | platform:"telegram" |
| Register auto-run | `task_create` | cron expression |

## Reference Documents

- 3 output templates: `references/routine-templates.md`
- Briefing generation script: `scripts/generate-briefing.py`

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
