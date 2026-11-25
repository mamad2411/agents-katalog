---
name: daily-activity-log
description: "Scan work repos (git), calendar events, PG/engineering emails, and Teams chats (SSP + customer) to build a structured daily activity log in customer-engagements. Writes activity-log.md per project as the source of truth for CRM sync and engagement tracking. Triggers include: 'daily activity', 'activity log', 'log my work', 'what did I do', 'sync activity', 'daily sync', 'update activity log', or any request to capture the day's SE work into customer-engagements."
---

# /daily-activity-log — Daily Activity Log Builder

Scan multiple data sources — work repos (git history), M365 calendar,
PG/engineering emails, and Teams chats (both SSP and direct customer) — to build
a structured daily activity summary per customer project. Writes `activity-log.md` in each project's
customer-engagements folder, making customer-engagements the single source of
truth for downstream consumers like `/crm-activity-sync`.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the matching shell syntax. See `_shared/PLATFORM.md` (skills repo root) for the full translation table. Quick reference:

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| List dir | `ls $HOME/customer-engagements/` | `Get-ChildItem $HOME/customer-engagements/` |
| Find node | `which node` | `Get-Command node` |
| Run git in repo | `cd $HOME/repo && git log ...` | `Set-Location $HOME/repo; git log ...` |
| Home dir | `~` or `$HOME` | `$HOME` |

Default to POSIX commands; use PowerShell on Windows native (not WSL/Git Bash).

## Core Principles

- **Evidence-based only.** Every logged activity must trace to a concrete artifact: a git commit, a calendar event, or a sent email. Never infer or fabricate work.
- **Aggregate per day.** All evidence for a single customer + project + date is merged into one daily entry. A day of design commits + a meeting + an engineering email → one entry with sections, not three separate entries.
- **Append, never overwrite.** New daily entries are prepended (most recent first) to `activity-log.md`. Existing entries are never modified or removed.
- **Idempotent.** If the log already contains an entry for the target date + project, skip it. Report: "Activity for {customer}/{project} on {date} already logged."
- **Preserve source language.** Commit messages, email subjects, and meeting titles stay in their original language.
- **Graceful degradation.** Each data source can fail independently. If git is available but calendar isn't, log what you have. Note missing sources.
- **Classify, don't just list.** Each daily entry gets a **Task Category** classification based on the evidence. The category must match one of the 20 CRM `msp_taskcategory` values. The skill auto-classifies using signal keywords, but the user can override to any category during interactive mode or via the `default_activity_type` in `crm-mapping.json`.
- **Relevance-only content.** Every piece of text-based evidence (Teams messages, email body, meeting notes) must pass a **semantic relevance check** before being logged. You (the LLM executing this skill) read each message and judge whether it is project-related or off-topic. This is NOT a keyword filter — it is your semantic understanding of context. Personal chat, jokes, politics, social conversation, weekend plans, food, sports, and any off-topic messages are silently excluded — even if they appear in a customer or SSP chat. Only project-related business and technical content is logged. See "Relevance Classification" section below.

### CRM Task Categories (all 20)

These are the valid `msp_taskcategory` values in MSX. The skill can assign any of them:

| Category | Value | Auto-classify signals |
|---|---|---|
| **Architecture Design Session** | `861980004` | "architecture", "design", "topology", "solution review", design commits |
| **PoC/Pilot** | `861980005` | "poc", "pilot", "testing", "lab", "hands-on", poc commits |
| **Workshop** | `861980001` | "workshop", "deep-dive", "training", "enablement", multi-hour events |
| **Customer Engagement** | `861980000` | General customer meetings, sync calls, status updates |
| **Briefing** | `861980008` | "briefing", "ideation", "brainstorm", "explore", "concept" |
| **Blocker Escalation** | `861980006` | Engineering escalation emails, PG coordination on blockers |
| **Demo** | `861980002` | "demo", "demonstration", "showcase", "show and tell" |
| **Internal** | `861980012` | Internal-only meetings with project keyword match, no customer |
| **ACE** | `606820000` | "ace", "azure consumption" |
| **Call Back Requested** | `861980010` | "callback", "call back" |
| **Consumption Plan** | `861980007` | "consumption", "commit", "macc" |
| **Cross Segment** | `606820001` | "cross segment", "cross-segment" |
| **Cross Workload** | `606820002` | "cross workload", "cross-workload" |
| **External (Co-creation of Value)** | `861980013` | "co-creation", "hackathon", "joint development" |
| **Negotiate Pricing** | `861980003` | "pricing", "negotiate", "commercial", "deal terms" |
| **New Partner Request** | `861980011` | "partner", "isv", "si request" |
| **Post Sales** | `606820003` | "post sales", "post-sales", "go-live support" |
| **RFP/RFI** | `861980009` | "rfp", "rfi", "request for proposal" |
| **Tech Support** | `606820004` | "support", "incident", "troubleshoot" |
| **Technical Close/Win Plan** | `606820005` | "close plan", "win plan", "technical close" |

The top 8 are the most common for SE daily work. The remaining 12 are available for
specialized activities. If the auto-classifier can't determine the category, it falls
back to the project's `default_activity_type` in `crm-mapping.json`.

- **Detect unknown customers.** When a calendar event has external attendees whose domain doesn't match any existing `crm-mapping.json` customer, flag it. In interactive mode: ask whether it's a core customer, temp engagement, or not customer work. In automated mode: log the activity anyway (customer-engagements folder is source of truth if it exists) and send a Teams alert asking for classification.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Required Sibling Skills

This skill requires sibling skills from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|---|---|---|
| `/crm-activity-sync` | Downstream — reads `activity-log.md` and pushes to CRM. Also owns the shared `config.json` and setup flow | ✅ For config + CRM sync |
| `/customer-repo` | Scaffolds `customer-engagements/` folder structure per customer | ✅ For initial setup |
| `/msx-crm` | CRM query tools (`run-tool.mjs`) for milestone and opportunity lookups | ⚠️ Only if CRM sync is desired |

Check if each required skill is installed:

```bash
# macOS / Linux
for skill in crm-activity-sync customer-repo msx-crm; do
  [ -f "$HOME/.copilot/skills/$skill/SKILL.md" ] && echo "✅ $skill" || echo "❌ $skill MISSING"
done
```

```powershell
# Windows
foreach ($skill in @('crm-activity-sync','customer-repo','msx-crm')) {
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
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |
| Node.js | `node --version` | `Get-Command node` | `brew install node` | `winget install OpenJS.NodeJS` |

Node.js is only strictly required if CRM sync is desired. Install any missing tools before proceeding.

### CRM Tool Script (`run-tool.mjs`) — Optional

If CRM sync is desired, the helper script must exist at `$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs`.

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" ] && echo "✅ CRM tools found" || echo "⚠️ CRM tools not found (CRM sync will be unavailable)"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\msx-crm\crm-tools\run-tool.mjs") { "✅ CRM tools found" } else { "⚠️ CRM tools not found" }
```

If missing and CRM sync is desired, clone the SE Kanban Tracker repo:

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

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

### Additional Checks

