---
name: dsa-briefing
description: "Pilot delivery briefing system for 65 recipients across 7 persona types — DSAs, EMs, SAs, RSAs, Leader Digests, Steer Roll-up, and Executive Roll-up. Runs as a hybrid Databricks job (data prep notebook + Claude FM API compose/deliver notebook) on three schedules: 7 AM ET (Mon-Fri), 5 PM ET (Mon-Thu), 1 PM ET (Fri). Sub-commands: monday, morning, evening, friday."
user-invocable: true
model: sonnet
---

# DSA Briefing — Expanded Pilot

Full-week delivery cadence for 65 recipients across 7 persona types. One skill, four modes — each tuned to the time of day, day of week, and recipient persona.

**Usage:**
```
/dsa-briefing monday       -> Monday Outlook (ICs), Monday Digest (leaders), Monday GM Brief (exec)
/dsa-briefing morning      -> Morning Prep (ICs) — Tue-Fri AM
/dsa-briefing evening      -> Evening Summary (ICs), Evening Digest (leaders) — Mon-Thu PM
/dsa-briefing friday       -> Friday Wrap (ICs + exec), Friday Digest (leaders) — Fri PM
```

**Announce at start:** "Running briefing — pulling from SFDC, logfood, Slack, Calendar, and Drive for [N] recipients."

---

## Persona Types & Roster

| # | Persona | Count | Manager / Owner | Recipients |
|---|---------|-------|-----------------|------------|
| 1 | DSA | 24 | Zach Relli (10), Brandon Williams (14) | Direct reports of Zach and Brandon |
| 2 | EM | 4 | Vincent Delany | Tejal Nerkar, Kaleb Cisneros, Eric Winter, David Coons |
| 3 | SA | 12 | Steve Ricci (8), Bryan Li (4) | Direct reports of Steve and Bryan |
| 4 | RSA | 17 | Lan Jiang | All Lan's directs except Ghouse Mohammed and Scott Love |
| 5 | Leader Digest | 6 | — | Zach, Brandon, Steve, Bryan, Vincent, Lan |
| 6 | Steer Roll-up | 1 | — | Sandeep Vaid |
| 7 | Executive Roll-up | 1 | — | Christopher Olenik |

**Total: 65 recipients**

---

## Schedule

| Job | Time | Days | What fires |
|-----|------|------|------------|
| AM Job | 7:00 AM ET | Mon-Fri | Monday: Monday Outlook/Digest/GM Brief. Tue-Fri: Morning Prep |
| PM Job | 5:00 PM ET | Mon-Thu | Evening Summary (ICs) + Evening Digest (leaders) |
| Friday PM Job | 1:00 PM ET | Fri only | Friday Wrap (ICs + exec) + Friday Digest (leaders) |

### Mode Matrix — Who Gets What, When

| Mode | DSAs (24) | EMs (4) | SAs (12) | RSAs (17) | Leaders (6) | Steer (1) | Exec (1) |
|------|-----------|---------|----------|-----------|-------------|-----------|----------|
| Monday AM | Monday Outlook | Monday Outlook | Monday Outlook | Monday Outlook | Monday Digest | — | Monday GM Brief |
| Tue-Fri AM | Morning Prep | Morning Prep | Morning Prep | Morning Prep | — | — | — |
| Mon-Thu PM | Evening Summary | Evening Summary | Evening Summary | Evening Summary | Evening Digest | — | — |
| Friday PM | Friday Wrap | Friday Wrap | Friday Wrap | Friday Wrap | Friday Digest | — | Friday Wrap |

Sandeep Vaid (Steer Roll-up) receives a weekly roll-up — schedule TBD, not yet wired into the three jobs above.

---

## Sign-offs

Each cycle (AM, PM, Friday) uses a distinct sign-off per manager group. Applied once at the end of each message.

