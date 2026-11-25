---
name: vault-operator
description: |
  Read from and write to the AI Employee Obsidian vault. Process items in
  /Needs_Action, create plans in /Plans, update Dashboard.md, and move
  completed items to /Done. Use when directed to process the vault, handle
  pending tasks, or update the dashboard.
---

# Vault Operator

Interact with the AI Employee vault to process pending tasks and maintain state.

## Vault Layout

```
vault/
  Dashboard.md          ← Update after every session
  Company_Handbook.md   ← Read before acting; defines autonomy rules
  Inbox/                ← Drop folder (watched by filesystem_watcher.py)
  Needs_Action/         ← Items to process (written by watchers)
  Plans/                ← Write PLAN_*.md files here
  Done/                 ← Move completed items here (never copy, always move)
  Pending_Approval/     ← Write approval requests here for human review
  Logs/                 ← Append one JSON object per line per day
```

## Standard Workflow

### 1. Orient
```
Read vault/Company_Handbook.md   → recall autonomy rules
Read vault/Dashboard.md          → understand current state
List vault/Needs_Action/         → see what needs doing
```

### 2. Process Each Needs_Action Item
For every `.md` file in `/Needs_Action`:
1. Read the file and classify the requested action
2. Check `Company_Handbook.md` — is this auto-approved or does it need approval?
3. **Auto-approved** → create a Plan, execute, move to `/Done`
4. **Approval needed** → write an approval request to `/Pending_Approval/`, note it in Dashboard, stop

Never delete a Needs_Action file — always move it to `/Done` or `/Pending_Approval`.

### 3. Create a Plan
When a task requires multiple steps, write a plan first.

File naming: `Plans/PLAN_<description>_<YYYY-MM-DD>.md`

```markdown
---
created: <ISO timestamp>
status: in_progress
source: <Needs_Action filename>
---

## Objective
<One sentence describing the goal>

## Steps
- [x] Completed step
- [ ] Pending step

## Result
<Fill in when all steps are done>
```

### 4. Write an Approval Request
When a step requires human approval, write to `/Pending_Approval/`:

File naming: `Pending_Approval/APPROVAL_<description>_<YYYY-MM-DD>.md`

```markdown
---
type: approval_request
action: <email_send | payment | social_post | other>
created: <ISO timestamp>
expires: <ISO timestamp, typically +24h>
status: pending
---

## What I want to do
<Clear description of the proposed action>

## Why
<Reason / source task>

## To Approve
Move this file to vault/Approved/ (create folder if needed).

## To Reject
Move this file to vault/Rejected/ (create folder if needed).
```

### 5. Mark a Task Complete
When a task is fully done:
1. Update the Plan: set `status: done`, fill in `## Result`
2. Move the Needs_Action file to `Done/<original_filename>`
3. Move the Plan file to `Done/<plan_filename>`
4. Append a log entry to `Logs/YYYY-MM-DD.json`
5. Update `Dashboard.md`

### 6. Update Dashboard
Always update `Dashboard.md` at the end of every session:

```markdown
---
last_updated: <ISO timestamp>
---

# AI Employee Dashboard

## Status
- Watcher: ✅ Running  (or ⬜ Unknown / ❌ Stopped)
- Active Tasks: <count of .md files in Needs_Action (excluding .gitkeep)>
- Completed Today: <count of files moved to Done today>

## Pending Action
- FILE_report_2026-02-18_143000.md — new file dropped, awaiting review
- (or "None")

## Recent Activity
- [2026-02-18 14:32] Processed FILE_report_2026-02-18_143000.md → moved to Done
```

## Audit Log Format

Append one JSON object per line to `Logs/YYYY-MM-DD.json`:

```json
{"timestamp": "<ISO>", "action": "<description>", "source_file": "<filename>", "result": "success|skipped|pending_approval"}
```

Example:
```json
{"timestamp": "2026-02-18T14:32:00", "action": "processed file drop", "source_file": "FILE_report_2026-02-18_143000.md", "result": "success"}
```

## Quick Commands

```bash
# List pending tasks
ls vault/Needs_Action/

# Start the file system watcher
cd watchers && pip install -r requirements.txt
python filesystem_watcher.py ../vault

# Keep watcher alive with PM2
pm2 start watchers/filesystem_watcher.py --interpreter python3 -- vault
pm2 save && pm2 startup
```

## Typed Needs_Action Items

Some items have a `type:` field in their YAML frontmatter that signals a specific action:

### `type: briefing_request`
Auto-approved — read-only. Run the CEO briefing generator:

```bash
python .claude/skills/ceo-briefing/scripts/generate_briefing.py \
    --vault vault \
    --scope <daily|weekly>
```

The `scope` value comes from the frontmatter `scope:` field.
Output is written to `vault/Briefings/BRIEFING_<SCOPE>_<YYYY-MM-DD>.md`.
Move the Needs_Action file to `Done/` when complete.

### `type: file_drop`
Generic file dropped in Inbox. Read the file, determine appropriate action.

### `type: gmail_message`
New Gmail message — decide reply, approval request, or no-op.

### `type: linkedin_connection` / `type: linkedin_dm`
New LinkedIn activity — plan outreach or follow-up.

---

## Rules Summary (from Company_Handbook.md)

| Action                        | Auto-approved? |
|-------------------------------|----------------|
| Read any vault file           | ✅ Yes          |
| Create/update Plan files      | ✅ Yes          |
| Update Dashboard.md           | ✅ Yes          |
| Append to Logs                | ✅ Yes          |
| Move files within vault       | ✅ Yes          |
| Generate CEO briefing         | ✅ Yes (read-only) |
| Send email / message          | ❌ Needs approval |
| Any financial action          | ❌ Needs approval |
| Contact new people            | ❌ Needs approval |
| Delete files                  | ❌ Needs approval |