| Prerequisite | Required? | How to check |
|---|---|---|
| `customer-engagements/` folder | ✅ | `$HOME/customer-engagements/` exists with ≥1 customer |
| Config file | ✅ | `$HOME/.copilot/crm-activity-sync/config.json` — shared with crm-activity-sync |

**Note:** This skill shares its config with `/crm-activity-sync`. If setup hasn't
been run yet, it will trigger the setup flow (see crm-activity-sync Step 1).

## Commands

| Command | Purpose |
|---|---|
| `/daily-activity-log` | Log yesterday's activities (default) |
| `/daily-activity-log today` | Log today's activities (so far) |
| `/daily-activity-log <date>` | Log activities for a specific date (ISO: 2026-04-21) |
| `/daily-activity-log week` | Log the current work week (Sun–Thu) |
| `/daily-activity-log range <start> <end>` | Log a date range |
| `/daily-activity-log add-repo <customer>/<project> <path>` | Register a work repo for a project |
| `/daily-activity-log remove-repo <customer>/<project> <path>` | Unregister a work repo |
| `/daily-activity-log repos` | List all registered work repo mappings |
| `/daily-activity-log add-domain <customer> <domain>` | Register an email domain for a customer (e.g., `checkpoint checkpoint.com`) |
| `/daily-activity-log domains` | List all customer domain mappings |
| `/daily-activity-log discover-chats` | Scan recent Teams chats to auto-discover customer conversations |
| `/daily-activity-log customer-chats` | List all cached customer chat IDs |

## File Locations

| File | Purpose |
|---|---|
| `~/.copilot/crm-activity-sync/config.json` | Shared config (user profile, preferences, repo mappings) |
| `~/customer-engagements/{customer}/projects/{project}/activity-log.md` | Per-project daily activity log (output) |
| `~/customer-engagements/{customer}/crm-mapping.json` | Per-customer project-to-CRM mapping (shared with crm-activity-sync) |

## Config: Work Repo Registration

Work repos are stored in `crm-mapping.json` under each project:

```json
{
  "projects": {
    "sase": {
      "display_name": "SASE",
      "work_repos": [
        {
          "path": "/Users/robenhai/SASE",
          "label": "SASE Design & POC",
          "added": "2026-04-23"
        }
      ],
      "subject_keywords": ["sase", "checkpoint", "aks", "dpdk", "srv6"]
    }
  }
}
```

**Registration rules:**
- A repo is registered to exactly one project. If a repo serves multiple projects (rare), ask the user which project it belongs to.
- Repos are registered manually via `/daily-activity-log add-repo` or during setup.
- Not every project has a repo — some are meeting-only engagements.
- The path must be an absolute path to a directory containing `.git/`.
- Validate on registration: `[ -d "<path>/.git" ]`. If not a git repo → reject.

## Config: SSP Chat Mapping

SSP-to-customer mapping comes from `config.core_ssps[]` in
`~/.copilot/crm-activity-sync/config.json`. Each SSP entry lists which customers
they cover. The 1:1 chat ID is resolved at runtime via
`m365_create_chat_by_email(email)` and can optionally be cached in
`crm-mapping.json` for performance:

```json
{
  "ssp_chat_ids": {
    "kobishitrit@microsoft.com": "19:80cb6140-...@unq.gbl.spaces"
  },
  "projects": {
    "sase": {
      "group_chat_ids": [
        {
          "id": "19:5fda07cb...@thread.v2",
          "topic": "HSASE-AZURE-GlobalNetworkBrain",
          "added": "2026-04-23"
        }
      ]
    }
  }
}
```

**SSP chat scanning rules:**
- Only scan chats for SSPs in `config.core_ssps`. Never scan random chats.
- Cache resolved chat IDs in `crm-mapping.json` under `ssp_chat_ids` to avoid
  repeated lookups.
- Group chats are optional — register via `/daily-activity-log add-group-chat`.
- The `group_chat_ids` array is per-project in `crm-mapping.json`.

**New commands for SSP chat management:**

| Command | Purpose |
|---|---|
| `/daily-activity-log add-group-chat <customer>/<project> <chat-id> <topic>` | Register a group chat for scanning |
| `/daily-activity-log remove-group-chat <customer>/<project> <chat-id>` | Unregister a group chat |

## Config: Customer Domains & Chat Discovery

Customer email domains are stored in `crm-mapping.json` per customer under a
top-level `domains` array. This is the primary mechanism for matching Teams chats
to customers:

```json
{
  "domains": ["checkpoint.com"],
  "customer_chat_ids": [
    {
      "id": "19:abc123...@unq.gbl.spaces",
      "type": "oneOnOne",
      "topic": "John Smith (CheckPoint)",
      "members": ["john.smith@checkpoint.com"],
      "discovered": "2026-04-24"
    },
    {
      "id": "19:def456...@thread.v2",
      "type": "group",
      "topic": "SASE Architecture Review",
      "members": ["john.smith@checkpoint.com", "kobishitrit@microsoft.com"],
      "discovered": "2026-04-24"
    }
  ],
  "projects": { ... }
}
```

**Domain registration rules:**
- Each customer can have one or more domains (e.g., `["checkpoint.com", "checkpoint.co.il"]`).
- Domains are matched against the email part after `@` in Teams chat member addresses.
- Register via `/daily-activity-log add-domain <customer> <domain>` or auto-discover.
- If `domains` is empty or missing, the customer is skipped during chat discovery.

**Customer chat discovery flow** (`/daily-activity-log discover-chats`):

1. Collect all known `customer_domains → customer` mappings from all `crm-mapping.json` files.
2. Call `m365_list_chats(limit: 50, expand: "members")` to get recent chats with member info.
   **Important:** Use `m365_list_chats` with `expand: "members"`, NOT `m365_search_chats`.
   Search only matches topic names and will miss unnamed chats or chats where the
   topic doesn't contain the customer name. Member-based scanning catches everything.
3. For each chat, check if any member's email domain matches a known customer domain.
   This catches: 1:1 chats with customer contacts, named group chats, AND unnamed
   group chats — as long as the customer member's email domain is registered.
4. If match → cache the chat entry in that customer's `crm-mapping.json` under `customer_chat_ids[]`.
   For unnamed chats, generate a descriptive topic like "(unnamed) member1, member2".
5. Skip chats that are already cached (match by `id`).
6. Report: "Discovered N new customer chats: {customer} — {topic/member}."

**Pagination:** If the user has many chats, page through using `skipToken` from the
response. Scan at least 100 chats (2 pages of 50) to ensure good coverage.

**Auto-discovery during daily runs:**
- Run discovery at the start of EVERY daily run (not just when `customer_chat_ids`
  is empty). New customer chats may appear at any time.
- Discovery only runs once per skill invocation (not per date in range mode).
- Cache results immediately so subsequent dates in the same run benefit.
- Scan at least 50 recent chats per run. This is fast (single API call).

**Manual fallback:**
- If auto-discovery misses a chat (e.g., member uses a personal email, domain is
  unusual), the user can manually note the chat ID and register it. But unlike SSP
  chats and group chats, there is no separate manual-add command — just edit
  `crm-mapping.json` directly or let discovery handle it.

---

## Step 0: Determine Target Date(s)

