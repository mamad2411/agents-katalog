---
name: p2p-daily-update
description: "Path to Production Program Manager daily update for a Slack channel. Posts a parent message with headline summary, then 4 threaded replies: Customer Outcomes, People, Process, AI Tools + Tomorrow's Focus. Pulls live data from logfood gold tables, Slack, and Google Calendar."
user-invocable: true
model: sonnet
---

# Path to Production — Daily Update

Posts a structured daily program update to Slack with a parent message and 4 threaded replies covering Customer Outcomes, People, Process, and AI Tools.

**Usage:**
```
/p2p-daily-update
```

**Announce at start:** "Running Path to Production daily update — pulling from logfood, Slack, Calendar, and Drive."

---

## Configuration

Before running, resolve these values from the user's environment. If a value cannot be resolved, **stop and ask the user** rather than silently skipping.

### Required — resolve dynamically

| Variable | How to resolve | Fallback |
|----------|---------------|----------|
| `SLACK_CHANNEL_ID` | Ask user which Slack channel to post to, or check `~/.vibe/profile.yaml` for `p2p_channel_id` | Ask user |
| `USER_SLACK_ID` | Run `mcp__slack__slack_read_api_call("auth.test", {})` to get current user's ID | Ask user |
| `LOGFOOD_PROFILE` | Check `~/.databrickscfg` for a profile pointing to the logfood workspace | `logfood` |
| `LOGFOOD_WAREHOUSE` | Run `databricks warehouses list --profile <LOGFOOD_PROFILE>` and pick the first SQL warehouse | Ask user |
| `DATA_SCHEMA` | Check `~/.vibe/profile.yaml` for `p2p_schema`, or ask user | Ask user |
| `BU_FILTER` | Check `~/.vibe/profile.yaml` for `p2p_bu`, or ask user (e.g. `CMEG`, `ENT`, etc.) | Ask user |

### Table names (derived from DATA_SCHEMA)

Once `DATA_SCHEMA` is known, the tables are:

| Table | Full name |
|-------|-----------|
| UCO gold | `{DATA_SCHEMA}.u4_u6_path_to_production` |
| ASQ pipeline | `{DATA_SCHEMA}.asq_pipeline` |
| Golden Path | `{DATA_SCHEMA}.golden_path_pipeline` |
| User lookup | `{DATA_SCHEMA}.bronze_user` |
| PS Projects | `{DATA_SCHEMA}.bronze_ps_projects` |

## Dashboard Links

Include in the AI Tools thread (Thread 4) footer if available:

- **Propensity Dashboard**: Check `~/.vibe/profile.yaml` for `p2p_dashboard_url`, otherwise omit

---

## Prerequisites — Authenticate (Parallel)

Run all auth checks in parallel. **If any auth fails, stop and report** which authentication is missing — do not silently skip.

**A. Databricks (logfood):**
```bash
databricks auth token --profile ${LOGFOOD_PROFILE} 2>/dev/null | head -1
```

**B. Google (warm auth):**
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token 2>/dev/null
```

If auth fails for any service, run the appropriate auth skill (`/databricks-authentication`, `/google-auth`) before proceeding.

---

## Step 0 — Duplicate Post Check

Before posting, check if an update was already posted today:

```
mcp__slack__slack_read_api_call("conversations.history", {
  "channel": "${SLACK_CHANNEL_ID}",
  "limit": 10
})
```

Scan the last 10 messages for a parent message matching today's date pattern (e.g., "Daily Update — Mar 7"). If found, **ask the user** whether to post again or skip.

---

## Step 1 — Gather Data (Parallel)

Launch all data queries in parallel using background agents or parallel tool calls. **If any query returns 0 rows, note it** — include a ":warning: No data available" line in the relevant thread section rather than silently omitting.

### 1a. UCO Pipeline Metrics (logfood)

Query the gold UCO table for current pipeline.

**Active pipeline (U4-U5):**
```sql
SELECT
  current_stage,
  COUNT(*) as uco_count,
  SUM(COALESCE(monthly_dbus, 0)) as total_imrr
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE current_stage IN ('U4', 'U5')
GROUP BY 1
ORDER BY 1
```

**FY U6 deliveries** — only U6s that went live on or after the current fiscal year start:
```sql
-- FY start: dynamically derived (Databricks FY begins Feb 1)
-- DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
SELECT
  COUNT(*) as uco_count,
  SUM(COALESCE(monthly_dbus, 0)) as total_imrr
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE current_stage IN ('U6', 'Live')
AND u6_entry_date >= DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
```

**DSA $ coverage (U4-U5 only):**
```sql
SELECT
  current_stage,
  COUNT(*) as total,
  SUM(CASE WHEN dsa_assigned = true THEN 1 ELSE 0 END) as dsa_count,
  SUM(COALESCE(monthly_dbus, 0)) as total_imrr,
  SUM(CASE WHEN dsa_assigned = true THEN COALESCE(monthly_dbus, 0) ELSE 0 END) as dsa_imrr
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE current_stage IN ('U4', 'U5')
GROUP BY 1
```

Report DSA coverage as **% of iMRR $ covered** (not count-based).

### 1b. ASQ Pipeline (logfood)

```sql
SELECT
  status,
  COUNT(*) as cnt,
  SUM(COALESCE(approved_budget, 0)) as total_budget
