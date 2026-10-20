---
name: sa-planner
description: Daily or weekly todo list and planning for SAs. Use when the user says "todo list", "create a todo list", "weekly todo list", "daily planner", "weekly plan", "what's on my plate", "what do I need to do today", "what do I need to do this week", "start my day", "morning brief", "what should I work on", "plan my week", "plan my day", "what's coming up", or anything about creating/generating a task list or planner. Aggregates Calendar, meeting notes, Gmail, and Salesforce data into a prioritized brief with proactive recommendations.
user-invocable: true
context: fork
agent: general-purpose
model: opus
---

# SA Planner

Generates a prioritized daily or weekly brief that tells SAs what to **initiate**, not just what's overdue. Aggregates Calendar, meeting notes, Gmail, and Salesforce data, then layers on proactive recommendations: meeting prep, expansion plays, relationship-building, and strategic account moves.

**Announce at start:** "I'm using the sa-planner skill to build your prioritized task list."

## Differentiation from Related Skills

This skill consolidates and layers proactive intelligence on top of data that other skills handle individually:
- **`uco-hygiene-review`** / **`uco-next-steps`** — Focus on UCO field hygiene and drafting next steps. sa-planner uses UCO data as *input* to proactive signals (expansion, at-risk, stalled), not as the primary output.
- **`dsa-weekly-report`** / **`dsa-status-update`** — DSA-specific reporting formats (hours, deliverables, bandwidth). sa-planner targets SA workflows with calendar/Gmail/meeting-notes aggregation and consumption-weighted prioritization.
- **`renewal-risk-analyzer`** — Deep-dive risk scoring for a single account. sa-planner surfaces lightweight at-risk flags across the full book as part of a broader daily/weekly brief.

## Rules

- **Proactive over reactive:** Lead with what the SA should initiate (prep, outreach, demos, expansion conversations). UCO hygiene alerts are supporting data, not the headline.
- **Output:** Show short progress labels before each phase ("Scanning calendar...", "Checking meeting notes...", "Pulling Salesforce UCOs..."). Never show raw API responses, IDs, or tokens.
- **Interaction:** All interaction is natural language. No menus. If context is missing, ask in plain text.
- **Prioritization:** Proactive opportunities first (meeting prep, strategic outreach), then action items with deadlines, then UCO hygiene.
- **No duplicates:** Deduplicate across sources — if an action item appears in both meeting notes and Gmail, show it once.

## User Input

The user can provide optional context alongside their request. Parse the user's message for any of these before starting:

| Input | Example | How it's used |
|-------|---------|---------------|
| **Focus accounts** | "focus on Acme and GlobalCorp" | Only show data for named accounts; skip the rest |
| **Consumption context** | "MegaCorp is down because they decommissioned a legacy cluster" | Annotate the account row with user's note instead of flagging as at-risk |
| **Time horizon** | "just this afternoon", "next 3 days" | Override default daily/weekly scope |
| **Skip sources** | "skip gmail", "no slack" | Don't query that source |
| **Account notes** | "QBR with GlobalCorp is Thursday", "Acme POC extends to 3/15" | Include as pinned context in the relevant account section |

If the user provides focus accounts, scope ALL phases (calendar, meeting notes, Gmail, Salesforce) to only those accounts. This dramatically reduces data and speeds up the brief.

Store any user-provided context in `~/.vibe/sa-planner/user_context.json` so subsequent runs within the same day remember it. Format:

```json
{
  "date": "2026-03-11",
  "focus_accounts": ["Acme Corp"],
  "notes": { "MegaCorp": "consumption down due to legacy cluster decommission" },
  "skip_sources": ["slack"]
}
```

**Staleness check:** At the start of Phase 0, actively check and delete stale context:

```bash
# Delete stale user_context.json if date != today
CONTEXT_FILE="$HOME/.vibe/sa-planner/user_context.json"
if [ -f "$CONTEXT_FILE" ]; then
  STORED_DATE=$(python3 -c "import json; print(json.load(open('$CONTEXT_FILE')).get('date',''))" 2>/dev/null)
  TODAY=$(date +%Y-%m-%d)
  if [ "$STORED_DATE" != "$TODAY" ]; then
    rm "$CONTEXT_FILE"
    echo "Cleared stale context from $STORED_DATE"
  fi
fi
```

