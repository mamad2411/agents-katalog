---
name: crm-activity-sync
description: "Sync daily SE work activities (POC, Design, Workshops, Meetings, Ideations) into MSX CRM milestone activities. Reads activity-log.md from customer-engagements (populated by /daily-activity-log), maps each entry to the correct milestone, and creates CRM tasks. Runs on-demand or as a daily automation (Sun–Thu). Includes first-run onboarding, SSP/opportunity discovery, and failure recovery. Triggers include: 'crm activity', 'sync activities', 'log crm', 'update crm', 'crm tasks', 'activity sync', 'log my work', 'update milestones', 'what did I work on', or any request to push SE activities into MSX."
---

# /crm-activity-sync — CRM Activity Sync for Solution Engineers

Read structured activity logs from customer-engagements and push them into MSX CRM
(Dynamics 365) as milestone activities. This skill is the second stage of a two-stage
pipeline:

```
/daily-activity-log → activity-log.md → /crm-activity-sync → MSX CRM tasks
```

`/daily-activity-log` collects evidence (git repos, calendar, emails) and writes
`activity-log.md` in each project folder. This skill reads those logs, maps each
entry to the correct MSX milestone, and creates CRM tasks.

## Architecture: Pipeline Model

```
┌─────────────────────────┐     ┌──────────────────────────┐     ┌──────────┐
│  /daily-activity-log     │     │  customer-engagements/    │     │  MSX CRM │
│  (upstream skill)        │     │  (single source of truth) │     │          │
│                          │     │                           │     │          │
│  📦 Work repos (git)    │────▶│  activity-log.md          │     │          │
│  📅 Calendar events     │────▶│  meetings/                │────▶│  Tasks   │
│  📧 PG/Eng emails       │────▶│  followups.md             │     │          │
│  💬 Teams (future)      │────▶│  email-threads/ (future)  │     │          │
└─────────────────────────┘     └──────────────────────────┘     └──────────┘

 Runs daily at 07:30          Source of truth                  Runs daily at 08:00
```

**This skill reads ONLY from `customer-engagements/`.** It never directly queries
calendar, git repos, or email. That is `/daily-activity-log`'s job.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the right command syntax. See `_shared/PLATFORM.md` (skills repo root) for the full translation table. Quick reference:

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Run node script | `node ~/path/script.mjs` | `node $HOME/path/script.mjs` |
| Find node | `which node` | `Get-Command node` |
| Install node | `brew install node` (macOS) / pkg mgr (Linux) | `winget install OpenJS.NodeJS` |
| Run shell script | `bash ~/Scripts/x.sh` | `pwsh $HOME/Scripts/x.ps1` (provide PS1 alongside) |
| Home dir | `~` or `$HOME` | `$HOME` |

**VPN check note:** `~/Scripts/ensure-vpn.sh` is POSIX-only. On Windows, the user must connect Azure VPN Client manually before running this skill, or you must provide a PowerShell equivalent (`ensure-vpn.ps1`). If neither exists on Windows, ask the user to confirm VPN is connected and proceed.

Default to POSIX commands; fall back to PowerShell when running on Windows native (not WSL, not Git Bash).

## Core Principles

- **Single source of truth.** All activity evidence lives in `customer-engagements/`. This skill reads `activity-log.md` — nothing else. If an activity isn't logged there, it doesn't get synced to CRM.
- **Never fabricate activities.** Only create CRM tasks backed by entries in activity-log.md. If the log is empty for a date, create nothing.
- **Idempotent per daily activity.** Re-running the same source entry must not create
  another task, but work logged on different dates is new activity even when the
  subject, activity type, milestone, and scheduled-end month are identical.
- **Milestone-first.** Every CRM activity must link to a milestone via the `regardingobjectid` field. If no milestone exists, queue the activity locally and alert the user — never create an orphaned task.
- **User reviews before CRM writes.** In interactive mode, always present the proposed activities and get confirmation before creating anything. In automated mode, create activities and send a receipt summary.
- **Preserve source language.** Activity subjects and descriptions stay in their original language (English or Hebrew). Do not translate.
- **Portable by design.** No hardcoded user names, paths, or customer mappings. Everything is discovered at runtime via M365 profile + CRM queries + local folder scanning. Any team member with the prerequisites can run this skill.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Required Sibling Skills

This skill requires sibling skills from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|---|---|---|
| `/daily-activity-log` | Upstream — populates `activity-log.md` that this skill reads | ✅ Must run before this skill |
| `/customer-repo` | Scaffolds `customer-engagements/` folder structure | ✅ For initial setup |
| `/msx-crm` | CRM query tools (`run-tool.mjs`) for reading/writing MSX data | ✅ CRM backend |

Check if each required skill is installed:

```bash
# macOS / Linux
for skill in daily-activity-log customer-repo msx-crm; do
  [ -f "$HOME/.copilot/skills/$skill/SKILL.md" ] && echo "✅ $skill" || echo "❌ $skill MISSING"
done
```

```powershell
# Windows
foreach ($skill in @('daily-activity-log','customer-repo','msx-crm')) {
    if (Test-Path "$HOME\.copilot\skills\$skill\SKILL.md") { "✅ $skill" } else { "❌ $skill MISSING" }
}
```

**If ANY required skill is missing**, install all skills from the repository:

1. Clone the repo (skip if already cloned):
   ```bash
   # macOS / Linux
   [ -d "$HOME/customer-skills/.git" ] || git clone https://github.com/roie9876/clawpilot-skills.git "$HOME/customer-skills"
   ```
   ```powershell
   # Windows
   if (-not (Test-Path "$HOME\customer-skills\.git")) {
       git clone https://github.com/roie9876/clawpilot-skills.git "$HOME\customer-skills"
   }
   ```

2. Run the installer (idempotent — safe to re-run):
   ```bash
   # macOS / Linux
   bash "$HOME/customer-skills/scripts/install.sh"
   ```
   ```powershell
   # Windows
   pwsh "$HOME\customer-skills\scripts\install.ps1"
   ```

3. Verify the required skills are now installed. If still missing, stop and report the error.

### Required Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) |
|------|---------------|-----------------|-----------------|-------------------|
| Node.js | `node --version` | `Get-Command node` | `brew install node` | `winget install OpenJS.NodeJS` |
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |

Install any missing tools before proceeding. After installing Node.js, verify: `node --version`.

### CRM Tool Script (`run-tool.mjs`)

The CRM helper script must exist at `$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs`.

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" ] && echo "✅ CRM tools found" || echo "❌ CRM tools missing"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\msx-crm\crm-tools\run-tool.mjs") { "✅ CRM tools found" } else { "❌ CRM tools missing" }
```

If missing, clone the SE Kanban Tracker repo:

```bash
# macOS / Linux
git clone https://github.com/roie9876/crm-tools.git "$HOME/.copilot/skills/msx-crm/crm-tools"
cd "$HOME/.copilot/skills/msx-crm/crm-tools"
```

```powershell
# Windows
git clone https://github.com/roie9876/crm-tools.git "$HOME\.copilot\skills\msx-crm\crm-tools"
Set-Location "$HOME\.copilot\skills\msx-crm\crm-tools"; npm install
```

### VPN Connection

CRM is only accessible on Microsoft corpnet.

**macOS / Linux:** Run `$HOME/Scripts/ensure-vpn.sh` if it exists. If not, ask user to connect Azure VPN manually.

**Windows:** No automated VPN script. Ask user to confirm Azure VPN Client is connected.

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

### Additional Checks

| Prerequisite | How to check | If missing |
|---|---|---|
| `customer-engagements/` folder | `$HOME/customer-engagements/` exists with ≥1 customer | Run `/customer-repo` to scaffold |
| Config file | `$HOME/.copilot/crm-activity-sync/config.json` exists | Run `/crm-activity-sync setup` (Step 1) |
| Activity logs populated | `activity-log.md` exists in ≥1 project | Run `/daily-activity-log` first |

**Upstream dependency:** `/daily-activity-log` must run before `/crm-activity-sync`
to populate `activity-log.md`. If activity-log.md is missing or has no entry for the
target date, this skill reports "No activities logged for {date}. Run /daily-activity-log first."

## Commands

| Command | Purpose |
|---|---|
| `/crm-activity-sync` | Sync yesterday's logged activities to CRM (interactive) |
| `/crm-activity-sync setup` | First-run onboarding — discover profile, customers, SSPs, milestones |
| `/crm-activity-sync week` | Sync the current work week (Sun–Thu) |
| `/crm-activity-sync range <start> <end>` | Sync a custom date range (ISO dates) |
| `/crm-activity-sync status` | Show config, pending queue, last sync date |
| `/crm-activity-sync remap` | Re-run milestone mapping for a customer/project |
| `/crm-activity-sync watch` | Check for new opportunities from known SSPs |
| `/crm-activity-sync retry` | Retry all pending (failed/queued) activities |

## File Locations

| File | Purpose |
|---|---|
| `~/.copilot/crm-activity-sync/config.json` | User profile, SSP list, customer coverage, preferences |
| `~/customer-engagements/{customer}/crm-mapping.json` | Per-customer: opportunity + milestone + project + work repo mappings |
| `~/customer-engagements/{customer}/projects/{project}/activity-log.md` | Daily activity log (written by /daily-activity-log, read by this skill) |
| `~/.copilot/crm-activity-sync/pending.json` | Queue of activities that couldn't be synced (no milestone, CRM error, etc.) |
| `~/.copilot/crm-activity-sync/sync-log.json` | History of synced activities (for idempotency and audit) |

## CRM Tool Path

All CRM operations use the existing tool runner:

```bash
~/Scripts/ensure-vpn.sh --quiet
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs <tool-name> '<json-params>'
```

**Important:** The CRM tool currently supports **read-only** operations. Before this
skill can create activities, `run-tool.mjs` must be extended with a `create_task`
tool. See [Phase 0: CRM Write Tool](#phase-0-crm-write-tool) below.

---

## Step 0: Environment Check

Run before every sync operation.

1. **VPN:** Run `~/Scripts/ensure-vpn.sh --quiet`. If exit code ≠ 0:
   - Log: "⚠️ VPN not connected. CRM operations will fail."
   - If interactive → ask user to connect manually.
   - If automated → queue all activities to `pending.json`, send Teams notification: "CRM activity sync skipped — VPN down."
   - Stop.

2. **CRM auth:** Run `node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_auth_status`.
   - If `authenticated: false` → same behavior as VPN failure.

3. **Config:** Check `~/.copilot/crm-activity-sync/config.json` exists.
   - If missing → run Step 1 (setup) automatically.

4. **Activity logs exist:** Check that at least one `activity-log.md` file exists across projects.
   - If none exist → prompt: "No activity logs found. Run `/daily-activity-log` first to populate them."
   - In automated mode → send Teams notification and stop.

---

## Step 1: First-Run Setup (`/crm-activity-sync setup`)

This step runs once to bootstrap the configuration. Re-run anytime to update.

### 1a. Discover User Identity

```
m365_get_my_profile → displayName, mail, jobTitle, department, officeLocation
m365_get_my_manager → manager name, email, title
CRM: crm_whoami → UserId (CRM system user GUID)
```

Store in config:
```json
{
  "user": {
    "name": "Roie Ben Haim",
    "email": "robenhai@microsoft.com",
    "initials": "RBH",
    "jobTitle": "Azure Specialist SE",
    "department": "IL-Spec Sales",
    "officeLocation": "HERZLIYA-AT3",
    "crmUserId": "<GUID from WhoAmI>",
    "manager": {
      "name": "Ido Katz",
      "email": "idokatz@microsoft.com"
    }
  }
}
```

**Initials derivation:** Take the first letter of each word in the display name,
uppercase. "Roie Ben Haim" → "RBH". Confirm with user — they may prefer different
initials (e.g., "RB" instead of "RBH").

### 1b. Discover Customers and Projects

Scan the local customer-engagements folder:

```bash
ls ~/customer-engagements/
```

For each customer folder found:
1. Read `~/customer-engagements/{customer}/README.md` — extract customer display name.
2. Read `~/customer-engagements/{customer}/stakeholders.md` — extract Microsoft account team members (SSPs, account leads).
3. List `~/customer-engagements/{customer}/projects/` — each subfolder is a project.
4. For each project, read `projects/{project}/README.md` — extract project type (POC, ADS, etc.) and status.

### 1b-2. Classify Customers: Core vs. Temp

During setup, ask the user:

1. **"Who are your dedicated SSPs?"** — These are the field sellers you work with daily.
2. **"Which customers are you actively covering?"** — These become **core** customers.

Any customer folder in `~/customer-engagements/` that is NOT listed as core is classified as **temp**.

**Core customers:**
- Always scanned for activities during daily sync.
- Their SSPs are watched for new opportunities (`/crm-activity-sync watch`).
- Persist indefinitely in the config.

**Temp customers:**
- Scanned for activities the same way as core (customer-engagements is always source of truth).
- Their SSPs are NOT watched for new opportunities.
- After `preferences.temp_archive_days` (default 14) with no new activity, the sync prompts: "No activity with {customer} for {N} days. Archive this temp engagement?"
- Archiving sets `customer_type: "archived"` in `crm-mapping.json` — stops scanning but preserves history.

**Classification is stored in `crm-mapping.json`:**
```json
{
  "customer_type": "core",  // or "temp" or "archived"
  "temp_reason": "Urgent help request via Ido Katz",  // only for temp
  "temp_started": "2026-04-20"  // only for temp
}
```

**Discovery of new temp customers:**
When `/daily-activity-log` detects a calendar meeting with an external domain not matching any existing `crm-mapping.json`, it alerts:
- "Meeting detected with unknown customer domain: clal-ins.co.il. Is this: A) A new core customer, B) A temp engagement, C) Not customer work (skip)"

### 1c. Match Customers to MSX Accounts + Opportunities

For each discovered customer:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs list_opportunities '{"customerKeyword":"<customer-name>"}'
```