### Zach Relli's DSAs
- **AM:** "Have the Best Day Ever. -- Zach"
- **PM:** "Thank you for all you do! -- Zach"
- **Friday:** "These are good places to build for customer outcomes. Take a look, test yourself and build something tailored to your customer and the outcomes you want to achieve. We look forward to seeing the speed you get back from this effort!\n\nHave an AWESOME weekend :fist_right::fist_left: -- Zach"

### Brandon Williams' DSAs
- **AM:** "Have the Best Day Ever. -- Brandon"
- **PM:** "Thank you for all you do! -- Brandon"
- **Friday:** "These are good places to build for customer outcomes. Take a look, test yourself and build something tailored to your customer and the outcomes you want to achieve. We look forward to seeing the speed you get back from this effort!\n\nHave an AWESOME weekend :fist_right::fist_left: -- Brandon"

### Vincent Delany's EMs
- **AM:** "Go find the leverage."
- **PM:** "Good work today. Reset and reload."
- **Friday:** "Study the board. Next week's wins start now."

### Steve Ricci's SAs
- **AM:** "You're one of the best in the business at this. Go show them why. -- Steve"
- **PM:** "You're one of the best in the business at this. Go show them why. -- Steve"
- **Friday:** "You absolutely crushed it this week. Enjoy the weekend and come back Monday ready to close. -- Steve"

### Bryan Li's SAs
- **AM:** "Grateful to have you on this team. Let's go build something great this week. -- Bryan"
- **PM:** "Appreciate the work you put in today. Rest up. -- Bryan"
- **Friday:** "What a week. Proud to work alongside each of you. Have a great weekend. -- Bryan"

### Lan Jiang's RSAs
- **AM:** "Your work matters. Let's have a strong week."
- **PM:** "Great effort today. Take care of yourself tonight."
- **Friday:** "Proud of what you all delivered this week. Enjoy your weekend -- you earned it."

### Christopher Olenik (Executive)
- **All modes:** "Let me know what you think. -- Zach"

---

## Configuration

All values are resolved dynamically. Override via `~/.vibe/profile.yaml`:

```yaml
dsa-briefing:
  slack_channel_id: C0AHSRRE1RC          # #fy27-u4-acceleration
  logfood_profile: logfood
  logfood_warehouse_id: 74b037a3a9ec9847
  fevm_profile: fe-vm-cmegdemos
  sfdc_target_org: user@databricks.com
  propensity_dashboard_url: https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01f119021cb51021af589a7b61931a04/published
  delivery_playbook_template_id: 1pmPZ6QnlSToNhEfFv6xxaWbaAV4CqwEx5BdSghKFhQ8
  dsa_kpi_annualized_imrr: 2000000
  dsa_kpi_u4_u6_days: 80
  staging_schema: home_zach_relli.dsa_briefing  # staging tables for hybrid job

  # Roster — resolved dynamically via SFDC User query
  # SELECT Name, Email, Manager.Name FROM User
  #   WHERE Manager.Name IN (...) AND IsActive = true
  persona_groups:
    - persona: DSA
      managers: [Zach Relli, Brandon Williams]
    - persona: EM
      managers: [Vincent Delany]
      explicit_members: [Tejal Nerkar, Kaleb Cisneros, Eric Winter, David Coons]
    - persona: SA
      managers: [Steve Ricci, Bryan Li]
    - persona: RSA
      managers: [Lan Jiang]
      exclude: [Ghouse Mohammed, Scott Love]
    - persona: Leader Digest
      explicit_members: [Zach Relli, Brandon Williams, Steve Ricci, Bryan Li, Vincent Delany, Lan Jiang]
    - persona: Steer Roll-up
      explicit_members: [Sandeep Vaid]
    - persona: Executive Roll-up
      explicit_members: [Christopher Olenik]
```

If `~/.vibe/profile.yaml` has a `dsa-briefing` section, use those values. Otherwise resolve dynamically:

| Variable | Resolution | Fallback |
|----------|-----------|----------|
| `${SLACK_CHANNEL_ID}` | From profile.yaml | Ask user for channel |
| `${LOGFOOD_PROFILE}` | Check `~/.databrickscfg` for `logfood` | Ask user |
| `${SFDC_TARGET_ORG}` | `sf org display --json` | Ask user |
| `${IC_ROSTER}` | SFDC query: `WHERE Manager.Name IN (...)` + exclusion filters | From profile.yaml |
| `${SIGN_OFF}` | Matched from recipient's Manager.Name + mode -> sign-off table | `-- [Manager first name]` |
| `${STAGING_SCHEMA}` | From profile.yaml | `home_zach_relli.dsa_briefing` |

---

## Databricks Hybrid Job Architecture

The briefing runs as a two-notebook Databricks job, not as a single Claude Code invocation. This enables scale to 65 recipients within FM API rate limits.

### Notebook 1: `briefing_data_prep`

Runs on serverless compute. Gathers all structured data and writes staging tables.

**Staging tables** (`home_zach_relli.dsa_briefing.*`):

| Table | Contents |
|-------|----------|
| `run_metadata` | Current mode (monday/morning/evening/friday) + timestamp |
| `dsa_roster` | 24 DSAs: name, email, FLM |
| `dsa_ucos` | UCO portfolio per DSA |
| `dsa_summary` | Per-DSA KPIs (iMRR, pipeline, delivered) |
| `account_team` | AE, SA, SSA per account |
| `em_roster` | 4 EMs: name, email, leader |
| `em_accounts` | EM-to-account mapping via AE Director segments |
| `sa_roster` | 12 SAs: name, email, FLM |
| `sa_accounts` | SA account assignments |
| `sa_ucos` | UCO portfolio per SA |
| `rsa_roster` | 17 RSAs: name, email |
| `rsa_projects` | RSA project assignments from `resource_planner` |
| `rsa_account_ucos` | UCOs on RSA-assigned accounts |
| `propensity_scores` | From `delivery_intelligence_results` |
| `partner_matches` | From `partner_match_results` |
| `sign_off_config` | Per-leader, per-cycle sign-offs |
| `accelerators` | Accelerator catalog (Friday only) |
| `delivery_queue` | Composed messages for audit/retry |
| `delivery_log` | Delivery status per run (appended) |

### Notebook 2: `briefing_compose_and_deliver`

Runs after notebook 1. Reads staging tables, calls Claude FM API to compose personalized messages, posts Slack DMs.

**Flow:**
1. Read `run_metadata` to determine mode (monday/morning/evening/friday)
2. For each recipient, read their staging data and build context
3. Call Claude FM API (`databricks-claude-sonnet-4-5`) to compose message with persona-specific sign-off
4. Post Slack DM via Databricks external function (`slack` connection) — no separate bot token needed
5. Save composed messages to `delivery_queue` table
6. Append delivery status to `delivery_log`

---

## Data Sources

| Source | What it provides | How accessed |
|--------|-----------------|-------------|
| **SFDC (user)** | Recipient roster, manager hierarchy | logfood `sfdc_bronze.user` |
| **SFDC (usecase__c)** | UCO portfolio, stages, health, iMRR, next steps | logfood `sfdc_bronze.usecase__c` |
| **SFDC (approvalrequest__c)** | Open ASQs, due dates, status | logfood `sfdc_bronze.approvalrequest__c` |
| **SFDC (accountteammember)** | AE, SA, SSA names per account | logfood `sfdc_bronze.accountteammember` |
| **SFDC (account)** | Account names, ARR, industry | logfood `sfdc_bronze.account` |
| **Delivery Intelligence** | Propensity scores, risk signals | `home_zach_relli.path_to_production.delivery_intelligence_results` |
| **Partner Intelligence** | Partner matches, velocity scores | `home_zach_relli.path_to_production.partner_match_results` |
| **Accelerator catalog** | 1,000+ accelerators with tags, URLs | `home_zach_relli.path_to_production.accelerator_catalog` |
| **RSA projects** | Resource planner assignments | `field_professional_services.resource_planner` |
| **logfood consumption** | DBU trends (30d vs prior 30d) | `fin_live_gold.finance_usage` |
| **Slack** | Account activity, decisions, blockers | MCP `slack_read_api_call` (search) |
| **Calendar** | Meeting schedule, attendees | Google Calendar API |
| **Gmail** | Email threads about accounts | Gmail API search |
| **Drive** | Docs, decks, shared assets | Google Drive API search |

