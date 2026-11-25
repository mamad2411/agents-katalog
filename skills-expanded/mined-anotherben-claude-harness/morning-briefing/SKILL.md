---
name: morning-briefing
description: Start-of-day briefing for ADHD workflow. Shows what happened since last session, surfaces stale/blocked items across ALL life domains (dev, business, personal, learning, creative), recommends focus items, and proactively nudges about forgotten things. Use when the user says "good morning", "what's up", "brief me", "start my day", "what were we up to", "what did we do", or invokes /morning-briefing. Also triggered by the 9am weekday cron.
---

# Morning Briefing

Your ADHD-friendly start-of-day system. Conversational, direct, and actionable. No walls of text — headlines first, details on request.

**Presented in clear sections: Dev Work → Business → Personal → Learning & Creative → Cross-cutting.**

## Vault Path

`{{VAULT_PATH}}`

## Vault Folders

| Folder | Domain | Contains |
|---|---|---|
| `00-Inbox` | mixed | Untriaged items |
| `01-Bugs` | dev | Agent-ready bugs |
| `02-Tasks` | dev | Agent-ready tasks |
| `03-Ideas` | dev | Parked dev ideas |
| `04-In-Progress` | dev | Currently being worked on |
| `05-Archive` | mixed | Completed/archived |
| `06-Business` | business | Strategy, revenue, operations |
| `07-Personal` | personal | Errands, appointments, life admin |
| `08-Learning` | learning | Courses, articles, research |
| `09-Creative` | creative | Side projects, product ideas, SaaS |

## Known Project Directories

| Project | Path |
|---|---|
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| my-project | `{{PROJECT_DIR}}` |
| cortex | `{{PROJECT_DIR}}` |

## Tone

Be conversational and direct. You are a reliable co-pilot, not a clinical dashboard. Use short sentences. Be honest about stale items — the user wants accountability, not coddling. But always offer an escape hatch (park, archive, wont-do).

Examples:
- "You started the PO approval fix 2 weeks ago and haven't touched it. Park it or push through?"
- "You said you'd call the accountant 5 days ago. Done?"
- "3 ideas have been sitting for over a month. Quick gut check — still excited about any of these?"
- "You're spread across 8 projects but only touched 3 this week. That's a lot of mental load."

---

## Section 1: Dev Work

### Step 1.1: What Happened Recently

**Activity Logs**: Read files from `_activity/` created in the last 48 hours (by filename date prefix).

**Handovers**: Glob for recent handover files across known project directories:
```
{project_path}/docs/handovers/YYYY-MM-DD-*.md
```

**Git Activity**: For each known project directory that exists:
```bash
git -C {project_path} log --oneline --since="2 days ago" --all 2>/dev/null | head -10
```

**Summarize**:
```
Since you were last here:
- my-project: 4 commits, agent completed "PO approval bug fix"
- my-project: 2 commits, left off on "V3 disposal form migration"
- No activity on: my-project, my-project (last touched 12 days ago)
```

### Step 1.2: Dev Vault State

Call `mcp__vault-index__list_vault` to fetch items. Filter to dev-domain folders (00 through 05).

```
| Queue          | Count | Critical | High | Stale |
|----------------|-------|----------|------|-------|
| 00-Inbox       | 8     | -        | 2    | 3     |
| 01-Bugs        | 25    | 1        | 5    | 4     |
| 02-Tasks       | 220   | -        | 12   | 8     |
| 03-Ideas       | 9     | -        | -    | -     |
| 04-In-Progress | 35    | 2        | 8    | 6     |
```

### Step 1.3: Dev Staleness Callouts

For items in dev folders (NOT in `03-Ideas` or `05-Archive`), compute days since `updated` (or `created`).

**Only call out items that need attention** — don't list fresh items.

- **Aging (7-14d)**: "Aging: {title} ({project}) — {N} days without update"
- **Stale (14-30d)**: "You started '{title}' {N} days ago and haven't touched it. Park it or finish it?"
- **Abandoned (30d+)**: "'{title}' has been sitting for {N} days. Be honest — are you going to do this? Archive it or put it on today's list."

Limit to top 5. If more: "...and {N} more stale items. Run /vault-sweep for the full picture."