Present the matches to the user:
```
Found for "checkpoint":
  1. Checkpoint - SASE (opportunityid: xxx, owner: Kobi Shitrit)
  2. Checkpoint - CloudGuard (opportunityid: yyy, owner: ...)
Which opportunities are you actively working on?
```

For each confirmed opportunity, fetch milestones:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs get_milestones '{"opportunityId":"<opp-id>","statusFilter":"active"}'
```

### 1d. Build Per-Customer Mapping

Write `~/customer-engagements/{customer}/crm-mapping.json`:

```json
{
  "customer_display_name": "CheckPoint",
  "customer_slug": "checkpoint",
  "account_name": "CHECK POINT SOFTWARE TECHNOLOGIES LTD",
  "account_id": "<GUID>",
  "ssps": [
    {
      "name": "Kobi Shitrit",
      "email": "kobishitrit@microsoft.com",
      "role": "Account Lead",
      "crm_user_id": "<GUID>"
    }
  ],
  "projects": {
    "sase": {
      "display_name": "SASE",
      "project_type": "POC",
      "opportunity_id": "<GUID>",
      "opportunity_name": "Checkpoint - SASE",
      "milestones": [
        {
          "milestone_id": "<GUID>",
          "milestone_number": "7-502749008",
          "milestone_name": "SASE POC",
          "milestone_status": "On Track",
          "is_primary": true
        }
      ],
      "default_activity_type": "POC",
      "subject_keywords": ["sase", "checkpoint", "aks", "dpdk"],
      "work_repos": [
        {
          "path": "/Users/robenhai/SASE",
          "label": "SASE Design & POC",
          "added": "2026-04-23"
        }
      ]
    }
  },
  "last_refreshed": "2026-04-23T08:00:00Z"
}
```

**Mapping rules:**
- Each project maps to exactly one opportunity (1:1).
- A project may have multiple milestones (e.g., "SASE ADS" and "SASE POC"). Mark one as `is_primary` — this is the default target for activities.
- `subject_keywords` are used by `/daily-activity-log` to match calendar events to projects.
- `default_activity_type` is the fallback when classification is ambiguous.
- `work_repos` are registered manually — not every project has a repo. Used by `/daily-activity-log` to scan git history.

### 1e. Discover SSPs

For each confirmed opportunity:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_query '{
  "entitySet": "msp_dealteams",
  "filter": "_msp_opportunityid_value eq '\''<opportunity-id>'\''",
  "select": "_msp_userid_value,msp_role",
  "top": 50
}'
```

Cross-reference with stakeholders.md to identify SSPs (Solution Sales Professionals),
ATU members, and other field roles. Store in the `ssps` array of `crm-mapping.json`.

Also store the aggregated SSP list in the global config for opportunity watching:

```json
{
  "known_ssps": [
    {
      "name": "Kobi Shitrit",
      "email": "kobishitrit@microsoft.com",
      "crm_user_id": "<GUID>",
      "customers": ["checkpoint"]
    }
  ]
}
```

### 1f. Set Preferences

Ask the user:

1. **Sync mode:** Interactive (review before creating) or Auto (create + receipt)?
   - Default: Interactive.
2. **Scheduling:** Manual only, or daily automation (Sun–Thu)?
   - If daily: what time? Default: 08:00 IST.
3. **Activity naming convention:**
   - Default: `{initials} - {type}` (e.g., "RBH - POC"). Matches the pattern in the screenshot.
   - Option: `{initials} - {type} - {description}` (e.g., "RBH - POC - AKS Architecture Review").
4. **Which data sources to scan:** Calendar (always on), customer-engagements (always on), Teams (optional), Kanban (optional).

Store preferences in config:

```json
{
  "preferences": {
    "sync_mode": "interactive",
    "schedule": "daily",
    "schedule_time": "08:00",
    "schedule_days": ["sunday", "monday", "tuesday", "wednesday", "thursday"],
    "subject_format": "{initials} - {type}",
    "data_sources": ["calendar", "customer-engagements", "teams"],
    "auto_retry_pending": true
  }
}
```

### 1g. Confirm and Save

Present a summary of the entire config to the user:
```
✅ Setup complete!

User: Roie Ben Haim (RBH), Azure Specialist SE
Manager: Ido Katz
CRM User ID: xxx

Customers:
  • CheckPoint → Checkpoint - SASE → Milestone: SASE POC (7-502749008)
  • Clal Insurance → [opportunity TBD]
  • Sapiens → [opportunity TBD]

SSPs watching: Kobi Shitrit (checkpoint)
Sync mode: Interactive
Schedule: Daily Sun–Thu at 08:00

Ready to sync? Run /crm-activity-sync
```

---

## Step 2: Read Activity Logs