---

## Shared Step 0 — Authenticate & Discover (All Modes)

Run in parallel:

**A. SFDC** -- get full recipient roster:
```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
sf data query --query "SELECT Id, Name, Email, Manager.Name, UserRole.Name FROM User WHERE Manager.Name IN ('Zach Relli','Brandon Williams','Vincent Delany','Steve Ricci','Bryan Li','Lan Jiang') AND IsActive = true AND Email LIKE '%@databricks.com'" --target-org ${SF_TARGET_ORG} --json
```
Apply exclusion filters (remove Ghouse Mohammed, Scott Love from RSA group). Add explicit leader/steer/exec recipients.

**B. Logfood** -- confirm auth:
```bash
databricks auth token --profile ${LOGFOOD_PROFILE} 2>/dev/null | head -1
```

**C. Google** -- warm auth:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token 2>/dev/null | head -1
```

**D. Slack** -- look up recipient Slack IDs:
```
mcp__slack__slack_read_api_call("users.lookupByEmail", {"email": "<RECIPIENT_EMAIL>"})
```

**E. Get today's date and day of week:**
```bash
python3 -c "from datetime import date; d=date.today(); print(f'{d.isoformat()}|{d.strftime(\"%A\")}')"
```

If any auth fails, tell the user which skill to run (`/salesforce-authentication`, `/databricks-authentication`, `/google-auth`) and stop.

---

## Shared Step 1 — Fetch IC Portfolios (All Modes)

Run these queries in parallel via logfood warehouse. Each query scopes to the IC's SFDC User ID (DSA__c, SAOwner__c, rsa__c, or OwnerId depending on persona).

### 1a. Active UCOs

```sql
WITH deduped AS (
  SELECT uc.*, ROW_NUMBER() OVER (PARTITION BY uc.Id ORDER BY uc.ds DESC) as rn
  FROM main.sfdc_bronze.usecase__c uc
)
SELECT
  uc.Id as uco_id, uc.Name as uco_name,
  a.Name as account_name, uc.Account__c as account_id,
  uc.Stages__c as stage, uc.Implementation_Status__c as health,
  uc.MonthlyTotalDollarDBUs__c as monthly_dbus,
  SUBSTRING(uc.Demand_Plan_Next_Steps__c, 1, 200) as next_steps,
  uc.Implementation_Start_Date__c as start_date,
  uc.Full_Production_Date__c as target_date,
  uc.Competitor_Status__c as competitor,
  uc.POCStatus__c as poc_status,
  uc.DSA__c, uc.SAOwner__c, uc.rsa__c
FROM deduped uc
LEFT JOIN (
  SELECT Id, Name, ROW_NUMBER() OVER (PARTITION BY Id ORDER BY ds DESC) as rn
  FROM main.sfdc_bronze.account
) a ON uc.Account__c = a.Id AND a.rn = 1
WHERE uc.rn = 1
AND (uc.DSA__c = '${IC_USER_ID}'
   OR uc.SAOwner__c = '${IC_USER_ID}'
   OR uc.rsa__c = '${IC_USER_ID}')
AND uc.Stages__c IN ('U2','U3','U4','U5','U6')
AND NOT (uc.Stages__c = 'U6' AND uc.Full_Production_Date__c < '2025-02-01')
ORDER BY a.Name, uc.Stages__c
```

### 1b. Open ASQs

```sql
WITH deduped_ar AS (
  SELECT ar.*, ROW_NUMBER() OVER (PARTITION BY ar.Id ORDER BY ar.ds DESC) as rn
  FROM main.sfdc_bronze.approvalrequest__c ar
)
SELECT
  ar.Id, ar.Name as asq_name, a.Name as account_name,
  ar.Status__c as status, ar.Support_Type__c as support_type,
  ar.End_Date__c as due_date, ar.Request_Description__c as description
