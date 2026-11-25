---
name: coordinate-executors
description: "Sends deadline reminder emails to task executors for overdue or
  approaching-deadline tasks. Checks Jira (or project-plan.md as fallback) for
  tasks with deadlines within 2 business days or already overdue, groups them by
  assignee, and sends personalized reminders via Gmail — autonomy level 1 (no
  PM confirmation required). Covers project tasks #13 (Phase 3, prototyping) and
  #23 (Phase 5, launch/marketing). Runs as a scheduled task (Mon–Fri, 10:00) or
  on demand via /remind-executors.
  Triggers RU: «напомни исполнителям», «проверь дедлайны», «coordinate-executors»,
  «кто просрочил задачи», «отправь напоминания команде», «какие задачи горят»,
  «напоминания о дедлайнах», «проверь просроченные задачи».
  Triggers EN: 'remind executors', 'check deadlines', 'send deadline reminders',
  'who has overdue tasks', 'executor reminders', 'task reminders', 'overdue tasks',
  'remind the team about deadlines', 'coordinate executors', 'deadline check'."
---

# Skill: coordinate-executors

Sends personalized deadline reminder emails to task executors.
Checks Jira for overdue or approaching-deadline tasks, groups by assignee,
and sends emails via Gmail at autonomy level 1 (no confirmation needed).
Runs daily as a scheduled task or on demand.

---

## Triggers

**Russian:** «напомни исполнителям», «проверь дедлайны», «отправь напоминания», «кто просрочил задачи», «какие задачи горят», «проверь просроченные»
**English:** "remind executors", "check deadlines", "send deadline reminders", "overdue tasks", "remind the team", "coordinator reminders"

---

## Language Detection

1. Read `language` field from `project-state.md` → use that value (RU or EN)
2. If field is absent → scan any existing project artifact for Cyrillic content; if found → RU
3. If still undetermined → EN (default)

- RU → `email-tpl-reminder-deadline-ru.md`
- EN → `email-tpl-reminder-deadline-en.md`

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Tasks with deadlines and assignees | yes | Jira MCP (primary) or `02-planning/project-plan.md` (fallback) |
| Reminder horizon | no | Default ≤ 2 business days; configurable via `project-state.md → reminder_horizon_days` |
| Executor contacts | no | `01-initiation/stakeholder-map.md` or Jira profiles |
| Project name, current phase | no | `project-state.md` |

## Output

| File / Action | Path | Condition |
|---------------|------|-----------|
| Deadline reminder email | — (Gmail, external) | Tasks with deadline ≤ 2 days or overdue |
| `reminders-{YYYY-MM-DD}.md` | `reports/` | Fallback: Gmail unavailable |
| Log entry | `logs/log.md` | Always |
| State update | `project-state.md` | When reminders are sent |

---

## Instructions

### Step 1 — Guard-rail

If the request is about team management theory, HR practices, or motivation
(not about specific project task deadlines) → respond:
"coordinate-executors sends deadline reminders to task assignees. Tell me which
tasks or project phase to check."
Do not start the workflow.

---

### Step 2 — Initialize

Determine run mode:
- **Scheduled:** fully autonomous — no questions asked
- **Manual:** may clarify reminder horizon if explicitly changed by PM

Read `project-state.md` → project name, current phase, sprint, PM name,
`reminder_horizon_days` (default: 2 if not set).

---

### Step 3 — Fetch Tasks

**Primary path (Jira available):**
Query tasks with filter:
- Status not "Done" / "Closed" / "Won't Fix"
- Assignee is set (not "Unassigned")
- `dueDate` ≤ today + `reminder_horizon_days` (business days) OR `dueDate` < today

Group results by assignee.

**Fallback (Jira unavailable):**
Read `02-planning/project-plan.md`. Extract tasks for the current phase with
fields: task name, owner, deadline, status.
Apply the same filter: deadline ≤ today + horizon OR overdue.
Notify PM in chat: "Jira unavailable. Data loaded from project-plan.md."

---

### Step 4 — Check for Tasks

If no qualifying tasks found:
- Write to `logs/log.md`:
  `{DATE}: coordinate-executors — check complete, no overdue or approaching tasks`
- Exit without sending emails.

---

### Step 5 — Prepare Reminders

For each executor with qualifying tasks:

1. Split tasks into two lists:
   - **Overdue:** `dueDate` < today (include days overdue)
   - **Upcoming:** `dueDate` = today or today + 1–{horizon} days (include days remaining)

2. Load the E6 template matching the project language:
   - English → `templates/email-tpl-reminder-deadline-en.md`
   - Russian → `templates/email-tpl-reminder-deadline-ru.md`

3. Populate the template:
   - `{EXECUTOR_NAME}` — assignee name
   - `{PROJECT_NAME}` — from project-state.md
   - `{OVERDUE_TASKS}` — table: task name | due date | days overdue
   - `{UPCOMING_TASKS}` — table: task name | due date | days remaining
   - `{PM_NAME}` — from project-state.md (or placeholder)

4. Resolve executor email:
   - From `01-initiation/stakeholder-map.md` (primary)
   - From Jira profile (if stakeholder-map unavailable)
   - If not found → add to unknown-contact list; escalate to level 2 for that executor

---

### Step 6 — Send Reminders

**Primary path (Gmail available):**
For each executor:
- Call `send-email` skill with autonomy level 1 (auto-send)
- **Exception:** if executor email is not in stakeholder-map.md or Jira profile → escalate to level 2 (show draft to PM, request confirmation before sending)
- One email per executor (do not merge multiple executors into one email)

**Fallback (Gmail unavailable):**
Create `reports/reminders-{YYYY-MM-DD}.md`. For each executor — one section using the E6 template structure:
- H2 header: `## {EXECUTOR_NAME} <{EXECUTOR_EMAIL}>`
- Subject line, greeting, overdue/upcoming tables, action items, signature
- Blank line between executor sections

Notify PM: "Gmail unavailable. Reminder drafts saved to `reports/reminders-{DATE}.md` — send manually."

---

### Step 7 — Log and Update State

1. Write to `logs/log.md`:
   - If sent: `{DATE}: coordinate-executors — {N} reminders sent ({EXECUTOR_LIST})`
   - If fallback: `{DATE}: coordinate-executors — fallback, saved reports/reminders-{DATE}.md`

2. Update `project-state.md`: set `last_reminder_check` to today's date.

3. Output summary to chat:
   - Number of reminders sent and executor names, OR
   - "No overdue or approaching tasks found."

---

## Templates

| File | Purpose |
|------|---------|
| `templates/email-tpl-reminder-deadline-en.md` | Email template E6 — deadline reminder (EN) |
| `templates/email-tpl-reminder-deadline-ru.md` | Email template E6 — deadline reminder (RU) |

---

## Dependencies

**Reads (optional):**
- `project-state.md` — project name, phase, PM, horizon setting
- `01-initiation/stakeholder-map.md` — executor contacts
- `02-planning/project-plan.md` — task list (Jira fallback)

**External actions:**
- Jira MCP — task query (primary)
- Gmail MCP via `send-email` — sending reminders (primary)

**Passes data to:**
- `send-email` — email body, recipient, autonomy level

---

## Constraints

- Does not create Jira tasks — only reads existing ones
- Does not update task status — only sends reminders
- Does not analyze root causes of overdue tasks
- One email per executor per run; re-running the same day sends a new email
- Tasks without a due date are ignored
- In scheduled mode without a valid `project-state.md` → log error and exit
- Fallback mode does not block log entry creation