This is the core data-reading phase. For a target date (or date range), scan all
customer projects for logged activities.

**Default target:** Yesterday, adjusted for Israeli work week.
- If today is Sunday → yesterday was Saturday (weekend) → use Thursday.
- If today is Friday/Saturday → use Thursday.
- Otherwise → use yesterday.

### 2a. Scan All Projects

```bash
find ~/customer-engagements/*/projects/*/activity-log.md -type f 2>/dev/null
```

For each `activity-log.md` found:
1. Parse the file for `## <target-date>` headers.
2. If a matching date header exists → extract the full entry (everything between
   this `## ` header and the next `## ` header or `---` separator).
3. If no matching date → skip this project.

### 2b. Parse Each Entry

From each daily entry, extract:

| Field | Source in activity-log.md | Required? |
|---|---|---|
| **Activity type** | `**Type:** Design` line | ✅ |
| **Sources** | `**Sources:** repo (21 commits), email (1 PG thread)` line | ✅ |
| **Summary** | `### Summary` section — the 2-4 sentence description | ✅ |
| **Repo details** | `### Repo Work` section — commit count, topics | Optional (enriches description) |
| **Meeting details** | `### Meetings` section — attendees, subjects | Optional (enriches description) |
| **Engineering coordination** | `### Engineering Coordination` section | Optional (enriches description) |

### 2c. Build Activity List

Produce a list of activities to sync:

```
[
  {
    customer: "checkpoint",
    project: "sase",
    date: "2026-04-21",
    activity_type: "Design",
    summary: "Full design sprint for SASE — 10 architecture areas...",
    sources: "repo (21 commits)",
    already_synced: false  // checked against sync-log.json
  },
  ...
]
```

**If zero activities found across all projects** → report: "No activities logged for {date}. Run /daily-activity-log first." Stop.

---

## Step 3: Map Activities to Milestones

For each activity in the list:

1. **Load CRM mapping** — read `~/customer-engagements/{customer}/crm-mapping.json`.
   - If missing → queue with reason `no_crm_mapping`.

2. **Find the project** — look up `projects.{project}` in the mapping.
   - If missing → queue with reason `project_not_mapped`.

3. **Select milestone** — use the `is_primary: true` milestone for the project.
   - If the project has multiple milestones, check if the activity type matches
     a milestone name more closely (e.g., "Workshop" activity + milestone named
     "SASE Workshop" → use that one).

4. **Validate milestone is still active** — query CRM to confirm:
   ```bash
   node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs get_milestones '{"milestoneId":"<milestone-id>"}'
   ```
   Check `msp_milestonestatus` is in the active set (Not Started, On Track, In Progress, Blocked, At Risk).

5. **Handle missing/closed milestones:**

   | Scenario | Action |
   |---|---|
   | Milestone exists and is active | ✅ Proceed to Step 4 |
   | Milestone exists but is completed/closed | ⚠️ Alert: "Milestone {name} is closed. Create activity anyway, or skip?" |
   | No milestone for this project | 🔴 Queue to `pending.json` with reason `no_milestone`. Alert: "No active milestone for {customer}/{project}. Ask {ssp} to create one?" |
   | No opportunity for this customer | 🔴 Queue with reason `no_opportunity`. Alert: "No MSX opportunity found for {customer}." |

---

## Step 4: Create CRM Activities

### 5a. Prepare Activity Payload

For each activity to create, build the CRM task record:

```json
{
  "subject": "RBH - POC",
  "description": "SASE architecture review with CheckPoint — discussed AKS networking gaps, SRv6 encapsulation options, and multi-NIC requirements.",
  "scheduledend": "2026-04-30T08:00:00Z",
  "msp_taskcategory": 861980005,
  "regardingobjectid_msp_engagementmilestone@odata.bind": "/msp_engagementmilestones(<milestone-id>)"
}
```

**Field mapping:**

| CRM Field | Source | Notes |
|---|---|---|
| `subject` | `{initials} - {type}` from preferences | E.g., "RBH - POC" |
| `description` | Activity date marker + auto-generated summary from activity-log.md `### Summary` section | Start with `Activity date: YYYY-MM-DD`, then keep the summary concise: 1-3 sentences with customer name, topic, and key work done. |
| `scheduledend` | End of current month at 08:00 UTC (11:00 IST), OR milestone due date if sooner | Matches the pattern seen in the screenshot (4/30/2026 11:00 AM). If the milestone has a `msp_milestonedate`, use the earlier of: milestone date or end-of-month. |
| `msp_taskcategory` | Activity type → CRM enum (see table below) | Maps our activity classification to CRM picklist values. |
| `regardingobjectid` | Milestone GUID | Binds the task to the milestone via OData relationship. |

**`msp_taskcategory` Mapping — All 20 Categories:**

The `**Type:**` line in `activity-log.md` uses the exact CRM label. This skill maps
it directly to the `msp_taskcategory` integer value:

| CRM Label (from activity-log.md `Type:` field) | `msp_taskcategory` Value |
|---|---|
| ACE | `606820000` |
| Architecture Design Session | `861980004` |
| Blocker Escalation | `861980006` |
| Briefing | `861980008` |
| Call Back Requested | `861980010` |
| Consumption Plan | `861980007` |
| Cross Segment | `606820001` |
| Cross Workload | `606820002` |
| Customer Engagement | `861980000` |
| Demo | `861980002` |
| External (Co-creation of Value) | `861980013` |
| Internal | `861980012` |
| Negotiate Pricing | `861980003` |
| New Partner Request | `861980011` |
| PoC/Pilot | `861980005` |
| Post Sales | `606820003` |
| RFP/RFI | `861980009` |
| Tech Support | `606820004` |
| Technical Close/Win Plan | `606820005` |
| Workshop | `861980001` |

If the `Type:` value from `activity-log.md` doesn't match any CRM label exactly,
fall back to the project's `default_activity_type` from `crm-mapping.json`. If
that's also missing, default to `Customer Engagement` (`861980000`).

**Subject format options (from config `subject_format`):**
- `{initials} - {type}` → "RBH - POC" (matches screenshot pattern)
- `{initials} - {type} - {description}` → "RBH - POC - AKS Architecture Review"
- `{initials} - {type} ({date})` → "RBH - POC (Apr 22)"

**Subject `{type}` short labels** (for readability in CRM):