FROM ${DATA_SCHEMA}.asq_pipeline
WHERE created_date >= DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
GROUP BY status
ORDER BY cnt DESC
```

### 1c. Launch Accelerator / Golden Path (logfood)

```sql
SELECT
  status,
  COUNT(*) as cnt,
  AVG(days_to_complete) as avg_days
FROM ${DATA_SCHEMA}.golden_path_pipeline
GROUP BY status
```

### 1d. DSA Top U4s (logfood)

```sql
SELECT dsa_name, account_name, use_case_name, monthly_dbus, implementation_strategy
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE current_stage = 'U4'
AND dsa_assigned = true AND dsa_name IS NOT NULL
ORDER BY monthly_dbus DESC
LIMIT 15
```

### 1e. DSA AI/Agent UCOs (logfood)

```sql
SELECT dsa_name, account_name, use_case_name, current_stage, monthly_dbus
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE (LOWER(use_case_name) LIKE '%genif%'
    OR LOWER(use_case_name) LIKE '%agent%'
    OR LOWER(use_case_name) LIKE '%gen ai%'
    OR LOWER(use_case_name) LIKE '%llm%'
    OR LOWER(use_case_name) LIKE '%model serving%')
AND dsa_assigned = true
ORDER BY monthly_dbus DESC
LIMIT 15
```

### 1f. SSAs Active on U4s (logfood)

```sql
SELECT DISTINCT a.account_name, a.technical_specialization, u.use_case_name,
       u.current_stage, u.dsa_name, u.monthly_dbus
FROM ${DATA_SCHEMA}.asq_pipeline a
INNER JOIN ${DATA_SCHEMA}.u4_u6_path_to_production u
  ON a.account_name = u.account_name