### Step 1.4: Top 3 Dev Focus

Score non-blocked, non-archived, non-parked dev items:
```
score = priority_weight * (1 + staleness_days / 7)
```
Priority weights: critical=4, high=3, medium=2, low=1.
In-progress items get 1.5x (lower switching cost for ADHD).

```
Dev focus for today:
1. [BUG] "{title}" — {project} — {why}
2. [TASK] "{title}" — {project} — {why}
3. [BUG] "{title}" — {project} — {why}
```

---

## Section 2: Business

Read items from `06-Business/`. Compute staleness.

Present:
```
Business ({count} items):
- {high priority items first}
- Stale: "{title}" — {N} days. Still relevant?
- Parked reminders due: "{title}" parked {N} days ago
```

If empty: "No business items tracked. /brain-dump to capture any."

---

## Section 3: Personal

Read items from `07-Personal/`. These are often time-sensitive (appointments, errands).

Present with urgency:
```
Personal ({count} items):
- "{call the accountant}" — you captured this {N} days ago. Done?
- "{renew rego}" — {N} days old. Overdue?
- "{buy birthday present}" — low priority, 3 days old
```

If empty: "No personal items tracked."

---

## Section 4: Learning & Creative

Read items from `08-Learning/` and `09-Creative/`. Light touch — these are low-pressure.

```
Learning ({count}): "{look into Rust}" (12d), "{read that article on X}" (5d)
Creative ({count}): "{SaaS for gun dealers}" (20d), "{side project Y}" (8d)
```

Only flag items over 60 days (these categories are naturally slow-burn).

---

## Section 5: Cross-cutting

### Parked Item Reminders

Search ALL folders for items with `parked` tag where `remind_after` date has passed:

```
Parked reminders due:
- "{title}" ({domain}) — parked {N} days ago, reminder was set for today. Pick up, extend (+7d), or archive?
```

### Scatter-Brain Score

Count across ALL domains:
- **Open items**: distinct projects/domains with at least one non-archived item
- **Recently active**: distinct projects/domains with activity in last 7 days

```
Scatter-brain score: {open} areas open, {active} recently active.
```

If open > active * 2: warn about spread.

### Idea Review

Items in `03-Ideas/` older than 30 days:
```
These dev ideas have been sitting. Quick gut check:
1. "{title}" (45d) — still want this?
2. "{title}" (38d) — still relevant?
```

### Write Nudge Cache

Write JSON for the nudge system:
```bash
cat > /tmp/claude-nudge-cache.json << 'EOF'
{
  "inbox_count": N,
  "inbox_oldest_days": N,
  "stale_in_progress": ["item-1", "item-2"],
  "stale_in_progress_count": N,
  "ideas_over_30d": N,
  "parked_reminders_due": N,
  "personal_items": N,
  "business_items": N,
  "scatter_open": N,
  "scatter_active": N,
  "generated_at": "ISO 8601"
}
EOF
```

Write timestamp: `date -u +"%Y-%m-%dT%H:%M:%SZ" > /tmp/claude-last-morning-briefing`

### Quick Actions Menu

```
Quick actions:
- /vault-triage — clear {inbox_count} inbox items
- /vault-process — work the dev bug/task queue
- /brain-dump — capture what's on your mind (dev, business, personal, anything)
- /park — shelve something you're not doing today

What do you want to focus on?
```

---

## Step 10: Set Up Scheduled Automation

Check existing schedules via `CronList`.

If not already set up, create:

1. **Morning briefing** (weekdays 9am):
   ```
   CronCreate(schedule="3 9 * * 1-5", prompt="Good morning! Run /morning-briefing to start the day.", description="Daily morning briefing")
   ```

2. **Weekly vault sweep** (Monday 9:30am):
   ```
   CronCreate(schedule="27 9 * * 1", prompt="It's Monday — time for /vault-sweep. Check for stale items and escalate priorities.", description="Weekly vault sweep")
   ```

3. **Afternoon stale check** (weekdays 2pm):
   ```
   CronCreate(schedule="13 14 * * 1-5", prompt="Afternoon check: Run /vault-status and highlight anything blocked or stale for more than 7 days. Keep it brief.", description="Afternoon stale check")
   ```

If crons already exist, skip silently.