| CRM Label | Short label for subject |
|---|---|
| Architecture Design Session | ADS |
| PoC/Pilot | POC |
| Workshop | Workshop |
| Customer Engagement | Meeting |
| Briefing | Briefing |
| Blocker Escalation | Escalation |
| Demo | Demo |
| Internal | Internal |
| ACE | ACE |
| Consumption Plan | Consumption |
| RFP/RFI | RFP |
| Tech Support | Support |
| Technical Close/Win Plan | Close Plan |
| Post Sales | Post Sales |
| Negotiate Pricing | Pricing |
| New Partner Request | Partner |
| Cross Segment | Cross-Seg |
| Cross Workload | Cross-WL |
| Call Back Requested | Callback |
| External (Co-creation of Value) | Co-creation |

### 5b. Idempotency Check

Build a stable source key for each parsed daily entry:

```text
{activity-date}|{customer}|{project}|{subject}|{milestone-id}
```

Check `sync-log.json` for that exact key before creating the task. Also include
`Activity date: YYYY-MM-DD` in the CRM task description so the source date is
preserved and can be used for recovery if the local sync log is unavailable.

A task is a duplicate only when it represents the **same source activity date,
customer, project, subject, and milestone**. A same-subject task from another day
or another month is not a duplicate and must not be skipped. For example, daily
`RBH - POC` entries on the same milestone are separate CRM activities when their
activity dates differ.

Before creating, optionally query milestone activities for recovery:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs get_milestone_activities '{"milestoneId":"<milestone-id>"}'
```

Only treat a CRM result as a recovered duplicate when its subject matches and its
description contains the same `Activity date: YYYY-MM-DD` marker. Never deduplicate
by subject or scheduled-end month alone.

If the exact source key or date marker matches:
- Interactive: "This exact daily activity is already synced. Skip or update?"
- Auto: Skip and retain the existing task ID in `sync-log.json`.

### 5c. Ensure Deal Team Membership

Before creating any task on a milestone, verify the user is on the deal team for
the parent opportunity. If not, auto-add them.

**Check membership:**

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_query '{
  "entitySet": "msp_dealteams",
  "filter": "_msp_parentopportunityid_value eq '"'"'<opportunity-id>'"'"' and _msp_dealteamuserid_value eq '"'"'<user-crm-id>'"'"' and statecode eq 0",
  "select": "msp_dealteamid",
  "top": 1
}'
```

- If count > 0 → already on team, proceed to task creation.
- If count == 0 → **auto-add to deal team:**

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_query '{
  "method": "POST",
  "entitySet": "msp_dealteams",
  "body": {
    "msp_dealteamuserid@odata.bind": "/systemusers(<user-crm-id>)",
    "msp_parentopportunityid@odata.bind": "/opportunities(<opportunity-id>)"
  }
}'
```

On success:
- Log: "Added {user} to deal team for {opportunity-name}."
- Cache in `crm-mapping.json`: `"deal_team_verified": true` on the project.
- Proceed to task creation.

On failure (403/permissions):
- Interactive: "Cannot auto-join deal team for {opp}. Ask SSP ({ssp-name}) to add you."
- Auto: send Teams message to user with the SSP name. Queue activity in `pending.json`.

**Cache the check.** Once verified, set `"deal_team_verified": true` in the project's
`crm-mapping.json` entry. Skip the check on subsequent syncs unless the opportunity
changes. Reset to `false` if the opportunity ID changes or a task creation fails
with a permissions error.

### 5d. Create the Task

**This requires the `create_task` tool in `run-tool.mjs` (see Phase 0).**

**Parse duration from activity-log.md:** Extract the number from the `**Duration:**`
line (e.g., `**Duration:** 285 min (4h 45m) — ...` → `285`). Pass as
`duration` (the tool maps it to `actualdurationminutes` internally).

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs create_task '{
  "subject": "RBH - POC",
  "description": "...",
  "scheduledend": "2026-04-30T08:00:00Z",
  "milestoneId": "<milestone-guid>",
  "taskcategory": 861980005,
  "duration": 285
}'
```

**Duration field mapping:**
- `duration` — maps to `actualdurationminutes` CRM field internally
- Value in minutes, rounded to nearest 15 by `/daily-activity-log`
- If `**Duration:**` line is missing from activity-log.md (older entries), omit
  the field — CRM will use its default

On success:
- Log to `sync-log.json` with the created task ID.
- In interactive mode: "✅ Created 'RBH - POC' on milestone SASE POC."
- In auto mode: append to receipt.

On failure:
- If **permissions error** → deal team membership may have been revoked. Reset
  `deal_team_verified` to false, retry Step 5c, then retry task creation.
- Save to `pending.json` with error details.
- In interactive mode: show error and ask to retry.
- In auto mode: send Teams notification.

### 5d. Present Summary

After all activities are processed, show a summary:

```
📋 CRM Activity Sync — April 22, 2026

Created:
  ✅ RBH - POC → SASE POC (CheckPoint) — AKS architecture review
  ✅ RBH - Design → AI Search ADS (Clal Insurance) — Agent infrastructure discussion

Skipped (already exists):
  ⏭️ RBH - Meeting Call → SASE POC (CheckPoint) — duplicate

Pending (no milestone):
  🔴 Sapiens / Digital-AI — no active milestone. Queued.

Run /crm-activity-sync retry after milestone is created.
```

---

## Step 5: Milestone Scanner and Opportunity Watch

This step runs as part of every sync. It serves three purposes:
1. **Find new opportunities** from core SSPs where you're not on the deal team.
2. **Find new milestones** on tracked opportunities.
3. **Resolve orphaned activities** from the pending queue.

### 5a. Scan Core SSP Opportunities

For each SSP in `config.json → core_ssps`:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_query '{"entitySet":"opportunities","filter":"_ownerid_value eq '"'"'<ssp-crm-user-id>'"'"' and statecode eq 0","select":"opportunityid,name,_parentaccountid_value,createdon","orderby":"createdon desc","top":20}'
```

Compare against known opportunities in all `crm-mapping.json` files. If an opportunity is:
- Owned by a core SSP
- For an account that matches a customer you cover
- NOT already in any `crm-mapping.json`
- Created in the last 30 days (or new since last check)

Then alert:
```
🔔 New opportunity detected!
  "Checkpoint - CloudGuard" by Kobi Shitrit
  → Add to your tracking? (Yes / Skip)