This runs before any cache reads so stale context never leaks into the current session.

## Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| **Daily** (default) | "today", "daily", "morning", "start my day" | Today's calendar + last 7 days of meeting notes (action items only) + starred Gmail |
| **Weekly** | "this week", "weekly", "what should I work on" | This week's calendar + last 7 days of meeting notes + Gmail + proactive signals |

If the user doesn't specify, default to **daily**.

## Prerequisites

**Run all 3 auth checks in a single message as parallel Bash calls:**

```bash
# Call 1 — Google auth
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
python3 "$GOOGLE_AUTH" token 2>/dev/null
```

```bash
# Call 2 — Salesforce auth
sf org display 2>/dev/null
```

```bash
# Call 3 — Logfood auth (needed for book of accounts / consumption data)
databricks auth describe --profile logfood 2>/dev/null
```

These are independent — launch all 3 simultaneously. If any auth fails, tell the user to run `/google-auth`, `/salesforce-authentication`, or `/databricks-authentication` (logfood profile) first. Continue with whichever sources are available — degrade gracefully. Without Logfood, the book of accounts will show accounts without consumption weighting.

## Performance

**Target: < 45 seconds for daily mode, < 90 seconds for weekly mode.**

Key optimizations:
- Prerequisites: 3 auth checks run as parallel Bash calls in one message
- Phase 0 cache-hit path: read cache files + launch Phase 1 agents all in one message (no extra round-trip)
- Phase 1: ALL 5 agents launch simultaneously in a single message (Calendar, Meeting Notes, Gmail, Salesforce, Slack)
- Meeting notes: only extract action-item lines, don't read full docs
- Daily mode: scoped Salesforce query (only UCOs needing action), no SA Insights
- Focus-account mode: all queries scoped to named accounts only

## Workflow

```
Prerequisites ──> Phase 0 (cached) ──> Phase 1 (ALL parallel) ──────> Phase 2 ──> Phase 3
  3 parallel          Load/build        Agent A: Calendar               Merge      Output
  auth checks         book of           Agent B: Meeting Notes          Enrich
                      accounts          Agent C: Gmail                  Prioritize
                                        Agent D: Salesforce
                                        Agent E: Slack (optional)
```

**Cache-hit fast path:** If both `accounts.json` and `consumption.json` are fresh, read them with parallel Bash calls AND launch all Phase 1 agents in the same single message. This eliminates the round-trip between Phase 0 and Phase 1.

### Phase 0: Load Account Data (two-layer cache)

```bash
mkdir -p ~/.vibe/sa-planner
```

Phase 0 uses two separate caches with different refresh cadences:

| Cache | File | TTL | Refresh trigger |
|-------|------|-----|-----------------|
| **Accounts** | `~/.vibe/sa-planner/accounts.json` | 30 days | Account assignments rarely change (typically annual territory planning). Force refresh with `/sa-planner refresh accounts`. |
| **Consumption** | `~/.vibe/sa-planner/consumption.json` | 8 hours | Consumption data lands in `fin_live_gold` on a daily batch. 8 hours means morning and afternoon runs see fresh data, but back-to-back runs within a work session don't re-query. |

**Cache check logic:**
1. Read `accounts.json` — if missing or > 30 days old, run Step 0B (account query)
2. Read `consumption.json` — if missing or > 8 hours old, run Step 0C (consumption query using cached account IDs)
3. If both caches are fresh, skip to Phase 1 (instant)

#### 0A: Identify the User

Read the vibe profile (created by the `vibe-profile` agent during setup). This is the source of truth for user identity.

```bash
cat ~/.vibe/profile 2>/dev/null
```

Extract from profile: `user.name`, `user.email`, `user.salesforce_id`. If the profile exists and has these fields, skip the fallback.

**Fallback** (if no vibe profile or missing Salesforce ID):

```bash
sf org display --json 2>/dev/null
```