**Default:** Yesterday, adjusted for Israeli work week.
- If today is Sunday → yesterday was Saturday (weekend) → use Thursday.
- Otherwise → use yesterday (including Friday and Saturday — work can happen
  on non-standard days; the skill logs whatever evidence it finds).

**Note:** The old logic skipped Friday and Saturday entirely. This was wrong —
SEs sometimes work on non-standard days (CritSits, deadlines, travel). The
skill should always check yesterday. If no evidence is found, it reports
"No activity detected" which is harmless. Missing real work is not.

**Explicit date:** The user can provide a specific date or range.

**Week mode:** Sunday through Thursday of the current week up to yesterday.

Set `target_dates[]` — an array of dates to process. Process each date
independently, in chronological order.

---

## Step 1: Load Config and Mappings

1. Read `~/.copilot/crm-activity-sync/config.json`.
   - If missing → prompt: "Run /crm-activity-sync setup first to configure your profile and customer mappings."
   - Stop.

2. For each customer in `~/customer-engagements/`:
   - Read `~/customer-engagements/{customer}/crm-mapping.json`.
   - If missing → this customer has no CRM mapping yet. Still process it (activity log is useful even without CRM), but warn: "No CRM mapping for {customer}. Activities will be logged but won't sync to CRM."

3. Build a lookup table:
   - `repo_path → { customer, project }` — maps each registered repo to its project.
   - `keyword → { customer, project }` — maps subject keywords to projects.
   - `customer_domains → { customer }` — maps email domains to customers (from `crm-mapping.json` `domains[]` field, falling back to `stakeholders.md`).
   - `ssp_email → { customer[], chat_id }` — maps SSPs to their customers and cached chat IDs.
   - `customer_chat_ids → { customer, chat_id, members[] }` — maps cached customer Teams chats to their customer (from `crm-mapping.json` `customer_chat_ids[]`).
   - `all_customer_names → [...]` — list of all known customer display names, slugs, and account names for content-based matching.
   - `all_project_keywords → { keyword: { customer, project } }` — flattened keyword map across all customers/projects for content-based matching.

---

## Step 2: Collect Evidence

For each target date, collect from all sources in parallel.

**Source types:**
- **2a.** Work Repo Git History (registered repos)
- **2b.** Calendar Events (M365)
- **2c.** Sent Emails (PG/Engineering + Customer)
- **2d.** SSP Teams Chat (registered SSP chats)
- **2e.** Customer Teams Chat (registered customer chats)
- **2f.** Relevance Classification (filter for all text sources)
- **2g.** Content-Based Chat Discovery (unmapped chats — LLM-driven) ⚠️ **MANDATORY — see gate below**

> **⚠️ Step 2g is NON-OPTIONAL.** Steps 2a–2e only scan pre-registered sources.
> Step 2g is the only mechanism that discovers NEW customer chats (ad-hoc meetings,
> EXT support cases, CritSit chats, 1:1s about customer work). Skipping it causes
> silent data loss — entire customer interactions will be missing from the daily log.
> A mandatory gate before Step 3 enforces this.

### 2a. Work Repo Git History

For each registered work repo:

```bash
cd <repo-path> && git --no-pager log \
  --format="%h %aI %s" \
  --since="<target-date>T00:00:00" \
  --until="<target-date+1>T00:00:00" \
  --author="$(git config user.email)" \
  2>/dev/null
```

**Important:** The `%aI` format gives ISO 8601 author date — needed for duration
calculation (time span from first to last commit).

**Important:** Filter by `--author` to only count the user's own commits, not
collaborators. Use `git config user.email` from the repo, or fall back to the
email in config.

**Extract from commits:**
- Total commit count.
- Commit message prefixes (everything before the first colon: `design:`, `poc:`, `feat:`, `fix:`, `docs:`, `test:`).
- Dominant prefix = most frequent → drives activity type classification.
- Summarize what changed: group by prefix, list the distinct topics.

**Prefix-to-task-category mapping:**

| Git prefix | CRM Task Category |
|---|---|
| `design`, `arch`, `proposal` | Architecture Design Session |
| `poc`, `feat`, `experiment`, `spike`, `test` | PoC/Pilot |
| `workshop`, `lab`, `enable` | Workshop |
| `demo`, `showcase` | Demo |
| `docs`, `readme`, `changelog` | Architecture Design Session (documentation supports design) |
| `fix`, `hotfix`, `patch` | PoC/Pilot (bug fixing during POC) |
| `escalation`, `blocker` | Blocker Escalation |
| `support`, `incident` | Tech Support |
| No prefix / unknown | Use project's `default_activity_type` from crm-mapping.json |

**If a repo has zero commits on the target date** → skip it, no entry for this source.

### 2b. Calendar Events

```
m365_list_events(startDate: "<target-date>T00:00:00Z", endDate: "<target-date>T23:59:59Z", limit: 50)
```

**Filter criteria:**
- ❌ Exclude all-day events.
- ❌ Exclude cancelled events.
- ❌ Exclude recurring 1:1s with manager (match `config.user.manager.email`).
- ❌ Exclude events with zero external attendees AND no project keyword match in subject.
- ✅ Include events where ≥1 attendee has an external (customer) email domain.
- ✅ Include events where the subject matches a project keyword, even if all-internal.

**For each qualifying event, extract:**
- Subject, start time, end time, duration.
- Attendee list (names, classify as internal/external/engineering).
- Whether external attendees are customer or Microsoft Engineering (PG).

**Map to customer/project:**
1. Match external attendee domains against `customer_domains` lookup.
2. Match subject against `keyword` lookup.
3. If both match the same project → confirmed.
4. If domain matches one customer but subject matches another → flag ambiguity, ask user.
5. If no match → skip (not a customer event).

**Classify meeting category:**
- Meeting + "workshop" / "deep-dive" / "hands-on" / "training" → **Workshop**
- Meeting + "architecture" / "design" / "topology" / "solution review" → **Architecture Design Session**
- Meeting + "poc" / "pilot" / "testing" / "lab" → **PoC/Pilot**
- Meeting + "demo" / "showcase" / "demonstration" → **Demo**
- Meeting + "ideation" / "brainstorm" / "explore" / "concept" → **Briefing**
- Meeting + "rfp" / "rfi" / "request for proposal" → **RFP/RFI**
- Meeting + "pricing" / "negotiate" / "commercial" / "deal" → **Negotiate Pricing**
- Meeting + "close plan" / "win plan" / "technical close" → **Technical Close/Win Plan**
- Meeting + "partner" / "isv" / "si" → **New Partner Request**
- Meeting + "consumption" / "commit" / "macc" → **Consumption Plan**
- Meeting + "support" / "incident" / "troubleshoot" → **Tech Support**
- Meeting + "post sales" / "go-live" → **Post Sales**
- Meeting with Microsoft PG/Engineering (no customer) + blocker context → **Blocker Escalation**
- Meeting with Microsoft PG/Engineering (no customer) + project keyword → **Architecture Design Session** or **PoC/Pilot** (internal engineering work)
- Internal-only meeting matching project keyword → **Internal**
- Customer meeting (generic, no keyword match) → **Customer Engagement**

### 2c. Sent Emails (PG/Engineering + Customer Architecture)