```

### 5b. Refresh Milestones on Tracked Opportunities

For each opportunity in all `crm-mapping.json` files:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs get_milestones '{"opportunityId":"<opp-id>","statusFilter":"active"}'
```

Compare against milestones currently in the mapping:
- **New milestone found** → "New milestone 'SASE Workshop' on Checkpoint - SASE. Add to mapping?"
- **Milestone status changed** (e.g., On Track → Completed) → update the mapping.
- **Milestone that was missing now exists** → check if any pending activity matches.

### 5c. Resolve Orphaned Activities

For each pending activity with reason `no_milestone`:

1. **Check mapped opportunity** — query milestones again (SSP may have created one since last check).
2. **If still no milestone on mapped opp** — broaden search to ALL active opportunities for the customer account:
   ```bash
   node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs list_opportunities '{"customerKeyword":"<customer-name>"}'
   ```
   Then get milestones for each:
   ```bash
   node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs get_milestones '{"opportunityId":"<opp-id>","statusFilter":"active"}'
   ```

3. **Score each discovered milestone** for the pending activity:
   - Milestone name contains project keyword? +3
   - Milestone category matches activity type (e.g., POC → POC/Pilot category)? +2
   - Milestone owner is a known SSP? +1
   - Milestone date is in the future? +1

4. **If best score ≥ 3** → suggest: "Your pending {customer}/{project} activity might match milestone '{name}' on '{opportunity}'. Map it?"
5. **If best score < 3** → no good match. In interactive mode: "No milestone found for {customer}/{project}. Notify SSP ({ssp_name}) to create one?"
6. **If resolved** → update `crm-mapping.json` with the new milestone, create the CRM task, move from pending to sync-log.

### 5d. When Does the Scanner Run?

| Trigger | Scope | Depth |
|---|---|---|
| Every daily CRM sync | Core customers only | Lightweight: check mapped opps only |
| `/crm-activity-sync watch` | All customers | Full: scan all account opps |
| Processing pending items | Per-customer | Full: broaden to all account opps |
| `/crm-activity-sync remap` | Specific customer | Full: re-discover everything |

---

## Step 6: Pending Queue Management

### pending.json Structure

```json
[
  {
    "id": "pending-001",
    "customer": "sapiens",
    "project": "digital-ai",
    "date": "2026-04-22",
    "activity_type": "Meeting Call",
    "subject": "RBH - Meeting Call",
    "description": "Digital AI overview session",
    "reason": "no_milestone",
    "evidence": {
      "calendar_event_id": "AAMkAGI2...",
      "meeting_note": "~/customer-engagements/sapiens/projects/digital-ai/meetings/2026-04-22-digital-ai-overview.md"
    },
    "created_at": "2026-04-23T08:00:00Z",
    "retry_count": 0,
    "last_retry": null
  }
]
```

### Retry Logic (`/crm-activity-sync retry`)

1. Load `pending.json`.
2. For each pending item:
   a. Re-check the reason:
      - `no_milestone` → query milestones again. If one now exists → proceed to create.
      - `no_opportunity` → query opportunities again.
      - `crm_error` → retry the create operation.
      - `vpn_down` / `auth_failed` → check VPN/auth, retry if resolved.
   b. If resolved → create the task, move from pending to sync-log.
   c. If still blocked → increment `retry_count`, update `last_retry`.
3. Report results.

### Auto-Retry

If `preferences.auto_retry_pending` is true, every daily sync run starts by
retrying pending items before processing new activities.

### Stale Pending Cleanup

Items pending for >30 days are flagged:
```
⚠️ Stale pending items (>30 days):
  - Sapiens / Digital-AI (Apr 22) — no_milestone — 31 days pending
  Archive or escalate?
```

---

## Failure Scenarios

| Failure | Detection | Impact | Mitigation |
|---|---|---|---|
| **VPN down** | `ensure-vpn.sh` exit ≠ 0 | All CRM ops fail | Auto-connect attempt → queue if still down → Teams alert |
| **CRM auth expired** | `crm_auth_status` → false | All CRM ops fail | CRM client auto-retries with fresh token; if persistent → queue + alert |
| **CRM rate limit (429)** | HTTP 429 from CRM | Writes throttled | CRM client has built-in backoff; batch creates with 1s delay between |
| **CRM write fails (403)** | HTTP 403 on POST | Task not created | Queue to pending with error; may need SSP to grant permissions on milestone |
| **CRM write fails (500)** | HTTP 500 on POST | Task not created | Retry once after 5s; if still fails → queue |
| **No milestone** | Milestone query returns empty | Can't link activity | Queue with reason `no_milestone`; alert user to request milestone creation |
| **Duplicate activity** | Exact source key or activity-date marker matches | Redundant retry of the same daily entry | Skip silently (auto) or ask (interactive); never deduplicate different work dates by subject/month |
| **Wrong milestone mapping** | User reports error | Activity on wrong milestone | Run `/crm-activity-sync remap {customer}/{project}` to fix; note: CRM task may need manual move |
| **Customer-engagements missing** | Folder doesn't exist | No local data source | Fall back to calendar-only mode |
| **M365 not signed in** | `m_m365_status` check | No calendar/Teams data | Prompt sign-in (interactive) or skip + alert (auto) |
| **Calendar empty** | No events returned | No calendar activities | Check customer-engagements for file changes as fallback |
| **Config stale** | `last_refreshed` >30 days old | Mappings may be wrong | Warn user; suggest re-running setup |
| **SSP changed** | Opportunity owner changed in CRM | Watch alerts stop | Weekly config refresh detects owner change |
| **Network timeout** | CRM request times out | Individual op fails | Built-in retry (3x for writes); queue if persistent |

---

## Phase 0: CRM Write Tool

**This must be implemented before the skill can create activities.**

Add `create_task` to `~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs`:

```javascript
async create_task({ subject, description, scheduledend, milestoneId, taskcategory, ownerId }) {
  if (!subject) error('subject is required');
  if (!milestoneId) error('milestoneId is required');
  const nid = normalizeGuid(milestoneId);
  if (!isValidGuid(nid)) error('Invalid milestoneId GUID');

  const body = {
    subject,
    ...(description && { description }),
    ...(scheduledend && { scheduledend }),
    ...(taskcategory && { msp_taskcategory: taskcategory }),
    'regardingobjectid_msp_engagementmilestone@odata.bind':
      `/msp_engagementmilestones(${nid})`
  };

  // If ownerId provided, bind it; otherwise CRM defaults to current user
  if (ownerId) {
    const oid = normalizeGuid(ownerId);
    if (isValidGuid(oid)) {
      body['ownerid@odata.bind'] = `/systemusers(${oid})`;
    }
  }

  const result = await crm.request('tasks', {
    method: 'POST',
    body
  });

  if (!result.ok) {
    error(`Create task failed (${result.status}): ${result.data?.message}`);
  }

  // Extract the created task ID from the OData-EntityId header or response
  const taskId = result.data?.activityid || 'created (ID not returned)';
  return { success: true, taskId, subject };
}
```

Also add `update_task` for future use (updating description, closing tasks):

```javascript
async update_task({ taskId, subject, description, scheduledend, statuscode, statecode }) {
  if (!taskId) error('taskId is required');
  const nid = normalizeGuid(taskId);
  if (!isValidGuid(nid)) error('Invalid taskId GUID');

  const body = {};
  if (subject !== undefined) body.subject = subject;
  if (description !== undefined) body.description = description;
  if (scheduledend !== undefined) body.scheduledend = scheduledend;
  if (statuscode !== undefined) body.statuscode = statuscode;
  if (statecode !== undefined) body.statecode = statecode;

  if (!Object.keys(body).length) error('No fields to update');

  const result = await crm.request(`tasks(${nid})`, {
    method: 'PATCH',
    body
  });

  if (!result.ok) {
    error(`Update task failed (${result.status}): ${result.data?.message}`);
  }

  return { success: true, taskId: nid };
}
```

**Testing the write tools:**
1. First test with `crm_whoami` to confirm auth.
2. Create a test task on a known milestone with a clearly-marked test subject.
3. Verify it appears in MSX UI.
4. Delete or close the test task.

---

## Automation Setup

If the user opts for daily scheduling during setup, create **two** Clawpilot automations:

```
Automation 1: Daily Activity Log
Schedule: Every weekday at 07:30 (Sun-Thu Israel time)
Prompt: |
  Run /daily-activity-log for yesterday.
  Process all customers. Skip already-logged dates.
  If new entries were created, send a brief Teams summary.
  If errors occur, include them in the summary.
```

```
Automation 2: CRM Activity Sync
Schedule: Every weekday at 08:00 (Sun-Thu Israel time)
Prompt: |
  Run /crm-activity-sync for yesterday.
  Mode: auto (create activities without asking, send receipt summary).
  If VPN is down, queue activities and notify me via Teams.
  If any activities were created, send a Teams summary.
  If any activities are pending, include them in the summary.
  Also run /crm-activity-sync watch to check for new opportunities.
```

Use `m_create_automation` with:
- `schedule`: "every sunday at 7:30am", "every monday at 7:30am", etc. (for activity log) and 8:00am versions (for CRM sync).
- `triggerType`: "schedule"
- `oneShot`: false

**The 30-minute gap** between 07:30 and 08:00 ensures `/daily-activity-log` finishes
populating `activity-log.md` before `/crm-activity-sync` reads it.

**Note on Israeli work week:** Sunday–Thursday. The automations should NOT run on
Friday or Saturday. Clawpilot's `work-hours` schedule option assumes Mon–Fri,
so use explicit day-based scheduling instead.

---

## Making This Skill Generic

### For Other Team Members

When another team member wants to use this skill:

1. **Install prerequisites:**
   - Clawpilot with M365 signed in.
   - CRM tools: `~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs` + MCAPS-IQ library.
   - VPN script: `~/Scripts/ensure-vpn.sh`.
   - At least one customer-engagements folder (via `/customer-repo`).

2. **Run setup:** `/crm-activity-sync setup` auto-discovers everything from their M365 profile and CRM access. No hardcoded values.

3. **Differences per team member:**
   - Different initials, different customers, different SSPs.
   - Same skill logic, same file structure.
   - Config is per-user (`~/.copilot/crm-activity-sync/config.json`).
   - Mappings are per-customer-repo (`crm-mapping.json`).

### Portability Checklist

- [ ] No hardcoded email addresses (discovered via `m365_get_my_profile`)
- [ ] No hardcoded customer names (discovered via folder scan + CRM query)
- [ ] No hardcoded milestone IDs (discovered via CRM query)
- [ ] No hardcoded CRM user IDs (discovered via `crm_whoami`)
- [ ] No hardcoded file paths except `~/customer-engagements/` and `~/.copilot/skills/msx-crm/crm-tools/` (could be made configurable)
- [ ] Israeli work week (Sun–Thu) is configurable via `preferences.schedule_days`
- [ ] Initials are confirmed with user, not assumed

### Team Onboarding Script

For rapid team rollout, a bootstrap script could:
1. Verify all prerequisites are installed.
2. Run `/crm-activity-sync setup` in interactive mode.
3. Optionally scaffold customer-engagements from a shared team list.

---

## Refresh and Maintenance

### Config Refresh Triggers

| Trigger | Action |
|---|---|
| Manual: `/crm-activity-sync setup` | Full re-discovery |
| Manual: `/crm-activity-sync remap` | Re-map milestones for specific customer |
| Auto: `last_refreshed` >14 days | Warn during sync; suggest refresh |
| Auto: Milestone query returns "closed" status | Remove from active mapping; alert user |
| Auto: New opportunity detected via watch | Prompt to add to mapping |

### Sync Log Retention

`sync-log.json` entries older than 90 days are archived to `sync-log-archive.json`
to keep the working file small. The archive is append-only.

---

## Example: Full Daily Pipeline Flow