If neither works, ask the user to run the `vibe-profile` agent first or provide their Databricks email.

#### 0B: Account Discovery (runs once per ~30 days)

Query `AccountTeamMember` for the SA's assigned accounts.

Reference: `salesforce-actions` → `resources/LOGFOOD_QUERIES.md` → "My Accounts" section.

```bash
databricks auth describe --profile logfood 2>/dev/null
```

```sql
-- Discover SA's book of accounts
SELECT DISTINCT a.Id AS account_id, a.Name AS account_name, atm.TeamMemberRole
FROM main.sfdc_bronze.accountteammember atm
JOIN main.sfdc_bronze.account a ON atm.AccountId = a.Id
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
AND atm.UserId = '<USER_SF_ID>'
AND atm.TeamMemberRole IN ('Primary Solution Architect', 'Solution Architect', 'Specialist Solution Architect')
ORDER BY a.Name
```

**Error handling:** If this returns 0 rows, tell the user: "No accounts found for your Salesforce ID. This can happen if your AccountTeamMember role doesn't match (Primary Solution Architect, Solution Architect, Specialist Solution Architect), or if your Salesforce ID is incorrect. Check your vibe profile with `cat ~/.vibe/profile` or run `/configure-vibe` to fix it." Do NOT proceed with an empty book — the rest of the skill depends on account data.

Write to `accounts.json`:

```json
{
  "generated_at": "2026-03-02T08:00:00Z",
  "user": { "name": "Calvin Min", "email": "calvin.min@databricks.com", "sf_id": "005..." },
  "accounts": [
    { "name": "Acme Corp", "account_id": "001...", "role": "Primary Solution Architect" },
    { "name": "GlobalCorp", "account_id": "001...", "role": "Solution Architect" }
  ]
}
```

#### 0C: Consumption Refresh (runs every ~8 hours)

Pull trailing consumption for the cached account IDs. Single query — no need to re-discover accounts.

Reference: `logfood-querier` → `resources/FIN_LIVE_GOLD.md`.

```sql
-- Trailing consumption per account with MoM trend
SELECT
  a.Name AS account_name,
  a.Id AS account_id,
  SUM(CASE WHEN f.date >= CURRENT_DATE - 30 THEN f.list_cost_dollars ELSE 0 END) AS last_30d_dollars,
  SUM(CASE WHEN f.date BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE - 31 THEN f.list_cost_dollars ELSE 0 END) AS prev_30d_dollars,
  ROUND(
    (SUM(CASE WHEN f.date >= CURRENT_DATE - 30 THEN f.list_cost_dollars ELSE 0 END) -
     SUM(CASE WHEN f.date BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE - 31 THEN f.list_cost_dollars ELSE 0 END))
    / NULLIF(SUM(CASE WHEN f.date BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE - 31 THEN f.list_cost_dollars ELSE 0 END), 0) * 100
  , 1) AS mom_change_pct
FROM main.fin_live_gold.daily_workspace_sku_aggregated f
JOIN main.sfdc_bronze.account a ON f.sfdc_account_id = a.Id
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE f.sfdc_account_id IN (<ACCOUNT_IDS_FROM_CACHE>)
AND f.date >= CURRENT_DATE - 60
GROUP BY a.Name, a.Id
ORDER BY last_30d_dollars DESC
```

**Error handling:** If the Logfood query times out or fails, log the error in the footer as a gap and continue without consumption data. Set all account weights to "unknown" and skip consumption-based signals.

#### 0D: Assign Weights

Merge account + consumption data and assign weights. If the user provided consumption context (e.g., "MegaCorp is down because of decommission"), store that note alongside the weight — it overrides the at-risk flag for that account.

| Signal | Weight |
|--------|--------|
| Consumption > $50K/month | High |
| Consumption $10K-$50K/month | Medium |
| Consumption < $10K/month | Low |
| MoM declining > 10% | Boost (at-risk) — unless user provided context explaining the decline |
| MoM growing > 20% | Boost (expansion) |

Write to `consumption.json`:

```json
{
  "generated_at": "2026-03-02T08:00:00Z",
  "accounts": [
    { "account_id": "001...", "name": "Acme Corp", "last_30d_dollars": 85000, "prev_30d_dollars": 72000, "mom_change_pct": 18.1, "weight": "high", "signals": ["growing"] }
  ]
}
```

**Force refresh:** The user can say "refresh accounts" or "refresh consumption" to force a cache rebuild.

### Phase 1: Data Collection (ALL PARALLEL)

**CRITICAL: Launch ALL agents in a single message using the Agent tool with `run_in_background: true`.** Every agent below is independent — they share no state and need no results from each other. Do NOT wait for one to finish before launching the next. Each source is optional — if one fails, skip it and note the gap in the output.

Scope all queries to accounts in the Phase 0 book. If the user specified focus accounts, filter to only those.

**Spawn ALL of these agents in ONE single message (4-5 parallel Agent tool calls).**

Each agent prompt MUST include:
- The mode (daily or weekly)
- The account list from Phase 0 (names + IDs) so the agent can scope its queries
- The user's Salesforce ID (for Agent D)
- Any focus-account filter from user input

#### Agent A: Calendar (Google)

**Agent prompt must include:** mode (daily/weekly), account names for matching attendees.

```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

GCAL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-calendar/resources/gcal_builder.py 2>/dev/null | sort -V | tail -1)
```

**Daily mode** — today only:
```bash
TODAY_START=$(date -u +"%Y-%m-%dT00:00:00Z")
TODAY_END=$(date -u +"%Y-%m-%dT23:59:59Z")
python3 "$GCAL_BUILDER" list --time-min "$TODAY_START" --time-max "$TODAY_END" --max-results 20
```

**Weekly mode** — today through end of week:
```bash
TODAY_START=$(date -u +"%Y-%m-%dT00:00:00Z")
WEEK_END=$(python3 -c "from datetime import datetime, timedelta; d=datetime.utcnow(); print((d + timedelta(days=7-d.weekday())).strftime('%Y-%m-%dT23:59:59Z'))")
python3 "$GCAL_BUILDER" list --time-min "$TODAY_START" --time-max "$WEEK_END" --max-results 30
```

Extract from calendar: event title, time, attendees. Classify each meeting:
- **Customer meeting:** has non-@databricks.com attendees → match to book accounts by attendee domain/name
- **Internal meeting:** all @databricks.com attendees
- **Prep needed:** customer meeting with no agenda in description and no linked doc

#### Agent B: Meeting Notes — action items only (Google Drive)

**Agent prompt must include:** mode, account names for matching docs.

First, check if logcall config exists and extract the root folder ID:

```bash
CONFIG_FILE="$HOME/.claude/fe-meeting-notes/config.json"
if [ -f "$CONFIG_FILE" ]; then
  ROOT_FOLDER_ID=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('root_folder_id', ''))" 2>/dev/null)
  echo "Root folder: $ROOT_FOLDER_ID"
else
  echo "NO_LOGCALL_CONFIG"
fi
```

**If no logcall config exists:** Skip meeting notes entirely. Report in agent output: "Meeting notes unavailable — no logcall config found. Run `/logcall` to set up meeting notes integration."

**If config exists:** Search Drive for recent meeting docs:

```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

CUTOFF=$(python3 -c "from datetime import datetime, timedelta; print((datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'))")
curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.document'+and+modifiedTime>'${CUTOFF}'+and+'${ROOT_FOLDER_ID}'+in+parents&orderBy=modifiedTime+desc&pageSize=5&fields=files(id,name,modifiedTime)&supportsAllDrives=true&includeItemsFromAllDrives=true&corpora=allDrives" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"
```

If the direct parent query returns nothing (docs nested in subfolders), fall back to name-based search:

```bash
curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.document'+and+name+contains+'Meeting'+and+modifiedTime>'${CUTOFF}'&orderBy=modifiedTime+desc&pageSize=5&fields=files(id,name,modifiedTime)&supportsAllDrives=true&includeItemsFromAllDrives=true&corpora=allDrives" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**Do NOT read the full document.** For each doc, export as plain text via `https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=text/plain`, then extract only lines matching action-item patterns:

- `- [ ]` (markdown checkboxes)
- `Action:` or `Action item:`
- `TODO:` or `To do:`
- `Follow up:` or `Follow-up:`
- `Next step:` or `Next steps:`
- `AI:` (common shorthand for "action item")
- Lines starting with `→` or `=>` (arrow-prefixed action items)

Discard everything else.

**Limitation:** These patterns are heuristic — they won't catch action items written as plain prose (e.g., "Calvin will send the POC results by Friday"). If the user reports missing items, suggest they adopt one of the patterns above in their meeting notes, or switch to a more structured template via `/logcall`.

#### Agent C: Gmail (skip if user said "skip gmail")

**Agent prompt must include:** mode, account names and their known email domains from the book of accounts.

**Build the search query with account filtering baked in** so filtering happens at the Gmail API level, not post-fetch. This prevents the cap from dropping relevant customer emails.

```bash
GMAIL_UTIL=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_utils.py 2>/dev/null | sort -V | tail -1)
```

**Construct the query dynamically** from the book of accounts. Use account domains and names:

```bash
# Example for 3 accounts — build this from the actual book of accounts
# Combine starred + account-scoped: domains from book + account names in subject
python3 "$GMAIL_UTIL" search "is:starred newer_than:7d (from:@acme.com OR from:@globalcorp.com OR from:@newco.io OR subject:Acme OR subject:GlobalCorp OR subject:NewCo)"
```

**If focus accounts are set**, only include those accounts in the query — this makes the search even tighter.

**Domain extraction:** Use the account names from Phase 0 to infer likely domains (e.g., "Acme Corp" → `@acme.com`, `@acmecorp.com`). If the book of accounts includes contact email domains from Salesforce, use those directly. When unsure, include both the company name in `subject:` and best-guess domain in `from:` — Gmail OR logic ensures no false negatives.

**If the account list is very large (20+ accounts)**, the query string may exceed Gmail's limit. In that case, fall back to `is:starred newer_than:7d` without account filtering, then post-filter results. Note this fallback in the agent output.

Extract: subject, sender, date, snippet. Cap at **10 threads** for daily, **20 for weekly** (higher caps are safe now that filtering is pre-fetch).

#### Agent D: Salesforce UCOs + Blockers

**Agent prompt must include:** mode (daily/weekly), user's Salesforce ID, account IDs if focus-account filter is set.

**Daily mode — scoped query** (only UCOs that need action NOW):

```bash
sf data query --query "SELECT Id, Name, Account__r.Name, Status__c, Next_Steps__c, Next_Steps_Date__c, Use_Case_Stage__c, LastModifiedDate, Technical_Win__c, POC_Start_Date__c, POC_End_Date__c, (SELECT Id, Name, Status__c, Priority__c, Description__c FROM Blockers__r WHERE Status__c != 'Closed') FROM UseCase__c WHERE (OwnerId = '<USER_SF_ID>' OR Primary_Solution_Architect__c = '<USER_SF_ID>' OR Solution_Architect__c = '<USER_SF_ID>' OR rsa__c = '<USER_SF_ID>' OR DSA__c = '<USER_SF_ID>') AND Use_Case_Stage__c IN ('U1 - Identified','U2 - Evaluated','U3 - PoC/Testing','U4 - Production Approved','U5 - Scaled') AND (Next_Steps_Date__c <= NEXT_N_DAYS:3 OR Next_Steps_Date__c = null OR POC_End_Date__c <= NEXT_N_DAYS:7 OR LastModifiedDate < LAST_N_DAYS:14) ORDER BY Next_Steps_Date__c ASC NULLS FIRST LIMIT 200" --json
```

**Weekly mode — full query** (all active UCOs for portfolio view):

```bash
sf data query --query "SELECT Id, Name, Account__r.Name, Status__c, Next_Steps__c, Next_Steps_Date__c, Use_Case_Stage__c, LastModifiedDate, Technical_Win__c, POC_Start_Date__c, POC_End_Date__c, (SELECT Id, Name, Status__c, Priority__c, Description__c FROM Blockers__r WHERE Status__c != 'Closed') FROM UseCase__c WHERE (OwnerId = '<USER_SF_ID>' OR Primary_Solution_Architect__c = '<USER_SF_ID>' OR Solution_Architect__c = '<USER_SF_ID>' OR rsa__c = '<USER_SF_ID>' OR DSA__c = '<USER_SF_ID>') AND Use_Case_Stage__c IN ('U1 - Identified','U2 - Evaluated','U3 - PoC/Testing','U4 - Production Approved','U5 - Scaled') ORDER BY Use_Case_Stage__c, Next_Steps_Date__c ASC NULLS FIRST LIMIT 200" --json
```

**Note:** Both queries include `LIMIT 200` as a safety cap. If results are truncated (the `sf` CLI shows `done: false` or `totalSize` exceeds 200), note the truncation in the footer so the SA knows not all UCOs are shown.

#### Agent E: Slack (Optional — skip if MCP unavailable or user said "skip slack")

```
mcp__slack__slack_read_api_call: search.messages with query "to:me" limit 5
```

If Slack MCP call fails or times out after 10 seconds, skip silently.

### Phase 2: Merge, Enrich, and Prioritize

Wait for all background agents to complete. Merge results.

#### 2A: Proactive Signal Detection

This is what makes the planner valuable — it identifies what the SA should **initiate**, not just what's overdue. Apply these signals to BOTH daily and weekly modes:

**Meeting prep signals** (from Agent A calendar data):
- Customer meeting today/tomorrow with no agenda or linked doc → "Prep needed — run `/customer-meeting-prep` for [Account]"
- Customer meeting with a new attendee title containing VP/Director/C-level/Head → "Executive in the room — review account context and prepare talking points"
- First meeting with an account in 14+ days → "Re-engagement meeting — review what's changed since last contact"

**Expansion signals** (from Phase 0 consumption + Agent D UCOs):
- Consumption growing >20% MoM but no new UCOs in 30 days → "Uncaptured growth — consumption is outpacing tracked use cases. Schedule a discovery call to identify what they're building."
- Account has only U4/U5 UCOs (all scaled/prod) but consumption is growing → "Mature account expanding organically — explore new workloads (AI/ML, streaming, Lakebase) with a proactive demo"
- Account consuming a product SKU (e.g., model serving, vector search) with no UCO for that workload → "New workload detected in consumption — create a UCO to track and support it"

**Relationship signals** (from Agent A + Agent B):
- No customer meeting with a HIGH-weight account in 14+ days → "Going dark on [Account] — schedule a check-in or forward relevant content"
- Meeting notes mention a stakeholder name you haven't met with in 30+ days → "Champion going cold — re-engage [Name] with a use case update or relevant content"
- Account has active UCOs but all recent meetings are internal (no customer attendees) → "Internal-only activity — make sure the customer is still engaged"

**Technical win signals** (from Agent D UCOs):
- U3 POC ending within 7 days with positive signals (no open blockers, recent meetings) → "POC wrapping up — prepare results deck and schedule tech win call"
- U4 approved but no activity in 14 days → "Production approved but not moving — reach out to confirm deployment timeline and offer enablement"
- Multiple UCOs at the same account in U2 → "Multiple evaluations in flight — consider a consolidated architecture session instead of separate meetings"

**Competitive signals** (from Agent B meeting notes):
- Meeting notes mention competitor names (Snowflake, Fabric, Redshift, BigQuery, Cloudera) → "Competitive mention at [Account] — run `/competitive-analysis` to prep"

#### 2B: UCO Hygiene Flags

These are secondary to proactive signals — important but reactive. Flag only UCOs with clear actions needed:
- Next steps overdue or missing → update required
- U3 past POC end date → close out or extend
- Open High/Critical blockers → escalate
- U4 with no Technical Win → confirm win
- Weekly only: U2 for 14+ days with no POC start date, U1 for 30+ days

#### 2C: Ordering

**Priority order within each output section:**
1. Proactive opportunities (prep, outreach, expansion) — these are the highest-leverage actions
2. Time-sensitive items (today's meetings, deadlines within 3 days)
3. Action items from meeting notes and email
4. UCO hygiene flags

Within each group, order by account weight: High > Medium > Low. At-risk accounts (declining >10% MoM, without user-provided context) boosted regardless of tier.

**Daily mode sections:** Proactive Plays, Meetings Today, Open Action Items, UCO Alerts (if any)
**Weekly mode adds:** Book Summary, SA Insights, Use Cases by Stage (aggregated from Agent D results by `Use_Case_Stage__c`), Full Proactive Opportunities

### Phase 2D: Generate SA Insights (WEEKLY MODE ONLY)

**Skip entirely in daily mode.** Daily should be a fast brief.

In weekly mode, analyze cross-source patterns:

**Time allocation** — count meetings per account weight tier this week. Flag if LOW-weight accounts get more meeting time than HIGH-weight.

**Follow-up gaps** — cross-reference calendar events from the past 7 days against logcall docs. Flag customer meetings with no notes logged.

**UCO velocity** — flag UCOs that moved stages (positive) or have been stuck 30+ days (negative).

**Coverage map** — for each book account, show: last meeting date, number of active UCOs, consumption trend. Highlight gaps (no meeting, no UCOs, declining consumption).

**Top 3 actions** — synthesize the most important proactive moves into 3 concrete next steps. These should be forward-looking (schedule X, prepare Y, initiate Z), not backward-looking (update UCO, log notes).

### Phase 3: Output

Print the brief to the terminal. Group by category, use plain language headers.

**Daily mode — lead with proactive plays:**

```
SA Daily Brief — Tuesday, March 11, 2026
═════════════════════════════════════════

