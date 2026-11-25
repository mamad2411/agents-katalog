---
name: team-kanban
description: >
  This skill should be used when the user says "team kanban", "update the team board",
  "sync tasks to Jira", "what's the team working on", "team task board", "push tasks to Jira",
  "update the MOXY board", "team kanban update", "kanban sync", "team status board", or any
  request to aggregate action items into the team-visible Jira board. Also trigger when the
  user asks to "set up the team board" or references the MOXY board. This skill sweeps
  non-chat sources (Google Drive Active Tasks, Google Calendar, Gmail) for action items and
  files them into the Jira board (project MOXY) with best-practice issue authoring
  (Context/Acceptance/Notes descriptions, sub-items as real Subtasks, dependencies as issue
  links), then maintains board hygiene (priorities, In Review workflow, dedup against Done).
  Jira is the single canonical board — there is no vault kanban and no Slack digest.
---

# Team Kanban — Single Board on Jira (project MOXY)

**Jira (project MOXY, https://moxywolf.atlassian.net) is the single canonical task board.** This skill sweeps non-chat sources (Google Drive Active Tasks, Google Calendar, Gmail) for action items and files genuinely-new ones into MOXY, then keeps the board healthy (priorities, In Review workflow, dedup). Team members file their own tasks directly into Jira — including straight from Slack via the Jira Slack app — so there is no chat scraping and no digest to post.

> **Migration note (2026-07-16):** MoxyWolf retired the vault kanban (`KANBAN_VIEW.md`) and all Slack task flows. Jira is now the only board. Do not read or write a vault kanban, do not scrape Slack for action items, and do not post a #general digest. Older sessions that reference those are pre-migration.

---

## Team Roster

People who can be assigned tasks. Use the short name for reference and the Jira accountId (resolved once at setup via `lookupJiraAccountId` from the email, stored in the config note) for issue assignment.

| Name | Short Name | Email | Role |
|------|-----------|-------|------|
| Dorian Cougias | dorian | dorianc@moxywolf.com | Founder/CEO |
| Philip Mudhir | phil | philm@moxywolf.com | Core team |
| Steven P | steven | stevenp@moxywolf.com | Core team |
| Michael Flanagan | michael | michaelf@moxywolf.com | Core team |

Contractors can be assigned by name; if they have no Jira account, leave the issue unassigned and put their name in the description.

---

## Board Columns (Jira statuses)

| Column | Purpose |
|--------|---------|
| Backlog | Captured but not yet prioritized. New tickets (incl. those filed from Slack) land here by default. |
| P0 - Today | Max 3. Time-sensitive, blocks other work, or external deadline within 24h |
| P1 - This Week | Max 7. Important but not today-urgent; must move before Friday |
| Blocked | Waiting on external input. Include who/what is blocking and how long |
| In Progress | Actively being worked on right now |
| In Review | Marked complete by the assignee — awaiting confirmation before Done |
| Done | Confirmed complete. Clear weekly on Monday |

Statuses are **discovered, never assumed** — if a target status doesn't exist on the board, use the fallback label (`blocked`, `in-review`, priority labels) per `references/jira-board-mapping.md`. Priorities are expressed as labels + column position.

---

## Operating Modes

### Mode 1: Full Sync (default)

**Triggers:** "team kanban", "update the team board", "sync tasks to Jira", or the `/team-kanban` command.

#### Step 1: Load config + read the current board
Read the config note at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/team-kanban-config.md` (cloudId, project key MOXY, roster accountIds, discovered statuses, `last_standup_read`). Then read the live board: `searchJiraIssuesUsingJql` with `project = MOXY ORDER BY updated DESC` for open issues, plus `project = MOXY AND statusCategory = Done AND updated >= -14d` for recently-closed issues (the tombstone set for dedup). Jira is the source of truth for what's already tracked and what's already done.

#### Step 2: Sweep Google Drive Active Tasks
Fetch the `Daily Ops - Active Tasks` doc (Team Drive `0AHxJ5CazJqxOUk9PVA`, folder `1MjSabHDWYjjnp17DshdO9pnESLyvm6Gs`): `google_drive_search` (name contains 'Daily Ops - Active Tasks') → `google_drive_fetch`. Parse its P0/P1/P2/P3 sections into candidate task objects.

#### Step 3: Scan Google Calendar for today
`gcal_list_events` for today. Extract implicit commitments from prep-required meetings, review sessions, deadline events ("Prep for investor call at 3 PM" → P0 candidate). Don't duplicate what's already on the board.

#### Step 4: Scan Gmail for action items
`gmail_search_messages`, targeted queries: urgent threads (`is:inbox newer_than:1d (urgent OR deadline OR ASAP OR "action required")`), unanswered action items (`is:inbox newer_than:2d -from:me`), VIP contacts, and meeting summaries (`subject:"Meeting summary" newer_than:2d` → `gmail_read_message`, extract action items/owners/deadlines, match names to the roster). One email yielding several steps toward one deliverable is ONE task with `subtasks`; unrelated items are separate tasks.

Candidate task object:
```
{ title, priority: "p0|p1|backlog", project: "slug or null",
  assigned_to: "short-name or dorian (default)", waiting_on, waiting_since,
  context: "originating signal, who/when", subtasks: [ {title, done} ] }
```
Track the `source` (drive/calendar/gmail) internally for dedup only — **never render source tags on Jira issues.** Issues show title, project (label), assignee, and context.

#### Step 5: Merge, dedup, and reconcile against the board
Combine candidates. Resolution rules:

1. **Tombstone check first.** Match every candidate against (a) open MOXY issues and (b) the recently-Done set from Step 1, using >80% fuzzy title match (source/tags stripped). If a candidate matches a Done issue and its source-signal date is on or before that issue's resolution date, **suppress it** — the work is done and this is the same signal resurfacing. Only add it if the signal is genuinely newer (a real recurrence); note "recurs after prior completion on `<date>`" in context. When ambiguous, suppress and surface to Dorian's triage. (Team rule: `feedback_kanban_check_tombstones_before_readd.md`.)
2. Add only candidates with no matching open issue. If a candidate adds context to an existing issue (e.g. a new blocker), update that issue instead of creating a duplicate.
3. Enforce column limits: P0 max 3, P1 max 7. Over limit → flag for Dorian's triage; keep each issue's priority label and column in agreement.
4. Jira is authoritative for completion — an issue in Done/In Review is complete/in-review; never resurrect it.

#### Step 6: File and update issues on MOXY
Read `references/jira-board-mapping.md` for the full column/status/label mapping and issue-authoring standard.

- **New candidate** → `createJiraIssue` (type Task) authored to standard: imperative summary; description with **Context** (originating signal, who/when), **Acceptance** (observable done-state), and **Notes** (blockers, reviewer, deadlines) — fill every section the source allows. Every entry in `subtasks` becomes a real **Subtask** issue under the parent (its own summary/assignee/status; `Done` if flagged) — never a `[ ]` checklist in the description. Dependencies on other tracked work become issue links (`getIssueLinkTypes` → `createIssueLink`, type "Blocks"; the blocker is the *inward* side), not prose. New tickets default to **Backlog** (they are not auto-added to an active sprint).
- **Existing issue changed** (title, priority, assignee, labels, blocked context) → `editJiraIssue`; for column moves, `getTransitionsForJiraIssue` → `transitionJiraIssue`.
- **Update batching:** only touch issues that actually changed — an unchanged board is a no-op sync.
- **Bulk-creation gate:** if a sync would create more than 5 new issues at once (e.g. the first sync after setup), show Dorian the full list first and get explicit approval — a mass write to the shared tracker is team-visible.
- **Connector rejects an object parameter** (description/assignee/labels) → use the browser-REST fallback in `references/jira-board-mapping.md` § Connector Mechanics (Jira REST v3 via the writer's logged-in browser through Claude in Chrome).

**Assignees:** map short names to Jira accountIds from the config note. Contractors without accounts stay unassigned (name in description).

#### Step 7: In Review workflow
When an assignee moves their issue to Done, don't let it close unreviewed — move it to **In Review** and assign a reviewer:

- **Default review pairings:** Dorian↔Phil, Michael↔Steven.
- **Fallback:** if the default reviewer is unavailable or is the task's creator, use Dorian.
- Note the reviewer and a "since YYYY-MM-DD" date (today's sync date) on the issue so the morning standup can age the review. An issue moves In Review → Done only when the reviewer confirms by transitioning it in Jira.

The `last_standup_read` timestamp lives in the config note (not on the board); personal-os's morning standup reads it to filter Done/In Review to items changed since the last standup, and updates it. This sync leaves it untouched.

#### Step 8: Report
Summarize what changed: issues created, updated, moved, and anything flagged for triage (over-limit columns, ambiguous tombstones, contractors unassigned). No digest is posted anywhere — the board itself is the team-visible artifact.

### Mode 2: Quick Update
**Triggers:** "quick kanban update", "just refresh the board", "push current tasks to Jira".
Skip Steps 3–4 (calendar/email). Read the board + Google Drive Active Tasks, merge, file to Jira. Faster mid-day refresh.

### Mode 3: Setup
**Triggers:** "set up the team kanban", "initialize the kanban board", or the `/team-kanban-setup` command.

The first full sync bulk-writes to the shared tracker — gate it. Before the bulk create, show Dorian the exact issue list and destination (MOXY) and wait for explicit approval. Never auto-create in bulk.

1. **Verify Jira access:** `getAccessibleAtlassianResources` → cloudId; `getVisibleJiraProjects` → confirm **MOXY** visible, capture issue types (expect Task, Subtask).
2. **Resolve roster accountIds:** `lookupJiraAccountId` for each roster email; record for the config note.
3. **Check board statuses:** discover available statuses. If **Blocked** or **In Review** are missing, tell Dorian he can add those columns in Jira board settings for a 1:1 mapping; the sync degrades gracefully to labels if he doesn't.
4. **First full sync (after approval):** run Mode 1. Bulk-create shows the full issue list for approval first.
5. **Store config:** write `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/team-kanban-config.md` per the template in `references/jira-board-mapping.md` (cloudId, project key, board URL, discovered statuses, roster accountIds, column configuration, `last_standup_read`).
6. **Offer a scheduled task** for daily automated syncs (via the Cowork scheduled-tasks system).

---

## Finding existing config
Before creating anything, read `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/team-kanban-config.md`. If it has a cloudId + project key, verify with `getVisibleJiraProjects` (cheap read). If it has roster accountIds, use them directly. If missing or MOXY is unreachable, fall back to discovery or prompt for setup.

---

## Error Handling
- **Jira unreachable / Atlassian MCP not connected:** don't fake the sync. Save the merged candidate list to `MoxyWolf Vault/Tasks/team-kanban-latest.md`, note the gap, and tell Dorian the Atlassian connector needs attention.
- **Transition fails (status missing):** apply the fallback label per `references/jira-board-mapping.md` and note it in the report.
- **Connector rejects an object parameter:** expected — use the browser-REST fallback (§ Connector Mechanics).
- **Google Drive unreachable:** proceed with the board + other sources; note the gap in the report.
- **Column limits exceeded:** don't silently drop items. Flag the overflow: "P0 has 5 (limit 3). Triage needed."

## Restraint layer (ponytail)
Ingest the `/ponytail-debt` ledger: each `ponytail:` shortcut lacking an upgrade trigger becomes a tech-debt card on the board. See the `ponytail` skill — the YAGNI ladder (does it need to exist; stdlib before custom; native before dependency; one line before fifty), never cutting validation, error handling, security, or accessibility.