```
07:30 IST — /daily-activity-log automation triggers

1. Scan work repos for Apr 22:
   - ~/SASE: 21 commits (design: 18, docs: 3) → CheckPoint/SASE, type: Design
   - No other repos have commits

2. Scan calendar for Apr 22:
   - 10:00-11:00 "SASE Architecture Deep-Dive" (checkpoint.com attendees) → CheckPoint/SASE
   - 14:00-15:30 "AI Search Agent Infrastructure" (clal-ins.co.il attendees) → Clal/AI-Search
   - 16:00-16:30 "Sapiens Digital AI Overview" (subject keyword match) → Sapiens/Digital-AI

3. Scan sent emails for Apr 22:
   - Email to josephyostos@microsoft.com (AKS PG): "multi-NIC node pool" → CheckPoint/SASE

4. Aggregate per customer/project:
   - CheckPoint/SASE → Design (21 commits + 1 meeting + 1 PG email) → write activity-log.md
   - Clal/AI-Search → Meeting Call (1 meeting) → write activity-log.md
   - Sapiens/Digital-AI → Meeting Call (1 meeting) → write activity-log.md

5. Commit to git in each customer-engagements repo.

---

08:00 IST — /crm-activity-sync automation triggers

1. Step 0: VPN ✅, CRM auth ✅, Config ✅, activity-log.md files ✅

2. Retry pending:
   - Sapiens/digital-ai (no_milestone from Apr 21) → query milestones → still none → stays pending

3. Read activity-log.md for Apr 22:
   - CheckPoint/SASE → Type: Design, Sources: repo (21), meeting (1), email (1)
   - Clal/AI-Search → Type: Meeting Call, Sources: meeting (1)
   - Sapiens/Digital-AI → Type: Meeting Call, Sources: meeting (1)

4. Map to milestones:
   - CheckPoint/SASE → SASE POC milestone ✅
   - Clal/AI-Search → [milestone lookup] ✅
   - Sapiens/Digital-AI → no milestone 🔴 → queue

5. Idempotency check:
   - "RBH - Design" on SASE POC → does not exist → create
   - "RBH - Meeting Call" on Clal milestone → does not exist → create

6. Create CRM tasks:
   ✅ RBH - Design → SASE POC (description: "SASE architecture design — PoP topology,
      traffic flows, HA/failover. Meeting with CheckPoint. Coordinated with AKS PG
      on multi-NIC. 21 commits.")
   ✅ RBH - Meeting Call → Clal AI Search ADS
   🔴 Sapiens → pending (no_milestone)

7. Opportunity watch:
   - Kobi Shitrit opps: Checkpoint-SASE (known), Checkpoint-CloudGuard (NEW!)
   - 🔔 Alert: New opp "Checkpoint - CloudGuard" — you're not on deal team

8. Send Teams receipt:
   "📋 CRM Sync Apr 22: 2 created, 1 pending, 1 new opp detected"
```

---

## New User Adoption Guide

When this skill is installed by a new Clawpilot user, run through the following
onboarding steps before the first sync. This section is for the AI  executeagent 
these steps automatically on first invocation.

### Prerequisites Check

1. **VPN  User must have Azure VPN configured for CRM access.access** 
   - Check: `~/Scripts/ensure-vpn.sh` exists, or guide user to set up MSFT VPN.
   - If missing: "CRM access requires Microsoft VPN. Please configure Azure VPN
     Client and re-run setup."

2. **CRM  `~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs` must exist.tool** 
   - If missing: Clone the repo:
     ```bash
     git clone https://github.com/roie9876/crm-tools.git ~/.copilot/skills/msx-crm/crm-tools
     cd ~/.copilot/skills/msx-crm/crm-tools
     ```
   - Test (POSIX): `node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_whoami`
   - Test (Windows PowerShell): `node $HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs crm_whoami`
 auth/VPN issue.

3. **Node. Required for CRM tools.js** 
   - Check: `which node` (POSIX) or `Get-Command node` (PowerShell)
   - If missing: macOS → `brew install node` · Windows → `winget install OpenJS.NodeJS` · Linux → use the distro package manager

4. **M365 signed  Needed for calendar, email, and Teams data.in** 
   - Check: `m_m365_status`
   - If not signed in: `m_m365_sign_in`

### First-Run Setup Flow

On first invocation of `/crm-activity-sync` (no `config.json` exists):

1. **Discover user identity:**
 name, email, job title, department
 CRM user ID
 manager name and email
 "RBH")
   - Confirm with user: "Your initials for CRM subjects will be {XYZ}. OK?"

2. **Discover customers:**
   - Ask: "Which customers do you cover? List them or I'll scan your recent
     calendar for external attendee domains."
   - For each customer:
     - Create `~/customer-engagements/{slug}/` folder structure
     - Search CRM for matching opportunities
     - Get milestones for each opportunity
     - Build `crm-mapping.json`

3. **Discover SSPs:**
   - Ask: "Who are your SSPs (Solution Sales Professionals)?"
   - Or discover from deal team membership on known opportunities
   - Resolve Teams chat IDs: `m365_create_chat_by_email(email)`
   - Cache in `crm-mapping.json` under `ssp_chat_ids`

4. **Register work repos:**
   - Ask: "Do you have local git repos for any customer projects?"
   - For each: validate `.git/` exists, register in `crm-mapping.json`

5. **Set up automations:**
   - Ask: "Want daily automated activity logging + CRM sync? (Recommended)"
   - If yes: create the two daily automations (07:30 activity log + 08:00 CRM sync)
   - Adjust schedule for user's work week (Israel: Sun-Thu, others may differ)

6. **Test end-to-end:**
   - Run `/daily-activity-log today` for one customer
   - Show the generated activity-log.md
   - Create one test CRM task on a known milestone
   - Verify in MSX UI
   - Delete the test task
   - "Setup complete! Your daily pipeline is ready."

### What Gets Personalized (Not Hardcoded in Skill)

| Item | Where stored | Discovered how |
|---|---|---|
| User name, email, CRM ID | `config.json` | M365 profile + CRM whoami |
| Manager | `config.json` | M365 Graph |
| Initials (for CRM subjects) | `config.json` | Derived from name, confirmed by user |
| Customers | `customer-engagements/` folders | User input + calendar scan |
| Opportunities + milestones | `crm-mapping.json` per customer | CRM queries |
| SSPs | `config.json` + `crm-mapping.json` | User input + deal team queries |
| SSP chat IDs | `crm-mapping.json` | `m365_create_chat_by_email` |
| Work repos | `crm-mapping.json` | User input, validated |
| Work schedule (Sun-Thu vs Mon-Fri) | `config.json` | User input |
| VPN script path | `config.json` | Discovered or created during setup |
| CRM tool path | `config.json` | Default `~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs` |