FROM deduped_ar ar
LEFT JOIN (
  SELECT Id, Name, ROW_NUMBER() OVER (PARTITION BY Id ORDER BY ds DESC) as rn
  FROM main.sfdc_bronze.account
) a ON ar.Account__c = a.Id AND a.rn = 1
WHERE ar.rn = 1
AND ar.OwnerId = '${IC_USER_ID}'
AND ar.Status__c IN ('In Progress', 'Under Review', 'On Hold', 'New')
ORDER BY ar.End_Date__c ASC
```

### 1c. Account Consumption (last 30d vs prior 30d)

```sql
SELECT
  sfdc_account_name,
  SUM(CASE WHEN date >= current_date - 30 THEN dbu ELSE 0 END) as last_30d_dbus,
  SUM(CASE WHEN date >= current_date - 37 AND date < current_date - 7 THEN dbu ELSE 0 END) as prior_30d_dbus
FROM main.fin_live_gold.finance_usage
WHERE sfdc_account_name IN ([ACCOUNT_LIST_FROM_1a])
AND dedup_rk = 1
GROUP BY sfdc_account_name
```

### 1d. Account Teams

```sql
SELECT
  a.Name as account_name,
  u.Name as team_member_name, u.Email as team_member_email,
  atm.TeamMemberRole as role
FROM main.sfdc_bronze.accountteammember atm
JOIN main.sfdc_bronze.account a ON atm.AccountId = a.Id
JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
WHERE a.Id IN ([ACCOUNT_ID_LIST_FROM_1a])
ORDER BY a.Name, atm.TeamMemberRole
```

### 1e. Delivery Intelligence & Partner Matches

```sql
-- Propensity scores
SELECT * FROM home_zach_relli.path_to_production.delivery_intelligence_results
WHERE account_id IN ([ACCOUNT_ID_LIST_FROM_1a])

-- Partner intelligence
SELECT * FROM home_zach_relli.path_to_production.partner_match_results
WHERE account_id IN ([ACCOUNT_ID_LIST_FROM_1a])
```

### 1f. RSA Projects (RSA persona only)

```sql
SELECT *
FROM field_professional_services.resource_planner
WHERE resource_email = '${IC_EMAIL}'
AND status IN ('Active', 'Planned')
ORDER BY start_date
```

### 1g. Accelerator Catalog (for friday mode, pre-fetch for others)

```sql
SELECT
  name, category, source_type, description, url,
  tags, vertical
FROM home_zach_relli.path_to_production.accelerator_catalog
WHERE tags IS NOT NULL
ORDER BY category, name
LIMIT 200
```

---

## Mode: `monday` — Monday Outlook / Digest / GM Brief

**Schedule:** AM Job, 7:00 AM ET, Monday only

### IC Recipients (DSAs, EMs, SAs, RSAs) — Monday Outlook

#### Monday Step 2 — Per-Account Research

For each unique account in the IC's portfolio (max 8), research last 7 days:
- Slack: Search "[ACCOUNT_NAME]" -- decisions, blockers, outcomes
- Calendar: Meetings with account team in last 7 and next 7 days
- Gmail: Emails mentioning account last 7 days
- Drive: Docs modified last 7 days mentioning account

#### Monday Step 3 — Generate Delivery Intelligence Playbook Docs

For each account, create or update a Google Doc ("Delivery Intelligence Playbook - [ACCOUNT_NAME]"). If multiple ICs share an account, use the same doc. Structure follows the Delivery Intelligence Runbook template.

#### Monday Step 4 — Post Slack DM to IC

```
:wave: *Monday Outlook -- [NAME] -- Week of [DATE]*

:dart: *Your Top 3 This Week:*
1. *[Account]* -- [highest leverage action + why]
2. *[Account]* -- [action + why]
3. *[Account]* -- [action + why]

