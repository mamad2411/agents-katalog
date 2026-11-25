---
name: master-calendar
description: "Master Calendar — unified task/meeting hub in Asana. NPAO-classified task creation from Hermes, email, and Google Calendar."
version: 1.0.0
author: Hermes + Pat Diamitani
dependencies:
  - asana
  - google-workspace
---

# Master Calendar

Unified task + meeting hub. All todos, meetings, and reminders flow into a single Asana project with calendar view as default.

```
You (Hermes prompt / email) ──→ NPAO Classify ──→ Asana Task ──→ Calendar View
Google Calendar ──→ Cron Sync ──→ Asana Task ──→ Calendar View
```

## Key IDs

| Resource | GID |
|----------|-----|
| Workspace (Life) | `1206772437471958` |
| Project (Master Calendar) | `1216602500278026` |
| Calendar View | `1216606931078457` |
| Asana Link | https://app.asana.com/0/1206772437471958/1216602500278026 |

### Sections
| Section | GID |
|---------|-----|
| Untitled section | `1216602500278027` |
| Daily | `1216602500278035` |
| This Week | `1216606863211538` |
| Backlog | `1216607099316022` |
| Meetings | `1216607155326677` |
| Done | `1216607328833661` |

## CLI Shorthand

```bash
ASANA="python3 ~/.hermes/skills/productivity/asana/scripts/asana_cli.py"
GAPI="python3 ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
```

---

## Workflow 1: Hermes → Task (Natural Language)

When the user says something like:
- "add call dentist Friday 2pm"
- "remind me to submit the report by Monday"
- "create task: review PR, high priority"

### Step 1: Parse Intent (PAL Stage 1)

Extract:
- **task_name**: what needs to be done
- **due_date**: when (today, tomorrow, Friday, "next week", ISO date)
- **priority_signal**: "urgent", "high priority", "asap" → high; unstated → medium; "someday", "whenever" → low
- **source**: "hermes"
- **section**: infer from timeframe
  - Today/tomorrow → "Daily"
  - Within 7 days → "This Week"
  - Further out → "Backlog"

### Step 2: NPAO Classify

Apply 4D priority scoring:

```python
# Phase urgency (defaults)
phase_urgency = {
    "urgent": 8, "high": 6, "medium": 4, "low": 2, "someday": 2
}[priority_signal]

# Dependency: single task = 0 (no blockers)
dependency_impact = 0

# Business impact
business_impact = {
    "urgent": 8, "high": 6, "medium": 4, "low": 2
}[priority_signal]

# Resource efficiency: quick task < 1hr = 10
resource_efficiency = 10 if "quick" in task_name.lower() else 7

priority_score = (phase_urgency * 0.35) + (dependency_impact * 0.30) + \
                 (business_impact * 0.25) + (resource_efficiency * 0.10)

# Phase classification
if priority_signal == "urgent":
    phase = "deploy"  # needs immediate action
elif "fix" in task_name.lower() or "bug" in task_name.lower():
    phase = "debug"
elif "plan" in task_name.lower() or "design" in task_name.lower():
    phase = "design"
elif "research" in task_name.lower() or "look into" in task_name.lower():
    phase = "pred"
else:
    phase = "dev"
```

### Step 3: Build NPAO Notes

```
phase:{phase}|priority:{priority_score:.1f}|impact:{impact_label}|source:hermes
```

### Step 4: Create Asana Task

```bash
$ASANA task create \
  --name "TASK_NAME" \
  --project 1216602500278026 \
  --due DUE_DATE \
  --notes "phase:{phase}|priority:{score}|impact:{impact}|source:hermes" \
  --section "SECTION_NAME"
```

### Step 5: Report Back

Confirm with:
- Task name + Asana permalink
- Due date
- Section placed
- NPAO score

Example response:
> ✅ Added "Call dentist" for Friday July 18
> 📊 NPAO: phase=dev | priority=4.9 | section=This Week
> 🔗 https://app.asana.com/0/1206772437471958/1216602500278026/task/TASK_GID

---

## Workflow 2: Email → Task (Gmail → Asana)

### Setup (one-time)

1. Google Workspace OAuth must be configured (see `google-workspace` skill)
2. Create a cron job that polls Gmail for task emails

### Email Format

Send from your Gmail to yourself (patrick.diamitani@gmail.com):

```
Subject: [TODO] Call dentist Friday 2pm
Body: Priority: high
      Notes: Dr. Smith, 312-555-0100
```

Or just forward any email to yourself with `[TODO]` prefix.

### Cron Job

```bash
# Every 30 minutes, check for [TODO] emails and create Asana tasks
python3 ~/.hermes/skills/productivity/asana/scripts/gmail_to_asana.py
```

### Parsing Logic

- Subject after `[TODO]` → task name
- `Priority:` line → NPAO priority signal
- `Due:` line or day-of-week mention → due date
- Remaining body → task notes
- Source tag: `source:email`

---

## Workflow 3: Google Calendar → Asana Sync

### Setup

Requires Google Workspace OAuth with Calendar scope.

### Cron Job (Every 2 Hours)

```bash
$GAPI calendar list --start "$(date -u +%Y-%m-%dT00:00:00Z)" --end "$(date -u -v+7d +%Y-%m-%dT23:59:59Z)"
```

For each event not already in Asana (check by existing task names):
1. Create task in "Meetings" section
2. Set due date = event date
3. Notes: event details + Google Calendar link
4. Source tag: `source:gcal`

### Dedup Strategy

Before creating, check if a task with the same name + date already exists:
```bash
$ASANA task list --project 1216602500278026 --due-on EVENT_DATE
```
Skip if match found.

---

## Workflow 4: Daily Briefing (Cron)

Every morning at 7am CT, send today's task list:

```bash
$ASANA calendar today --project 1216602500278026
```

Format as a clean summary with NPAO-prioritized ordering.

---

## Verification

After every task creation:
```bash
$ASANA task get TASK_GID
```
Confirm: due date correct, section placed, notes have NPAO metadata, permalink works.

---

## Pitfalls

- **Section names**: always use names (not GIDs) with `--section` — the CLI resolves them automatically
- **Due dates**: always ISO format (YYYY-MM-DD) or "today"/"tomorrow"
- **NPAO notes**: pipe-delimited format — don't use commas or newlines inside the notes field
- **Google auth**: if `NOT_AUTHENTICATED`, guide user through `google-workspace` setup

## Reference Files

- Asana skill: `~/.hermes/skills/productivity/asana/`
- Google Workspace skill: `~/.hermes/skills/productivity/google-workspace/`
- NPAO reference: `rostr-framework` skill → `references/npao-orchestrator.md`