```
m365_list_emails(folder: "sent", startDate: "<target-date>", endDate: "<target-date+1>", limit: 50)
```

**Include only emails matching these criteria:**

1. **Product Group / Engineering emails:**
   - Recipient domain is `@microsoft.com` AND
   - Recipient is NOT in your direct team (config.user known team members) AND
   - Subject matches a project keyword from any `crm-mapping.json`

2. **Customer technical emails:**
   - Recipient domain matches a known customer domain AND
   - This is a project-related thread (subject matches keyword)

**Exclude everything else.** No internal team emails, no SSP coordination, no HR/admin.

**For each qualifying email, extract:**
- Subject, recipients (names + emails), date.
- Classify: "Engineering Coordination" or "Customer Communication".
- Map to customer/project via subject keywords and recipient domains.

**If zero qualifying emails on the target date** → skip, no entry for this source.

### 2d. SSP Teams Chat (Ad-hoc Calls & Technical Discussion)

Ad-hoc Teams calls between SE and SSP are a major activity source that doesn't appear
on the calendar. These are captured by scanning 1:1 and relevant group chats with
known SSPs.

**For each SSP in `config.core_ssps`:**

1. **Find chat ID.** Use `m365_create_chat_by_email(email: "<ssp-email>")` to get the
   1:1 chat ID. Cache this — the chat ID is stable.

2. **Pull messages for target date:**
   ```
   m365_list_chat_messages(chatId: "<chat-id>", limit: 50)
   ```
   Filter to messages where `createdDateTime` falls within the target date (in user's
   timezone). Paginate with `skipToken` if needed to cover the full day.

3. **Detect ad-hoc calls.** Messages with `content: "<systemEventMessage/>"` and
   `type: "unknownFutureValue"` are Teams call events (call started/ended). Count
   pairs of consecutive systemEventMessages as one call. Each pair typically has
   timestamps ~seconds apart (start + end).

4. **Extract technical context.** From the non-system text messages on the same date,
   apply the **Relevance Classification** (see Step 2f). For each message:
   - First apply the quick scheduling filter: messages that are purely coordination
     like "זמין?", "פנוי?", "available?", "בפגישה", "שניה", "ok", "👍", single emoji,
     or messages shorter than 10 characters → classify as **Scheduling**, drop.
   - For all remaining messages, apply **semantic relevance check**: read the content
     and classify as **Relevant** (technical/business/project) or **Off-topic**
     (personal, jokes, politics, social). Only include **Relevant** messages.
   - Preserve original language (Hebrew, English, mixed).

5. **Map to customer/project:**
   - Use the SSP → customer mapping from `config.core_ssps[].customers[]`.
   - If the SSP covers multiple customers (rare), match by scanning message content
     against each project's `subject_keywords`.
   - If ambiguous → assign to the SSP's primary customer. Flag in the log.

6. **Summarize topics.** Group the technical messages into topics:
   - Extract the key nouns/concepts discussed (e.g., "SRv6", "NAT GW", "SSD",
     "ephemeral storage", "LB usage").
   - Note if any messages reference forwarded emails, documents, or PG contacts.
   - Count: number of ad-hoc calls, number of substantive messages.

**Also scan relevant group chats** registered in `crm-mapping.json`:
- If a project has a `group_chat_ids[]` array, scan those too.
- Apply the same date filter and technical content extraction.
- Group chats with SSP + PG engineers are especially valuable (e.g., HSASE-AZURE-*).

**If zero calls AND zero technical messages on the target date** → skip, no entry
for this source.

**Important filtering rules:**
- Only scan chats with SSPs mapped to active customers. Don't scan random chats.
- Messages from the SSP AND from the SE (you) both count as evidence.
- A day with calls but no text messages → still log as "ad-hoc call(s)" with
  no topic detail. The call itself is evidence of customer engagement.
- A day with technical text messages but no calls → still log. SSP text coordination
  is also customer work (e.g., answering SSP questions about the design async).

### 2e. Customer Teams Chat (Direct Customer Communication)

Direct Teams conversations with customer contacts — 1:1 chats and group chats
that include external customer members. Unlike SSP chats (2d) which are between
internal Microsoft people, these are conversations directly with the customer.

**For each customer that has `customer_chat_ids[]` in `crm-mapping.json`:**

1. **Iterate cached chats.** For each entry in `customer_chat_ids[]`:

2. **Pull messages for target date:**
   ```
   m365_list_chat_messages(chatId: "<chat-id>", limit: 50)
   ```
   Filter to messages where `createdDateTime` falls within the target date (in user's
   timezone). Paginate with `skipToken` if needed to cover the full day.

3. **Detect calls.** Same logic as SSP chats: messages with
   `content: "<systemEventMessage/>"` and `type: "unknownFutureValue"` are Teams
   call events. Count pairs as one call.

4. **Extract content.** From the non-system text messages on the same date,
   apply the **Relevance Classification** (see Step 2f). Same process as SSP chats:
   - Quick scheduling filter first (short/emoji/coordination → drop).
   - Then **semantic relevance check** on remaining messages: read each one and
     classify as **Relevant** (project work) or **Off-topic** (personal/social).
   - Only include **Relevant** messages in the log.
   - Preserve original language.

5. **Map to project:**
   - Check if the chat's `members[]` domains match a specific project's
     `subject_keywords` from the message content.
   - If the customer has only one project → assign directly.
   - If multiple projects exist → scan message content against each project's
     `subject_keywords` to find the best match.
   - If ambiguous → in interactive mode, ask the user. In automated mode, assign
     to the customer's default project (first in `crm-mapping.json`).

6. **Summarize.** Group messages into topics:
   - Extract key discussion points.
   - Note document shares, links, images.
   - Count: calls, substantive messages, and which members participated.

**If a customer has `domains` but no `customer_chat_ids`:**
- Run auto-discovery (see Config section above) before scanning.
- Cache results and proceed with scanning.

**If zero calls AND zero substantive messages on the target date** → skip, no
entry for this source.

**Important filtering rules:**
- Scan chats cached in `customer_chat_ids[]` here. Unmapped chats are handled
  by Step 2g (content-based discovery) — do NOT skip them entirely.
- Both your messages and customer messages count as evidence.
- A day with only a Teams call to the customer (no text) → still log as
  "customer call" — the call itself is engagement evidence.
- A day with only text messages (no call) → still log. Async customer
  communication is also work.
- If the same customer chat already contributed to a calendar event match
  (e.g., a scheduled Teams meeting that shows up in both calendar and chat),
  the calendar event takes precedence for that time block. But additional
  text messages outside the meeting window still count as separate evidence.
- Group chats with mixed internal + customer members: classify as customer
  chat (not SSP chat), since the customer is directly participating.

---

### 2g. Content-Based Chat Discovery (Unmapped Chats)

**This is the most important discovery mechanism.** Steps 2d and 2e only scan
chats that are pre-registered in `crm-mapping.json`. But customer work often
happens in chats that were never registered: ad-hoc support cases (EXT tickets),
1:1 with colleagues helping on customer issues, meeting chats from one-off calls,
new group chats created mid-engagement.