:bar_chart: *Your KPIs:*
- Annualized iMRR: $[X] / $[TARGET] target ([X]%)
- Avg U4->U6: [X] days / <[TARGET] target
- Active Pipeline: [N] U4-U5 UCOs
- FY27 U6 Deliveries: [N]

:page_facing_up: *Delivery Intelligence Playbooks (updated):*
- <[DOC_URL_1]|[Account 1]>
- <[DOC_URL_2]|[Account 2]>

:calendar: *Key Meetings This Week:*
- [Day]: [Meeting] @ [Account] -- [prep notes]

${SIGN_OFF}
```

### Leader Recipients — Monday Digest

Aggregated view across all their direct reports:

```
:memo: *Monday Digest -- [LEADER_NAME] -- Week of [DATE]*

:busts_in_silhouette: *Team Snapshot ([N] directs):*
- Total Active UCOs: [N] (U4: [X], U5: [Y], U6 YTD: [Z])
- Team Annualized iMRR: $[X]
- Avg U4->U6 Cycle: [X] days

:dart: *Top Actions Across Your Team:*
1. [IC Name] @ [Account] -- [action]
2. [IC Name] @ [Account] -- [action]
3. [IC Name] @ [Account] -- [action]

:warning: *Attention Items:*
- [IC Name]: [risk or blocker needing manager attention]

${SIGN_OFF}
```

### Executive Roll-up — Monday GM Brief (Christopher Olenik)

High-level program summary:

```
:chart_with_upwards_trend: *Monday GM Brief -- Week of [DATE]*

:bar_chart: *Program Metrics (65 recipients, 7 persona types):*
- Total Active UCOs: [N] across [M] accounts
- Aggregate Annualized iMRR: $[X]
- U6 Deliveries FY27 YTD: [N]
- Avg U4->U6 Cycle: [X] days

:trophy: *Top Wins Last Week:*
- [Account] -- [outcome]
- [Account] -- [outcome]

:warning: *Risks & Escalations:*
- [Item needing exec attention]

:dart: *This Week's Focus:*
- [Strategic priority]

Let me know what you think. -- Zach
```

---

## Mode: `morning` — Daily Morning Prep (Tue-Fri)

**Schedule:** AM Job, 7:00 AM ET, Tuesday through Friday

**Recipients:** ICs only (DSAs, EMs, SAs, RSAs). Leaders and execs do NOT receive morning preps.

### Morning Step 2 — Meeting Prep

For each meeting today that involves an IC's account:
- Pull latest from Delivery Intelligence Playbook doc
- Check Slack for last 24h activity
- Identify relevant product updates

### Morning Step 3 — Post Slack DM

```
:sunrise: *[DAY_NAME] Focus -- [NAME] -- [DATE]*

:dart: *3 Things to Focus On Today:*
1. *[Account]* -- [specific action + context]
2. *[Account/Task]* -- [action + context]
3. *[Account/Task]* -- [action + context]

:calendar: *Today's Meetings:*
- [Time]: [Meeting] @ [Account]
  _Prep: [1-sentence context from playbook + recent Slack]_

:bulb: *Product Updates Relevant to Your Accounts:*
- [Update] -- relevant for [Account] ([UCO name])

${SIGN_OFF}
```

**Keep it short.** Morning DMs should be < 15 lines. No KPIs, no dashboards -- just what to do today.

---

## Mode: `evening` — Day Summary + Playbook Updates

**Schedule:** PM Job, 5:00 PM ET, Monday through Thursday

**Recipients:** ICs get Evening Summary. Leaders get Evening Digest. Executive does NOT receive evening messages.

### Evening Step 2 — Research Today's Activity

For each account the IC touched today (calendar, Slack, email), research:
- What happened (1-3 outcome-focused bullets)
- Decisions made or blockers surfaced
- What needs to happen tomorrow

### Evening Step 3 — Update Delivery Intelligence Playbooks

Update the "This Week" section of each account's Playbook doc with today's activity. Create new Playbook docs for newly touched accounts.

### Evening Step 4 — Post Slack DM to IC

```
:city_sunset: *End of Day -- [NAME] -- [DATE]*