WHERE a.request_type = 'Specialist SA (SSA) Request'
AND a.status = 'In Progress'
AND u.current_stage = 'U4'
AND a.created_date >= DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
ORDER BY u.monthly_dbus DESC
LIMIT 20
```

### 1g. SSA New This Week (logfood)

```sql
SELECT a.account_name, a.technical_specialization, a.created_date
FROM ${DATA_SCHEMA}.asq_pipeline a
WHERE a.request_type = 'Specialist SA (SSA) Request'
AND a.status = 'In Progress'
AND a.created_date >= DATE_ADD(CURRENT_DATE(), -7)
ORDER BY a.created_date DESC
LIMIT 10
```

### 1h. SSA Heavy Demand (logfood)

```sql
SELECT account_name, COUNT(*) as ssa_count
FROM ${DATA_SCHEMA}.asq_pipeline
WHERE request_type = 'Specialist SA (SSA) Request'
AND status = 'In Progress'
AND created_date >= DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
GROUP BY account_name
ORDER BY ssa_count DESC
LIMIT 10
```

### 1i. PS Projects — What They're Delivering (logfood)

Get active PS projects (non-Training):
```sql
SELECT Name as project_name, project_stage, project_service_type, Region_Level_2__c
FROM ${DATA_SCHEMA}.bronze_ps_projects
WHERE project_service_type NOT IN ('Training')
AND project_stage IN ('In Progress')
ORDER BY project_start_date DESC
LIMIT 25
```

Then cross-reference PS accounts with their UCOs to describe what PS is building:
```sql
SELECT account_name, use_case_name, current_stage, monthly_dbus, implementation_strategy
FROM ${DATA_SCHEMA}.u4_u6_path_to_production
WHERE account_name IN (<PS_ACCOUNT_NAMES>)
AND current_stage IN ('U4','U5')
ORDER BY monthly_dbus DESC
LIMIT 25
```

**IMPORTANT:** Frame PS bullets as the **work being delivered and outcomes** — not commercial constructs (avoid "Success Credits planned", "RSA Silver" — instead say what they're building).

### 1j. Invest-to-Commit Pipeline (logfood)

```sql
SELECT Name, project_stage, project_service_type, project_service_tier, Region_Level_2__c
FROM ${DATA_SCHEMA}.bronze_ps_projects
WHERE project_service_type = 'Invested DSA'
AND project_stage IN ('In Progress','Planned')
ORDER BY project_start_date DESC
```

Cross-reference with UCOs for each invested account to show pipeline value at stake.

### 1k. PAYG-to-Commit Conversions (logfood)

```sql
SELECT account_name, status
FROM ${DATA_SCHEMA}.asq_pipeline
WHERE request_type = 'PAYG to Commit Conversion'
AND created_date >= DATE_TRUNC('year', ADD_MONTHS(CURRENT_DATE(), -1)) + INTERVAL 1 MONTH
ORDER BY account_name
```

Cross-reference with UCOs and Golden Path data to identify COE/AI COE/MVP alignment.

### 1l. AI FDE Activity (logfood)

Check pipeline data for DSA-assigned UCOs where the DSA title/role indicates AI FDE:
- Look for users with "AI" or "FDE" in their role — these are separate from the DSA org
- Include them in a dedicated section, not mixed with DSA metrics

### 1m. DSA Org Validation

Validate DSA roster from the UCO table — cross-reference `dsa_name` values against the user's known org structure. The user should provide their DSA manager names in `~/.vibe/profile.yaml` under `p2p_dsa_managers`. If not configured, include all DSAs found in the data.

### 1n. Key Account Activity (Slack — last 48h)

Search Slack for recent activity on accounts with active U4 UCOs. Run as background agents:

```
mcp__slack__slack_read_api_call("search.messages", {
  "query": "<ACCOUNT_NAME> after:yesterday",
  "count": 10
})
```

Extract: decisions made, blockers raised, meetings held, outcomes delivered.

### 1o. Calendar — Last 24h + Next 48h

```bash
ACCESS_TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token 2>/dev/null)
YESTERDAY=$(python3 -c "from datetime import datetime, timedelta; print((datetime.utcnow()-timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z'))")
DAY_AFTER=$(python3 -c "from datetime import datetime, timedelta; print((datetime.utcnow()+timedelta(days=2)).strftime('%Y-%m-%dT23:59:59Z'))")
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=${YESTERDAY}&timeMax=${DAY_AFTER}&singleEvents=true&orderBy=startTime"
```

---

## Step 2 — Synthesize & Post

Once all data is gathered, compose the update as 1 parent message + 4 threaded replies. **Do not duplicate content across threads.**

### 2a. Parent Message

```
mcp__slack__slack_write_api_call("chat.postMessage", {
  "channel": "${SLACK_CHANNEL_ID}",
  "text": ":databricks: *Path to Production — Daily Update — <DATE>*\n\n> :mega: *Today:* <2-3 key headlines — pipeline numbers, top account activity, invest-to-commit highlights>\n\nFull update in thread :thread:",
  "unfurl_links": false
})
```

**Capture the returned `ts` value** — use as `thread_ts` for all 4 replies.

The headline should highlight: total pipeline numbers, top strategic account activity, invest-to-commit momentum (2-3 items max).

### 2b. Thread 1 — Customer Outcomes

```
:chart_with_upwards_trend: *Customer Outcomes*

*Active Pipeline: [N] U4-U5 UCOs | $[X] iMRR*
- [N] U4 ($[X]) | [N] U5 ($[X])
- FY27 U6 Deliveries: [N] UCOs live in production ($[X] iMRR)

*Launch Accelerator:* [N] workshops — [X] Complete, avg [N] days to MVP (target: 60)

*Invest-to-Commit Pipeline:* [N] Invested DSA projects active:
- [Account] — Invested DSA [Tier] ([Vertical]) + [N] UCOs ($[X] iMRR)
- [Account] — [context on DSA commit candidacy, Golden Path MVPs, renewal status]
... (only accounts with active investments)
```

### 2c. Thread 2 — People

```
:busts_in_silhouette: *People*

*PS Delivery:*
- *[Account]* — [what PS is building/delivering], [UCO linkage + iMRR]
- *[Account]* — [what PS is building/delivering], [UCO linkage + iMRR]
... (frame as outcomes/work delivered, not commercial constructs)

*SSAs:*
- Active on U4s: [Account] [UCO name] ($[X]), [Account] [UCO name] ($[X]), ...
- New this week: [Account], [Account], ...
- Heavy demand: [Account] ([N] SSAs), [Account] ([N]), ...

*DSAs:*
- *DSA $ Coverage: $[X] of $[Y] U4-U5 iMRR = [P]%* ([A] of [B] U4 | [C] of [D] U5)
- *Top U4s in flight:*
  - [DSA Name] — [Account] [UCO name] ($[X], [implementation strategy])
  - ... (top 5 by iMRR)