PROACTIVE PLAYS (do these first)
─────────────────────────────────
  1. Prep for Acme Technical Review (2:00 PM)              [$85K · HIGH]
     VP of Engineering attending — no agenda found
     → Run /customer-meeting-prep for Acme Corp

  2. NewCo expanding fast — uncaptured growth              [$12K · LOW ↑]
     Consumption up 45% MoM but only 1 UCO tracked
     → Schedule discovery call to identify new workloads

  3. Contoso competitive pressure                          [$28K · MED]
     Last meeting mentioned Snowflake for streaming
     → Run /competitive-analysis Databricks vs Snowflake streaming

MEETINGS TODAY
──────────────
  2:00 PM   Acme Technical Review       [CUSTOMER · ⚠ prep needed]
  3:30 PM   Internal Team Standup       [INTERNAL]
  4:00 PM   GlobalCorp QBR              [CUSTOMER · prep doc linked]

OPEN ACTION ITEMS
─────────────────
  ☐  Send POC results to Acme team                      [from 3/7 notes]
  ☐  Reply to Sarah Chen re: Lakebase pricing           [Gmail · starred 2d]

UCO ALERTS
──────────
  Acme — DW Migration (U3): POC ends 3/14 — prep results deck
  MegaCorp — Real-Time Analytics (U4): no tech win marked

───────────
Sources: Book (7) · Calendar (4) · Notes (3) · Gmail (2) · Salesforce (5 UCOs)
```

**Weekly mode** adds book summary, full proactive section, stage breakdown, SA insights.

Include user-provided context inline. For example, if the user said "MegaCorp consumption is down because of decommission", the book table row should show:

```
  MegaCorp    $41,000    -12% MoM   MED (user: legacy cluster decommission)
```

Instead of flagging it as at-risk.

**Footer:** Always show source counts and any gaps (e.g., "Meeting notes unavailable — no logcall config", "Slack unavailable", "Consumption query timed out", "Salesforce results truncated at 200").

## Cross-References

- `/customer-meeting-prep` — deep-dive prep for meetings flagged as "prep needed"
- `/competitive-analysis` — prep materials when competitor mentions detected
- `/logcall` — capture meeting notes that feed into this planner
- `/post-call-followup` — draft follow-up emails for action items surfaced here
- `/salesforce-actions` — update UCO next steps or create new UCOs for expansion signals
- `/uco-blockers` — check blocker status on flagged UCOs
- `/support-escalation` — escalate high-priority blockers