**The LLM (you) can read message content and understand which customer it relates
to.** This step uses semantic analysis — not domain matching — to discover
customer-relevant chats that other steps missed.

#### Discovery Flow

1. **Get recently active chats.**
   ```
   m365_list_chats(limit: 50, expand: ["members", "lastMessagePreview"])
   ```
   Filter to chats that had activity on any of the `target_dates[]`. Use
   `lastUpdatedDateTime` as the initial filter (it's fast — no message reads yet).

2. **Exclude already-scanned chats.** Remove chats that were already processed
   by steps 2d (SSP chats) or 2e (registered customer chats). These are identified
   by chat ID matching against `ssp_chat_ids` and `customer_chat_ids` in all
   `crm-mapping.json` files. Also exclude 1:1 chats with the user's manager
   (`config.user.manager.email`) — these are not customer work.

3. **Quick triage each remaining chat.** For each unscanned chat with target-date
   activity, read up to 20 messages from the target date:
   ```
   m365_list_chat_messages(chatId: "<id>", limit: 20)
   ```
   Filter messages to the target date (by `createdDateTime` in user's timezone).
   If zero messages on the target date → skip.

4. **LLM semantic classification.** For each chat with messages on the target
   date, you (the LLM) read the messages and answer these questions:

   a. **Is this customer-related work?** Look for:
      - Customer names, project names, product names matching known customers
      - Azure resource references (resource groups, subscriptions, VNets, PE)
        that match customer environments
      - Technical discussion tied to a known engagement (architecture, debugging,
        deployment, CritSit)
      - Support case context (EXT tickets, ICM incidents, CritSit)
      - Colleague names known to work on specific customer accounts (from
        `crm-mapping.json` SSP lists, stakeholders)
      - Chat topic keywords ("כלל ביטוח", "checkpoint", "sase", etc.)

   b. **Which customer and project?** Match against:
      - `all_customer_names` — customer display names, slugs, account names
      - `all_project_keywords` — subject keywords from all projects
      - Member names cross-referenced with known stakeholders/SSPs
      - Azure resource naming patterns (e.g., `rg-ai-clal-dev` → Clal Insurance)

   c. **What type of activity?** Classify using the same CRM Task Category
      signals as Step 3b.

   If the answer to (a) is NO → skip. Not customer work.
   If the answer to (a) is YES but (b) is ambiguous → in interactive mode, ask
   the user. In automated mode, log to the best-guess customer and flag
   "auto-classified — verify customer mapping."

5. **Process matched chats.** For each chat classified as customer-related:
   - Apply the same evidence extraction as Step 2e (calls, messages, topics,
     relevance classification from Step 2f)
   - Add the evidence to the appropriate `{ customer, project }` evidence bucket
   - **Auto-cache** the chat in that customer's `crm-mapping.json` under
     `customer_chat_ids[]` with `"source": "content-based"` so future runs
     find it via Step 2e directly (faster, no re-classification needed)

#### What This Catches That Domain-Based Discovery Misses

| Scenario | Why domain-based fails | Content-based catches it |
|---|---|---|
| EXT support case (e.g., "EXT \| 2604230050000351") | Members are MSFT + support vendor (LTI Mindtree, Teknowledge). No customer domain. | Messages reference customer name, Azure resources, and project context |
| 1:1 with internal colleague helping on customer issue | Both members are @microsoft.com | Messages contain customer resource groups, deployment errors, and project-specific terms |
| Meeting chat from ad-hoc customer call | Meeting wasn't in registered chats. Members may all be internal if customer joined via phone | Chat topic or messages reference customer by name |
| CritSit / ICM chat | Created by support, members are all internal + support vendor | ICM details, customer subscription IDs, resource names in messages |
| Cross-team collaboration | Engineers from other teams helping. No customer member present | Discussion clearly about customer architecture, deployment, blockers |

#### Performance Considerations

- **This step runs AFTER steps 2a-2e.** It only scans chats not already covered.
- **Quick exit:** Most chats are internal (team standup, org-wide, social). The
  LLM can classify these in seconds by reading the topic + first few messages.
  Only customer-related chats get full message extraction.
- **Caching eliminates re-work.** Once a chat is auto-cached in `crm-mapping.json`,
  future runs process it via Step 2e without needing LLM classification again.
- **Limit:** Scan at most 50 unmapped chats per run. This is enough for daily
  discovery. For backfill runs, page through more chats if needed.
- **Parallel with other steps:** This step can run in parallel with Steps 2a-2e
  since it targets different chats.

#### Auto-Cache Format

When a chat is auto-discovered via content-based classification, cache it in
`crm-mapping.json` under `customer_chat_ids[]`:

```json
{
  "id": "19:34791f8863eb455c860321ab3a702e08@thread.v2",
  "type": "group",
  "topic": "EXT | 2604230050000351",
  "members": ["Ido Katz", "Scott Vickers", "Jayant Kumar"],
  "discovered": "2026-04-25",
  "source": "content-based",
  "matched_by": "Messages reference Clal Insurance Azure resources (rg-ai-clal-dev-swe) and AI Foundry PE debugging"
}
```

The `source: "content-based"` and `matched_by` fields distinguish auto-discovered
chats from domain-matched ones. This helps the user audit and correct
misclassifications if needed.

---

## Step 2f: Relevance Classification (applies to ALL text sources)

Before any text-based evidence (Teams messages, email bodies, meeting chat) is
included in the activity log, apply **semantic relevance classification**. This is
not a keyword filter — it is an LLM judgment call made by you (the agent executing
this skill) when you read each piece of content.

### Classification Rules

For each message, email, or text excerpt, classify as one of:

| Classification | Action | Examples |
|---|---|---|
| **Relevant** | Include in activity log | Architecture discussion, requirements, design decisions, technical questions, pricing, timelines, deliverables, PG coordination, blocker discussion, status updates, action items, document sharing (technical), meeting scheduling about project topics |
| **Off-topic** | Silently exclude | Jokes, politics, sports, weekend plans, food, personal life, social chit-chat, memes, emoji-only reactions, holiday wishes, birthday messages, general small talk |
| **Scheduling** | Exclude (already filtered) | "זמין?", "available?", "ok", "👍", "שניה", "בפגישה", single emoji, <10 chars |

### How to Classify

Read the message content and ask: **"Does this message contribute to understanding
what work was done on the project?"**

- If YES → **Relevant**. Include it.
- If NO → **Off-topic**. Drop it silently. Do not mention it in the log.
- If MIXED (e.g., starts with a joke then pivots to a technical question) →
  **Relevant**. Include the technical part, summarize without the off-topic portion.

### Where This Applies

| Source | What gets classified | Notes |
|---|---|---|
| **SSP Teams chat (2d)** | Each non-system message | Replaces the old "scheduling chatter" blocklist with full semantic check |
| **Customer Teams chat (2e)** | Each non-system message | Same semantic check |
| **Sent emails (2c)** | Email subject + body preview | Already filtered by keyword + domain; relevance check is a second pass |
| **Calendar events (2b)** | Meeting subject | Already filtered by attendees + keywords; generally all relevant |
| **Git commits (2a)** | N/A — commits in registered repos are always relevant | No filter needed |
| **Group chats** | Each non-system message | Same semantic check |

### Counting Rules After Classification

- **Only relevant messages count** toward the `substantive messages` total in the
  Sources line (e.g., "customer-chat (1 call, 5 messages)" — those 5 are post-filter).
- **Calls always count** regardless of message content — a Teams call to a customer
  is work evidence even if the surrounding text is social.
- **Duration estimation** uses only relevant message count (5 min per relevant
  exchange, not per raw message).

### Edge Cases

| Case | Behavior |
|---|---|
| All messages in a chat on target date are off-topic | No entry from this source. The chat had no project-relevant activity. |
| Chat has a call + only off-topic text messages | Log the call. Skip the messages. Entry says "1 call, no substantive messages." |
| Message is in Hebrew/mixed language | Classify based on meaning, regardless of language. Technical Hebrew = relevant. |
| Message references a shared document | Relevant — document sharing is work activity, even if the text is brief ("check this doc"). |
| Ambiguous message (could be social or work) | When in doubt, include it. Better to over-log slightly than miss real work. |

---

## ⛔ Pre-Synthesis Gate (MANDATORY before Step 3)

**DO NOT proceed to Step 3 until ALL evidence sources have been executed.**
This gate exists because Step 2g (content-based chat discovery) is the most
commonly skipped step — it's the heaviest and runs last — but it catches
customer interactions that NO other step can find.

Confirm each source was executed (not just "no results" — actually ran):

| # | Source | Executed? |
|---|--------|-----------|
| 2a | Git repos scanned | ☐ |
| 2b | Calendar events scanned | ☐ |
| 2c | Sent emails scanned | ☐ |
| 2d | SSP chats scanned | ☐ |
| 2e | Customer chats scanned | ☐ |
| 2f | Relevance classification applied | ☐ |
| **2g** | **Content-based chat discovery (unmapped chats)** | **☐** |

**If 2g was not executed → STOP and run it now before continuing.**

A "no results" from 2g is fine (it means no unmapped chats had customer content).
But "not executed" is a skill violation — it guarantees silent data loss.

---

## Step 3: Aggregate and Classify

For each `{ customer, project, target_date }` combination that has at least one
piece of evidence:

### 3a. Merge Evidence

Combine all evidence into a single daily entry:

```
evidence = {
  repo_commits: [...],       // from 2a
  calendar_events: [...],    // from 2b
  sent_emails: [...],        // from 2c
  ssp_chat: {                // from 2d
    calls: N,                // count of ad-hoc Teams calls
    topics: [...],           // extracted technical topics
    messages: [...],         // substantive messages (filtered)
    ssp_name: "...",         // SSP name
    chat_sources: [...]      // which chats contributed (1:1, group names)
  },
  customer_chat: {           // from 2e
    calls: N,                // count of direct customer Teams calls
    topics: [...],           // extracted discussion topics
    messages: [...],         // substantive messages (filtered)
    members: [...],          // customer member names who participated
    chat_sources: [...]      // which chats contributed (1:1, group w/ customer)
  }
}
```

### 3b. Determine Task Category

Match evidence against the **auto-classify signals** from the CRM Task Categories
table above. Use the **dominant signal** with this priority:

| Priority | Signal | Category |
|---|---|---|
| 1 | Workshop event (>2 hours, multiple attendees, "workshop" keyword) | Workshop |
| 2 | Customer meeting with "design"/"architecture" keyword | Architecture Design Session |
| 3 | Customer meeting with "poc"/"pilot" keyword | PoC/Pilot |
| 4 | Engineering escalation email (PG coordination on blocker) | Blocker Escalation |
| 5 | SSP chat with "design"/"architecture" topics + calls | Architecture Design Session |
| 5b | Customer chat with "design"/"architecture" topics + calls | Architecture Design Session |
| 6 | SSP chat with "poc"/"pilot"/"testing" topics + calls | PoC/Pilot |
| 6b | Customer chat with "poc"/"pilot"/"testing" topics + calls | PoC/Pilot |
| 7 | "demo"/"showcase" keyword in meeting or commits | Demo |
| 8 | "rfp"/"rfi" keyword | RFP/RFI |
| 9 | "pricing"/"negotiate"/"commercial" keyword | Negotiate Pricing |
| 10 | "partner"/"isv" keyword | New Partner Request |
| 11 | Repo commits dominant prefix → match prefix to category (see 2a table) | Varies |
| 12 | Internal-only meeting matching project keyword (no customer attendees) | Internal |
| 13 | SSP chat (calls or technical messages, no other keyword match) | Customer Engagement |
| 13b | Customer chat (calls or technical messages, no other keyword match) | Customer Engagement |
| 14 | Customer meeting (generic, no keyword match) | Customer Engagement |
| 15 | Engineering emails only (no meeting, no repo) | Architecture Design Session |
| 16 | Project's `default_activity_type` from crm-mapping.json | Fallback |

**If multiple categories are equally strong** (e.g., 10 design commits + a POC meeting),
use the project's `default_activity_type` as tiebreaker.

**The `**Type:**` line in activity-log.md must use the exact CRM label** (e.g.,
"Architecture Design Session", not "Design") so `/crm-activity-sync` can map it
directly to the `msp_taskcategory` value without ambiguity.

### 3c. Estimate Duration

Calculate the total duration in **minutes** for the day's activity. This is written
to `activity-log.md` and consumed by `/crm-activity-sync` to populate
`actualdurationminutes` on the CRM task.

**Duration estimation rules by source:**

| Source | How to estimate | Example |
|---|---|---|
| **Calendar meeting** | Exact: `end - start` from event | 60 min meeting → 60 min |
| **Ad-hoc Teams call** | From `systemEventMessage` timestamp pairs: `end_ts - start_ts`. If only one pair detected, minimum 10 min | Two calls, 8 min + 15 min → 23 min |
| **SSP text discussion** (no call) | Estimate 5 min per substantive message exchange (back-and-forth) | 4 messages exchanged → 20 min |
| **Customer chat call** | Same as ad-hoc Teams call: `systemEventMessage` timestamp pairs. Minimum 10 min per call | 1 customer call, 22 min → 22 min |
| **Customer chat text** (no call) | Estimate 5 min per substantive message exchange (same as SSP) | 6 messages exchanged → 30 min |
| **Git commits** | Time span from first to last commit of the day: `last_commit_time - first_commit_time`. Minimum 30 min if only 1 commit. If spread > 6 hours, cap at 6 hours (assumes breaks) | First commit 09:15, last 14:30 → 315 min (5h15m) |
| **Sent email** (PG/customer) | 15 min per qualifying email (composing a technical email) | 2 PG emails → 30 min |

**Aggregation rules:**
- **Don't double-count overlapping time.** If a meeting runs 10:00-11:00 and
  commits span 09:00-14:00, the meeting time is already within the commit span.
  Use the larger of: commit span vs sum of meetings.
- **Formula:** `total_duration = max(commit_time_span, sum_of_meetings) + ssp_call_duration + ssp_text_time + customer_call_duration + customer_text_time + email_time`
- **But:** if meetings and commits overlap, don't add meetings separately — they're
  part of the same work block. Only add meetings that fall **outside** the commit
  time span.
- **Minimum:** 15 min (even a single email counts as some work).
- **Maximum:** 480 min (8 hours) per day per project. If calculated duration exceeds
  this, cap at 480 and note "Duration capped at 8h" in the log.
- **Round** to nearest 15 min for CRM (e.g., 47 min → 45 min, 53 min → 60 min).

**Write to activity-log.md:**

The `**Duration:**` line goes after `**Sources:**`:

```
**Type:** Architecture Design Session
**Sources:** repo (3 commits), ssp-chat (4 calls, 8 messages), email (1 PG thread)
**Duration:** 285 min (4h 45m) — repo span 3h, 4 calls 45m, 1 email 15m
```

The breakdown after the total is informational — helps the user understand and
override if needed.

### 3d. Generate Summary

Write a concise 2–4 sentence summary combining all evidence:

**Template:**
```
{Activity-type-verb} for {project-display-name} — {main topics from repo commits and/or meetings}.
{If SSP calls: "{N} ad-hoc call(s) with SSP ({name}). Topics: {topic1}, {topic2}."}
{If customer chat: "{N} call(s) + {M} messages with {customer-contact}. Topics: {topic1}, {topic2}."}
{If engineering emails: "Coordinated with {PG-team} on {topic}."}
{If meetings: "{N} meeting(s) with {customer/internal/PG}."}
{Commit count if repo work: "{N} commits."}
```

**Example with SSP calls + customer chat:**
```
Design work for SASE — SRv6 feasibility analysis, NAT GW topology,
ephemeral storage assessment. 4 ad-hoc calls with SSP (Kobi Shitrit).
1 call + 3 messages with customer (John Smith). Coordinated with
Azure Networking PG (Brian Lehr) on SRv6 support. 1 email to PG. 3 commits.
```

---

## Step 4: Idempotency Check

Before writing, check if `activity-log.md` already has an entry for this date:

```bash
grep -c "^## <target-date>" ~/customer-engagements/{customer}/projects/{project}/activity-log.md
```

If found → skip this entry. Report: "Activity for {customer}/{project} on {date} already logged."

**Override:** If the user explicitly says "re-log" or "update", replace the existing
entry for that date (find the `## <date>` header, delete everything until the next
`## ` header or `---` separator, insert the new entry).

---

## Step 5: Write activity-log.md

### File Format

```markdown
# Activity Log — {Customer Display Name} / {Project Display Name}

## 2026-04-23

**Type:** PoC/Pilot
**Sources:** repo (3 commits), ssp-chat (4 calls, 8 messages), customer-chat (1 call, 3 messages), email (1 PG thread)
**Duration:** 315 min (5h 15m) — repo span 3h, 4 SSP calls 45m, 1 customer call 15m, 1 email 15m

### Repo Work
- 3 commits in ~/SASE: secrets management design (area 12), SKU families recommendation
- Prefix breakdown: design (2), docs (1)

### SSP Coordination
- 4 ad-hoc calls with Kobi Shitrit (SSP)
- Topics discussed:
  - SRv6 feasibility in Azure — official position is it won't happen, need to communicate to CheckPoint
  - NAT GW topology — 2 per tenant (1 mgmt + 1 egress)
  - Ephemeral SSD — 30GB sufficient, no extra SSD needed
  - Load Balancer role — clarification on what it's used for (not E-W, not N-S, not egress)
- Also: coordinated PG outreach to Brian Lehr re SRv6

### Customer Communication
- 1 Teams call with John Smith (john.smith@checkpoint.com), 15 min
- 3 messages exchanged — topics: deployment timeline confirmation, SRv6
  alternative approach feedback, shared updated architecture diagram
- Chat: "John Smith (CheckPoint)" (1:1)

### Engineering Coordination
- Email to blehr@microsoft.com (Azure Networking PG): SRv6 requirements for SASE

### Summary
Design work for SASE — SRv6 feasibility analysis, NAT GW topology,
ephemeral storage assessment, LB role clarification. 4 ad-hoc calls with SSP
(Kobi Shitrit). 1 call + 3 messages with customer (John Smith). Coordinated
with Azure Networking PG on SRv6 support. 3 commits.

---

## 2026-04-21

**Type:** Architecture Design Session
**Sources:** repo (21 commits)
**Duration:** 480 min (8h) — repo span 09:15-17:45 (capped at 8h)

### Repo Work
- 21 commits in ~/SASE: PoP topology, traffic flow diagrams (6 scenarios),
  HA/failover, service functions, VPP/DPDK design, inter-PoP connectivity,
  addressing, control plane proposals
- Prefix breakdown: design (18), docs (3)

### Summary
Full design sprint for SASE — 10 architecture areas with draw.io diagrams.
Covered PoP topology (4-subnet model), 6 traffic flow scenarios, HA/failover
model (4 failure domains), service function chain model, VPP/DPDK and SRv6
fabric design. 21 commits.

---
```

### Writing Rules

1. **Create file if missing.** If `activity-log.md` doesn't exist, create it with the header:
   ```markdown
   # Activity Log — {Customer Display Name} / {Project Display Name}
   ```

2. **Prepend new entries.** Insert after the `# Activity Log` header line, before any existing `## ` date entry. Most recent date first.

3. **Separator.** Add `---` between date entries for readability.

4. **Commit to git.** After writing:
   ```bash
   cd ~/customer-engagements/{customer}
   git add projects/{project}/activity-log.md
   git commit -m "activity-log: {date} — {activity-type} ({sources summary})"
   ```

## Step 5b: Write communications/ (detailed chat & email records)

In addition to the summary in `activity-log.md`, write the **full relevant content**
of text-based sources to the `communications/` folder. This preserves the actual
messages for reference, search, and audit — while `activity-log.md` has the summary.

### File naming convention

One file per source per date:

```
communications/{date}-{source-type}.md
```

Examples:
- `communications/2026-04-23-customer-chat.md`
- `communications/2026-04-23-ssp-chat.md`
- `communications/2026-04-23-email-pg.md`

### File format for chat records

```markdown
# {Source Type} Summary — {Month Day, Year}

**Chat:** {chat topic or "(unnamed) member list"}
**Participants:** {external member name (email)}, {other members}
**Messages:** {N} relevant ({M} filtered as off-topic) | **Duration:** ~{X} min

---

## Key Topics

### 1. {Topic Title}
{2-4 sentence summary of what was discussed, decided, or raised. Include who
said what when it matters. Capture technical specifics — architecture choices,
numbers, product names, blockers — not just "they discussed networking".}

### 2. {Topic Title}
{Summary...}

## Action Items
- [ ] {Who} to {do what} (re: {topic context})
```

**Summary writing rules:**
- **Summarize, don't copy-paste.** Group related messages into topics. Write a
  coherent narrative of what was discussed, not a message-by-message transcript.
- **Preserve technical specifics.** Don't genericize. "Yafim compiled DPDK with
  MANA driver" is better than "discussed compilation progress".
- **Extract action items.** Any commitment, request, or next step mentioned in
  the conversation becomes a checkbox item.
- **Include who.** Name the person who raised a point, made a decision, or took
  an action — this matters for follow-up.
- **Language.** Write summaries in English even if the conversation was in Hebrew.
  Preserve technical terms and proper nouns in their original form.

### File format for email records

```markdown
# Email Coordination — {Month Day, Year}

---

### {HH:MM} — To: {recipients}
**Subject:** {subject}
{email preview/body excerpt — relevant portions only}
```

### Writing rules for communications/

1. **Only write for sources with relevant content.** No file for a source that had
   zero relevant messages after classification.
2. **Only include messages classified as Relevant** in Step 2f. Off-topic messages
   are silently excluded. Note the filtered count in the header.
3. **Idempotent.** If the file already exists for that date+source, skip it. If
   re-logging, replace it.
4. **Commit together** with the activity-log.md entry:
   ```bash
   cd ~/customer-engagements/{customer}
   git add projects/{project}/activity-log.md projects/{project}/communications/
   git commit -m "activity-log: {date} — {activity-type} ({sources summary})"
   ```

---

## Step 6: Report

After processing all target dates and all customer/projects, present a summary:

```
📋 Daily Activity Log — April 22, 2026

Logged:
  ✅ CheckPoint / SASE — Design (21 repo commits)
  ✅ Clal Insurance / AI Search — Meeting Call (1 meeting, 14:00-15:30)

Auto-discovered chats:
  🔍 Clal Insurance — "EXT | 2604230050000351" (content-based: AI Foundry PE debugging)
  🔍 Clal Insurance — 1:1 with Orel Yitzhakian (content-based: Bastion deployment for rg-ai-clal-dev-swe)

Skipped (already logged):
  ⏭️ CheckPoint / SASE — April 21 already in activity-log.md

No activity detected:
  ⚪ Sapiens / Digital-AI — no commits, no meetings, no emails

No CRM mapping (logged but won't sync):
  ⚠️ Sapiens — run /crm-activity-sync setup to add CRM mapping
```

---

## Automation

When running as a scheduled automation (e.g., daily at 07:30):

1. Run for yesterday (or last workday).
2. **Auto-discover customers** by scanning `~/customer-engagements/*/crm-mapping.json` — process every customer that has a `crm-mapping.json` with `customer_type` set. No hardcoded customer list.
3. Skip already-logged dates.
4. Send a Teams summary only if new entries were created.
5. No user interaction — fully automated.

**Automation prompt:**
```
Run /daily-activity-log for yesterday.
Auto-discover all customers by scanning ~/customer-engagements/*/crm-mapping.json —
process every customer that has a crm-mapping.json with customer_type set.
Skip already-logged dates.
If new entries were created, send a brief Teams summary.
If errors occur, include them in the summary.
```

---

## Edge Cases

| Case | Behavior |
|---|---|
| Repo has commits but project has no crm-mapping.json | Log anyway — activity-log.md is useful even without CRM |
| Calendar returns no events | Fine — log repo work only |
| M365 not signed in | Skip calendar + email + Teams chat. Log repo work only. Warn in report. |
| Multiple repos for one project | Merge all commits into one entry. List each repo path in the "Repo Work" section. |
| Repo has commits by someone else (pair programming) | `--author` filter ensures only user's commits are counted. If zero → skip. |
| Weekend date | Log anyway — SEs sometimes work on non-standard days (CritSits, deadlines). If no evidence found, report "No activity detected." |
| Empty day (no evidence from any source) | No entry created. Report as "No activity detected." |
| Very large commit count (>50) | Summarize at topic level, don't list individual commits. Show count only. |
| Commit message has no prefix | Use project's `default_activity_type`. In the entry, list as "general" prefix. |
| Customer chat found but no `domains` configured | Skip domain-based discovery for that customer, but content-based discovery (2g) may still find chats. |
| Chat has both customer + SSP members | Classify as customer chat (2e), not SSP chat (2d). Customer participation takes precedence. |
| Customer chat call overlaps with calendar meeting | Calendar event takes precedence for that time slot. Don't double-count the same meeting from both sources. |
| Multiple customer chats match the same customer | Merge evidence from all chats into one entry per customer/project/date. |
| Chat member domain doesn't match any customer | Don't skip — Step 2g (content-based) may still match it by reading messages. |
| Unmapped chat references customer by name in content | Step 2g classifies it, extracts evidence, and auto-caches for future runs. |
| Unmapped chat references Azure resources (RG, VNet, subscription) matching a customer | Step 2g matches resource naming patterns to customer environments. |
| EXT / CritSit / ICM support case chat | Step 2g reads messages, matches customer by context, and logs as Tech Support or Blocker Escalation. |
| 1:1 with colleague about customer work | Step 2g reads messages, detects customer-related content, and attributes to the correct customer. |
| Content-based match is ambiguous (could be 2 customers) | Interactive: ask user. Automated: best-guess + flag "auto-classified — verify." |
| Content-based discovers a completely new customer | Flag as "Unknown customer" in report. Do NOT auto-create customer-engagements folder. Ask user in interactive mode. |

---

## New User Adoption Guide

When this skill is installed by a new Clawpilot user, the following setup happens
automatically on first run (when `~/.copilot/crm-activity-sync/config.json` is
missing). This skill shares its config with `/crm-activity-sync`.

### First-Run Checklist

 Prompt: "Run `/crm-activity-sync`  it sets up yourfirst 
   profile, customers, and CRM mappings that this skill depends on."

 Guide user through customer discovery:
   - Scan recent calendar for external attendee domains
   - Ask user to confirm which are customers
   - Create `customer-engagements/` folder structure

 Needed for calendar + email + Teams chat scanning.
   Test with `m_m365_status`. Sign in if needed.

 For each customer project with a local
   git repo, register via `/daily-activity-log add-repo`.

 For customer-specific Teams groups
   with SSPs, register via `/daily-activity-log add-group-chat`.

### What Gets Personalized

| Item | Where stored | Notes |
|---|---|---|
| Git author email | Auto-detected from `git config user.email` per repo | No config needed |
| Customer folders | `~/customer-engagements/` | Created during `/crm-activity-sync` setup |
| Work repos | `crm-mapping.json` per customer | Registered manually |
| SSP chat IDs | `crm-mapping.json` per customer | Resolved via `m365_create_chat_by_email` |
| Group chat IDs | `crm-mapping.json` per project | Registered manually |
| Customer domains | `crm-mapping.json` per customer `domains[]` | Registered via `add-domain` or auto-discovered from calendar |
| Customer chat IDs | `crm-mapping.json` per customer `customer_chat_ids[]` | Auto-discovered via `discover-chats` or during daily runs |
| Subject keywords | `crm-mapping.json` per project | Set during setup, editable |
| Manager email (for filtering) | `config.json` | Auto-discovered via M365 Graph |
| Work week days | `config.json` | Israel: Sun-Thu, configurable |

### Sharing This Skill

To share with another SE:
1. Give them the `SKILL.md` files for both `/daily-activity-log` and `/crm-activity-sync`
2. They install in their Clawpilot (`~/.copilot/m-skills/`)
3. On first run, the setup flow personalizes everything for their identity, customers,
   and  no manual editing of SKILL.md neededrepos 
4. Examples in this file use "RBH" / "CheckPoint" / " these are illustrativeKobi" 
   only, not hardcoded logic