- *AI/Agent UCOs driven by DSAs:*
  - [DSA Name] — [Account] [UCO name] ($[X], [stage])
  - ... (Genify, Agent, Gen AI, LLM, Model Serving use cases only)

*AI FDE:*
- [Name] — $[X] iMRR, [N] active UCO(s)
```

### 2d. Thread 3 — Process

```
:gear: *Process*

*U4 GTM Initiatives:*
1. Run AI Programs at Target Accounts
2. Invite EMs to UCO Reviews — "How to Get to Live"
3. Assign DSAs to U4s for delivery ownership and "MVP Engineering" approach

*Program Momentum:*
- [N] UCOs delivered to production in FY27 — $[X] iMRR live
- [N] Invested DSA projects active — [top accounts with tier]; [commit candidates with Golden Path/COE alignment]
- DSA U4 coverage at [X]% vs [Y]% U5 — [specific high-iMRR U4s that need DSA assignment]

*ASQ Pipeline (FY27):*
- [N] total ASQs
- Active: [X] In Progress | [Y] Approved | [Z] New
- Completed: [N] delivered
```

### 2e. Thread 4 — AI Tools + Tomorrow's Focus

```
:robot_face: *AI Tools*

*:rocket: Getting Started — Run These Commands:*
1. Update vibe: `vibe update`
2. Open an AI agent session: `vibe agent`
3. Browse available skills: `vibe skills`

*Key Skills:*
- `/salesforce-actions` — query/update UCOs, accounts, ASQs directly
- `/competitive-analysis` — positioning vs Snowflake, Fabric, etc.
- `/uco-consumption-analysis` — validate UCO stages against consumption data
- `/databricks-sizing` — cost estimates and sizing for workloads

*Shipped:*
- [List recently shipped tools/features with brief description]

*In Progress:*
- [Active tool/project being tested with status]

:dart: *Tomorrow's Focus*
1. *[Account/Activity]* — [strategic context and why]
2. *[Account/Activity]* — [strategic context and why]
3. *[Account/Activity]* — [strategic context and why]

:link: *Dashboards*
- [Include dashboard URL from config if available]
```

---

## Quality Standards

### Audience
- **Sales leadership and ELT** — focus on outcomes, pipeline impact, and strategic account activity
- Do NOT include internal technical details (data pipeline fixes, auth issues, code changes)
- If a data source query returns 0 rows, include a brief ":warning: [Section] data unavailable" note so the reader knows the section was checked but empty

### Content Rules
- **No duplicate content across threads** — each data point appears in exactly one thread
- **Outcome-focused** — what shipped, progressed, or is at risk — not what was discussed
- **Concise** — each bullet is one sentence max
- **Quantified** — include iMRR, UCO counts, coverage percentages
- **PS framed as delivery** — describe the work and outcomes, not commercial constructs (no "GSS Bronze planned" or "Success Credits Master" — say what they're building)
- **SSA scoped to U4s** — only highlight SSA engagements tied to active U4 UCOs
- **DSA org validated** — only include DSAs validated against the configured manager hierarchy
- **AI FDE separated** — AI FDEs are a separate org from DSAs; report them in their own section

### Data Freshness
- UCO/ASQ/Golden Path counts come from **logfood gold tables** (refreshed nightly by DLT pipeline)
- PS projects from **bronze_ps_projects** (logfood)
- Key account activity from **live Slack search** (last 48h)
- Calendar data from **Google Calendar API** (last 24h + next 48h)

### Thread Structure
- Always **exactly 4 thread replies** — Customer Outcomes, People, Process, AI Tools
- Parent message is a **brief headline** with `:thread:` pointer
- @-mention the user's Slack ID in parent message

---

## Error Handling

- **Auth failure**: Stop and report which service needs authentication. Do not post partial updates.
- **Empty query results**: Include the section with a ":warning: No data available" note rather than silently omitting.
- **Slack post failure**: Report the error. Do not retry automatically — the user may need to check channel permissions.
- **Duplicate post detected**: Ask the user before posting again on the same day.

---

## Pre-Requisites

- Databricks: logfood profile in `~/.databrickscfg` with access to the data schema
- Google auth: `gcloud` authenticated for Calendar API
- Slack MCP: configured in `~/.claude.json`
- Logfood gold tables: refreshed by nightly DLT pipelines
- Optional: `~/.vibe/profile.yaml` with `p2p_channel_id`, `p2p_schema`, `p2p_bu`, `p2p_dashboard_url`, `p2p_dsa_managers`