:white_check_mark: *What You Did Today:*
- [Account] -- [outcome bullet]
- [Account] -- [outcome bullet]

:page_facing_up: *Playbooks Updated:*
- <[DOC_URL_1]|[Account 1]> _(updated)_
- <[DOC_URL_2]|[Account 2]> _(new)_

:arrow_right: *Tomorrow's Prep:*
- [Time]: [Meeting] @ [Account] -- [what to prep]

${SIGN_OFF}
```

### Evening Digest for Leaders

```
:city_sunset: *Evening Digest -- [LEADER_NAME] -- [DATE]*

:busts_in_silhouette: *Today Across Your Team:*
- [IC Name] @ [Account] -- [outcome]
- [IC Name] @ [Account] -- [outcome]

:warning: *Needs Attention:*
- [Item, if any]

${SIGN_OFF}
```

---

## Mode: `friday` — Friday Wrap / Digest

**Schedule:** Friday PM Job, 1:00 PM ET, Friday only

**No Friday evening update. No weekend updates.**

**Recipients:** ICs get Friday Wrap. Leaders get Friday Digest. Executive gets Friday Wrap.

### Friday Step 2 — Week Recap

Aggregate the full week's activity:
- UCOs that moved stages
- Consumption changes (WoW)
- Meetings held, docs created, tools shipped
- ASQs completed or escalated

### Friday Step 3 — Accelerator Matching

Match accounts to accelerator catalog:
1. Direct product match against active U4-U5 use cases
2. Competitive gap accelerators (if competitor present)
3. U3-to-U4 progression accelerators

### Friday Step 4 — Post Slack DM to IC

```
:tada: *Friday Wrap -- [NAME] -- Week of [DATE]*

:trophy: *What You Crushed This Week:*
- [Account] -- [win: stage move, consumption growth, tool shipped]
- [Account] -- [win]

:bar_chart: *Weekly KPIs:*
- Annualized iMRR: $[X] / $[TARGET] ([%])
- Avg U4->U6: [X] days / <[TARGET]
- UCOs Progressed This Week: [N]

:hammer_and_wrench: *Builder Day -- Recommended Accelerators:*

*[Account 1]:*
- <[URL]|[Accelerator]> -- [why it fits]

*[Account 2]:*
- <[URL]|[Accelerator]> -- [why it fits]

:page_facing_up: *Playbooks (Final Weekly Update):*
- <[DOC_URL_1]|[Account 1]>
- <[DOC_URL_2]|[Account 2]>

${SIGN_OFF}
```

### Friday Digest for Leaders

```
:memo: *Friday Digest -- [LEADER_NAME] -- Week of [DATE]*

:trophy: *Team Wins:*
- [IC Name] @ [Account] -- [win]
- [IC Name] @ [Account] -- [win]

:bar_chart: *Team KPIs This Week:*
- UCOs Progressed: [N]
- New U6 Deliveries: [N]
- Team iMRR Delta: +$[X]

:warning: *Carry-Forward Items:*
- [Item for next week]

${SIGN_OFF}
```

### Friday Wrap for Executive (Christopher Olenik)

Same structure as Monday GM Brief but retrospective -- program wins, metrics delta, risks resolved/escalated.

```
:chart_with_upwards_trend: *Friday Wrap -- Week of [DATE]*

:trophy: *Program Wins:*
- [Top 3-5 wins across all persona groups]

:bar_chart: *Weekly Metrics Delta:*
- UCOs Progressed: [N]
- New U6 Deliveries: [N]
- iMRR Delta: +$[X]

:warning: *Open Risks:*
- [Item, if any]

Let me know what you think. -- Zach
```

---

## Error Handling

| Failure | Detection | Recovery |
|---------|----------|---------|
| SFDC auth expired | `sf org display` returns error | Tell user: run `/salesforce-authentication` |
| Logfood auth expired | `databricks auth token` returns empty | Tell user: run `/databricks-authentication` |
| Google auth expired | Token check returns empty | Tell user: run `/google-auth` |
| Slack MCP unavailable | MCP call returns error | Skip Slack research, note in output |
| No UCOs found for IC | Empty SFDC query result | Send abbreviated message noting empty portfolio |
| Playbook doc not found | Drive search returns empty | Create new doc (don't error) |
| Accelerator catalog empty | Empty query result | Skip accelerator matching, note in output |
| Staging table missing | Notebook 2 read fails | Fail loudly -- notebook 1 must complete first |
| FM API rate limit | 429 response | Retry with exponential backoff, batch recipients |

**Never silently skip a failed step.** Report what failed and continue with available data.

---

## Safe Resource Management

- **Google Docs**: Creates or updates Playbook docs per account. Never deletes docs. Searches by title before creating to avoid duplicates.
- **Slack**: Posts DMs to individual recipients only. Does not post to channels unless explicitly configured.
- **SFDC**: Read-only. Does NOT update UCO fields, stages, or next steps.
- **Staging tables**: Written by notebook 1, read by notebook 2. Overwritten each run (not append).
- **No destructive operations**: This skill only reads data, creates/updates Google Docs, and sends Slack DMs.

---

## Quality Standards

### Slack DMs
- **Concise** -- each bullet is one sentence max
- **Outcome-focused** -- what shipped, not what was discussed
- **Actionable** -- every item has a next step or decision point
- **No fluff** -- skip accounts with zero activity since last update
- **Day-appropriate** -- Monday is strategic, morning is tactical, evening is summary, Friday is celebratory
- **Persona-appropriate** -- ICs get account-level detail, leaders get team aggregates, exec gets program metrics

### Delivery Intelligence Playbooks
- **Living document** -- updated daily, weekly sections preserved as history
- **Account-team-aware** -- includes what AE/SA are doing, not just the IC
- **Source-linked** -- every insight links to a Slack thread, doc, or dashboard
- **Shared when needed** -- same doc for multiple ICs on same account

### Data Freshness
- UCO/ASQ: logfood sfdc_bronze (nightly DLT refresh)
- Consumption: logfood fin_live_gold (nightly DLT refresh)
- Delivery Intelligence / Partner Intel: nightly refresh via logfood job
- Slack/Calendar/Drive/Gmail: live API queries (via notebook 2 or Claude Code)
- Accelerator catalog: nightly refresh via logfood job

---

## Pre-Requisites

- Salesforce auth: `/salesforce-authentication`
- Databricks logfood profile: `/databricks-authentication`
- Google auth: `/google-auth`
- Slack MCP: configured in `~/.claude.json`
- Databricks `slack` external function connection on logfood workspace (for notebook 2 delivery)
- Composed messages saved to `delivery_queue` table for audit/retry

---

## Invocation Examples

```
/dsa-briefing monday
  -> Monday Outlook (59 ICs) + Monday Digest (6 leaders) + Monday GM Brief (1 exec)

/dsa-briefing morning
  -> Morning Prep for 59 ICs (Tue-Fri)

/dsa-briefing evening
  -> Evening Summary (59 ICs) + Evening Digest (6 leaders) — Mon-Thu

/dsa-briefing friday
  -> Friday Wrap (59 ICs + 1 exec) + Friday Digest (6 leaders)

/dsa-briefing
  -> Auto-detects mode based on day/time
```

### Auto-detect logic (when no sub-command given):
```python
from datetime import datetime
now = datetime.now()
day = now.strftime("%A")
hour = now.hour

if day == "Monday":
    mode = "monday"
elif day == "Friday":
    if hour < 13:
        mode = "morning"
    else:
        mode = "friday"
elif day in ("Saturday", "Sunday"):
    print("It's the weekend -- no briefing needed. Enjoy your time off.")
    exit()
elif hour < 12:
    mode = "morning"
else:
    mode = "evening"
```
