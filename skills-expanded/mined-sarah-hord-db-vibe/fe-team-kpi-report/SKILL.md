---
name: fe-team-kpi-report
description: Generate SA team KPI scorecard and workload summary report for FE managers. Use when asked for SA team performance, team KPI report, team workload summary, FE team metrics, SA scorecard, manager team overview, or SA pipeline and consumption review.
---

# FE Team KPI Report

**Purpose:** Produce a complete KPI scorecard for an SA manager's direct-report team, covering consumption (T3M DBU$, MoM growth), pipeline (weighted by stage and FY quarter), velocity (U2 avg days, U3 avg days), support activity (ASQ QTD ownership, SSA + STS filed FY YTD), and QTD leaderboard. Delivered as a formatted Slack DM.

**Execution order:** Phase 0 (identity + team) → Phase 1 (parallel data collection) → Phase 2 (analysis + formatting) → Phase 3 (Slack output).

---

## Pre-execution: Manager identification

**Who is this skill for?** The FE manager running the skill. All data and output are scoped to their direct-report SA team.

1. **Load vibe profile.** Read `~/.vibe/profile` (or use `vibe-profile` skill). Set:
   - `[Manager Email]` = `user.email`
   - `[Manager Slack]` = `user.slack_handle` (for Slack DM delivery)
   - If no profile or missing email, ask: *"Provide your Databricks manager email to identify your team."*

2. **Auth.** Load `databricks-authentication` (logfood profile) before any queries. Verify the connection before proceeding.

3. **Slack delivery.** Send the final output as a DM to `[Manager Slack]`. If `slack_handle` is not in the vibe profile, ask for it or print the output to console and note: "Add `slack_handle` to vibe profile for automatic DM delivery."

---

## Phase 0: Setup — Identity and Team

**Skills to load:** `databricks-authentication`, `logfood-querier`, `databricks-warehouse-selector`.

**Fiscal context:** Compute dynamically from today's date using the shared fiscal calendar utility — never hardcode quarter or FY dates.

> **Shared resource:** `../../resources/fiscal_calendar.py` (single source of truth for all fe-manager skills). Run directly for JSON output or import the function in Python.

```python
import subprocess, json

ctx = json.loads(subprocess.run(
    ["python3", "../../resources/fiscal_calendar.py"],
    capture_output=True, text=True
).stdout)
# OR absolute path import:
# import sys; sys.path.insert(0, os.path.expanduser("~/.vibe/marketplace/plugins/fe-manager/resources"))
# from fiscal_calendar import databricks_fiscal_context; ctx = databricks_fiscal_context()

# Returns: fiscal_year (int), fiscal_quarter (int),
#          fiscal_year_quarter_str (e.g. "FY'27 Q1"), quarter_start (YYYY-MM-DD),
#          quarter_end, prior_fiscal_year, prior_fiscal_quarter,
#          next_fiscal_year, next_fiscal_quarter.

# fy_start_date (FY start = Feb 1) is not returned directly — compute from fiscal_year:
# fiscal_year is 4-digit (e.g. 2027 for FY27); FY starts Feb of the prior calendar year.
# FY27 starts Feb 2026 → fy_start_year = fiscal_year - 1  (2027 - 1 = 2026)
fy_start_date = f"{ctx['fiscal_year'] - 1}-02-01"
ctx["fy_start_date"] = fy_start_date
```

Use `ctx["quarter_start"]`, `ctx["fy_start_date"]`, and `ctx["fiscal_year"]` in all queries and output. NEVER paste a literal date string — always substitute from `ctx`.

Databricks FY starts **February 1**. Example: on Mar 3 2026, `ctx` yields `fiscal_year=2027`, `fiscal_quarter=1`, `quarter_start="2026-02-01"`, `fy_start_date="2026-02-01"`.

**1. Identify the calling manager (from vibe profile or SFDC):**
```sql
SELECT Id, Name, Email, FEL2Team__c, FEL2Role__c
FROM main.sfdc_bronze.user
WHERE Email = '[manager_email]'
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
```

**2. Load direct reports (SA team):**
```sql
SELECT Id AS sa_id, Name AS sa_name, Email AS sa_email, FEL2Role__c, User_Sub_Region__c
FROM main.sfdc_bronze.user
WHERE ManagerId = '[manager_sfdc_id]'
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  AND IsActive = true
ORDER BY Name
```
Persist `sa_ids` list and name→short-name map for all downstream queries.

---

## Phase 1: Data Collection (run all queries in parallel)

Use Logfood warehouse (profile `logfood`). Use `databricks-warehouse-selector` to get a running warehouse ID. Run queries 1a–1i concurrently via `ThreadPoolExecutor`.

> **Attribution policy (Option B — full credit + deduplicated team totals):**
> When multiple SAs from the team share the same account, **each SA receives full credit** for that account's consumption and pipeline — this reflects that both SAs are actively working it and is more motivating for individuals.
> However, to prevent double-counting at the org level, **team totals** (the TEAM row in scorecards and pipeline tables, and all team-level summary bullets) must be computed from **deduplicated account/UCO sets**, not by summing SA-level rows.
> Queries 1a and 1b include a second "team total" CTE/sub-query for this purpose. Always use those for TEAM row values.

### 1a. T3M DBU and MoM Growth per SA

T3M window: 3 completed calendar months back from today. MoM = last completed month vs prior month.

> **Schema note:** Table `main.gtm_gold.account_consumption_monthly` uses column `dbu_dollars` (not `total_arr_usd`) and `calendar_year_month` as a string key `'YYYY-MM'` (not a date column `calendar_month`).

**Part A — per-SA (full credit, shared accounts counted for each SA):**
```sql
WITH sa_accounts AS (
  SELECT DISTINCT atm.UserId, atm.AccountId, u.Name AS sa_name
  FROM main.sfdc_bronze.accountteammember atm
  JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  WHERE atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
    AND atm.IsDeleted = false
    AND atm.TeamMemberRole LIKE '%Solution Architect%'
    AND atm.UserId IN (<sa_ids>)
),
monthly AS (
  SELECT sa.sa_name,
    acm.calendar_year_month,
    SUM(acm.dbu_dollars) AS dbu
  FROM main.gtm_gold.account_consumption_monthly acm
  JOIN sa_accounts sa ON acm.account_id = sa.AccountId
  WHERE acm.calendar_year_month >= DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -3), 'yyyy-MM')
    AND acm.calendar_year_month <  DATE_FORMAT(DATE_TRUNC('month', CURRENT_DATE()), 'yyyy-MM')
  GROUP BY sa.sa_name, acm.calendar_year_month
)
SELECT
  sa_name,
  SUM(dbu) AS t3m_dbu,
  SUM(CASE WHEN calendar_year_month = DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -1), 'yyyy-MM') THEN dbu ELSE 0 END) AS last_month_dbu,
  SUM(CASE WHEN calendar_year_month = DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -2), 'yyyy-MM') THEN dbu ELSE 0 END) AS prior_month_dbu,
  SUM(CASE WHEN calendar_year_month = DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -3), 'yyyy-MM') THEN dbu ELSE 0 END) AS oldest_month_dbu
FROM monthly
GROUP BY sa_name
```
Compute `mom_pct = ROUND((last_month_dbu - prior_month_dbu)*100.0 / NULLIF(prior_month_dbu, 0), 1)`.

**Part B — team total (deduplicated: each account counted once regardless of how many SAs share it):**
```sql
WITH team_account_ids AS (
  SELECT DISTINCT atm.AccountId
  FROM main.sfdc_bronze.accountteammember atm
  WHERE atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
    AND atm.IsDeleted = false
    AND atm.TeamMemberRole LIKE '%Solution Architect%'
    AND atm.UserId IN (<sa_ids>)
)
SELECT
  SUM(acm.dbu_dollars) AS team_t3m_dbu,
  SUM(CASE WHEN acm.calendar_year_month = DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -1), 'yyyy-MM') THEN acm.dbu_dollars ELSE 0 END) AS team_last_month_dbu,
  SUM(CASE WHEN acm.calendar_year_month = DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -2), 'yyyy-MM') THEN acm.dbu_dollars ELSE 0 END) AS team_prior_month_dbu
FROM main.gtm_gold.account_consumption_monthly acm
WHERE acm.account_id IN (SELECT AccountId FROM team_account_ids)
  AND acm.calendar_year_month >= DATE_FORMAT(ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE()), -3), 'yyyy-MM')
  AND acm.calendar_year_month <  DATE_FORMAT(DATE_TRUNC('month', CURRENT_DATE()), 'yyyy-MM')
```
Use `team_t3m_dbu`, `team_last_month_dbu`, `team_prior_month_dbu` **only** for the TEAM row in the scorecard and team-level summary bullets. Never use the sum of per-SA rows for the team total.

### 1b. Weighted Pipeline by Stage and FY Quarter per SA

Standard stage weights: **U2=20%, U3=40%, U4=60%, U5=80%**. `Weight__c` is often NULL — always apply these defaults.

Go-live date field: `COALESCE(Full_Production_Date__c, Forecasted_Date__c, Go_Live_Date__c)`.

FY quarter assignment — correct offsets (see Common Mistakes for the off-by-one bug):
```sql
-- fiscal quarter from a date column `d`:
CASE
  WHEN MONTH(d) IN (2,3,4)  THEN CONCAT('FY', YEAR(d) - 1999, ' Q1')
  WHEN MONTH(d) IN (5,6,7)  THEN CONCAT('FY', YEAR(d) - 1999, ' Q2')
  WHEN MONTH(d) IN (8,9,10) THEN CONCAT('FY', YEAR(d) - 1999, ' Q3')
  WHEN MONTH(d) IN (11,12)  THEN CONCAT('FY', YEAR(d) - 1999, ' Q4')  -- same offset as Q1–Q3
  WHEN MONTH(d) = 1         THEN CONCAT('FY', YEAR(d) - 2000, ' Q4')  -- Jan belongs to prior FY
END
-- FY27 Q4 = Nov 2026 – Jan 2027.
-- Months 11/12: offset -1999. Nov 2026 → 2026-1999=27 → FY27 Q4 ✓
-- Month 1: offset -2000.   Jan 2027 → 2027-2000=27 → FY27 Q4 ✓
```

**Part A — per-SA (full credit, UCOs on shared accounts counted for each SA):**
```sql
WITH sa_accounts AS (
  SELECT DISTINCT atm.UserId, atm.AccountId
  FROM main.sfdc_bronze.accountteammember atm
  WHERE atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
    AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
    AND atm.UserId IN (<sa_ids>)
),
pipeline AS (
  SELECT u.Name AS sa_name,
    CASE uc.Stages__c
      WHEN 'U2' THEN 0.20 WHEN 'U3' THEN 0.40
      WHEN 'U4' THEN 0.60 WHEN 'U5' THEN 0.80 ELSE 0 END AS weight,
    uc.QtrlyPipeGenDollarDBU__c AS pipe_dbu,
    CASE
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (2,3,4)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q1')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (5,6,7)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q2')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (8,9,10)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q3')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (11,12)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q4')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) = 1
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-2000,' Q4')
    END AS fq
  FROM main.sfdc_bronze.usecase__c uc
  JOIN sa_accounts sa ON uc.Account__c = sa.AccountId
  JOIN main.sfdc_bronze.user u ON sa.UserId = u.Id
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  WHERE uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND uc.IsDeleted = false AND uc.Stages__c IN ('U2','U3','U4','U5')
    AND uc.QtrlyPipeGenDollarDBU__c IS NOT NULL AND uc.QtrlyPipeGenDollarDBU__c > 0
)
SELECT sa_name, fq,
  ROUND(SUM(pipe_dbu * weight), 0) AS weighted_pipe_dbu,
  COUNT(*) AS uco_count
FROM pipeline WHERE fq IS NOT NULL
GROUP BY sa_name, fq ORDER BY sa_name, fq
```

**Part B — team pipeline total (deduplicated: each UCO counted once regardless of how many SAs share its account):**
```sql
WITH team_account_ids AS (
  SELECT DISTINCT atm.AccountId
  FROM main.sfdc_bronze.accountteammember atm
  WHERE atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
    AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
    AND atm.UserId IN (<sa_ids>)
),
deduped_pipeline AS (
  SELECT DISTINCT uc.Id AS uco_id,
    uc.QtrlyPipeGenDollarDBU__c AS pipe_dbu,
    CASE uc.Stages__c
      WHEN 'U2' THEN 0.20 WHEN 'U3' THEN 0.40
      WHEN 'U4' THEN 0.60 WHEN 'U5' THEN 0.80 ELSE 0 END AS weight,
    CASE
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (2,3,4)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q1')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (5,6,7)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q2')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (8,9,10)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q3')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) IN (11,12)
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-1999,' Q4')
      WHEN MONTH(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c)) = 1
        THEN CONCAT('FY',YEAR(COALESCE(uc.Full_Production_Date__c,uc.Forecasted_Date__c,uc.Go_Live_Date__c))-2000,' Q4')
    END AS fq
  FROM main.sfdc_bronze.usecase__c uc
  WHERE uc.Account__c IN (SELECT AccountId FROM team_account_ids)
    AND uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND uc.IsDeleted = false AND uc.Stages__c IN ('U2','U3','U4','U5')
    AND uc.QtrlyPipeGenDollarDBU__c IS NOT NULL AND uc.QtrlyPipeGenDollarDBU__c > 0
)
SELECT fq, ROUND(SUM(pipe_dbu * weight), 0) AS team_weighted_pipe_dbu
FROM deduped_pipeline WHERE fq IS NOT NULL
GROUP BY fq ORDER BY fq
```
Use the results of Part B **only** for the TEAM totals row in the pipeline table and the team pipeline summary bullet. Never use the sum of per-SA rows for the team total.

### 1c. U3 Age (Average Days in U3 per SA)

U3 is often the pipeline bottleneck — flag SAs with average U3 age >90 days.

```sql
SELECT u.Name AS sa_name,
  ROUND(AVG(uvd.days_in_evaluating), 0) AS avg_u3_age_days,
  COUNT(*) AS u3_count
FROM main.gtm_gold.use_case_velocity_details uvd
JOIN main.sfdc_bronze.usecase__c uc ON uvd.use_case_id = uc.Id
  AND uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
  AND uc.Stages__c = 'U3' AND uc.IsDeleted = false
JOIN main.sfdc_bronze.accountteammember atm ON uc.Account__c = atm.AccountId
  AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
  AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
  AND atm.UserId IN (<sa_ids>)
JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
GROUP BY u.Name
```
Fallback if `use_case_velocity_details` times out: `ROUND(AVG(DATEDIFF(CURRENT_DATE(), uc.Last_Stage_Modified_Date__c)), 0)` on `usecase__c WHERE Stages__c = 'U3'`.

### 1d. ASQ Requests QTD (Scaled SAs Support Request — SA as OWNER)

**Semantic:** ASQ ✓ means the SA **owns** (picked up) a Scaled SA request from an AE to help on a hunter account. Filter by `OwnerId IN (<sa_ids>)`.

**QTD definition — CRITICAL:** Count ASQs that were **active during the current quarter** — this means either:
- `CreatedDate >= ctx["quarter_start"]` (newly opened this quarter), OR
- `LastModifiedDate >= ctx["quarter_start"]` (existing request still being progressed/completed this quarter)

Using only `CreatedDate >= quarter_start` will miss carryover requests that are actively worked (In Progress or Completed) within the quarter. Always use the combined OR filter below. Substitute `ctx["quarter_start"]` — never a hardcoded date string.

```sql
SELECT u.Name AS sa_name, COUNT(DISTINCT ar.Id) AS asq_qtd
FROM main.sfdc_bronze.approvalrequest__c ar
JOIN main.sfdc_bronze.user u ON ar.OwnerId = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
WHERE ar.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.approvalrequest__c)
  AND ar.IsDeleted = false
  AND ar.OwnerId IN (<sa_ids>)
  AND ar.Request_Type__c = 'Scaled SAs Support Request'
  AND (
    ar.CreatedDate >= '[quarter_start]'
    OR ar.LastModifiedDate >= '[quarter_start]'
  )
GROUP BY u.Name
```

### 1e. SSA Requests Filed FY YTD (Specialist SA Request — SA as CREATOR)

**Semantic:** SSA requests are filed **BY** the SA (`CreatedById`) to request specialist help. The specialist who picks it up is the `OwnerId` — that is a *different* SA. Always filter by `CreatedById`, never `OwnerId`, for this metric.

Window: current FY YTD — use `ctx["fy_start_date"]` from `get_fiscal_context()`, not a hardcoded date.

```sql
SELECT u.Name AS sa_name, COUNT(DISTINCT ar.Id) AS ssa_ytd
FROM main.sfdc_bronze.approvalrequest__c ar
JOIN main.sfdc_bronze.user u ON ar.CreatedById = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
WHERE ar.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.approvalrequest__c)
  AND ar.IsDeleted = false
  AND ar.CreatedById IN (<sa_ids>)
  AND ar.Request_Type__c = 'Specialist SA (SSA) Request'
  AND ar.CreatedDate >= '[fy_start_date]'
GROUP BY u.Name
```

### 1f. STS Requests Filed FY YTD (Shared Technical Services — SA as CREATOR)

**Semantic:** STS requests are filed **BY** the SA (`CreatedById`) to bring in a Scaled Tech Specialist (e.g. for a technical deep-dive or competitive POC assist). Same attribution logic as SSA — filter by `CreatedById`, never `OwnerId`.

> **Verified `Request_Type__c` for Logfood org:** `'Shared Technical Services'` — confirmed via discovery query on 2026-03-03. Other orgs may use a different string; re-verify if deploying elsewhere.

Window: current FY YTD — use `ctx["fy_start_date"]`, never a hardcoded date.

```sql
SELECT u.Name AS sa_name, COUNT(DISTINCT ar.Id) AS sts_ytd
FROM main.sfdc_bronze.approvalrequest__c ar
JOIN main.sfdc_bronze.user u ON ar.CreatedById = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
WHERE ar.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.approvalrequest__c)
  AND ar.IsDeleted = false
  AND ar.CreatedById IN (<sa_ids>)
  AND ar.Request_Type__c = 'Shared Technical Services'
  AND ar.CreatedDate >= '[fy_start_date]'
GROUP BY u.Name
```

### 1g. UCO Stage Progressions QTD

Compare quarter-start snapshot vs most recent snapshot. Quarter start = `ctx["quarter_start"]` from `get_fiscal_context()` — never hardcoded.

```sql
WITH stage_order AS (
  SELECT 'U1' AS stage, 1 AS ord UNION ALL SELECT 'U2', 2 UNION ALL
  SELECT 'U3', 3 UNION ALL SELECT 'U4', 4 UNION ALL SELECT 'U5', 5 UNION ALL
  SELECT 'U6', 6 UNION ALL SELECT 'Live', 6
),
snap_start AS (
  SELECT Id, Stages__c, Account__c
  FROM main.sfdc_bronze.usecase__c
  WHERE processDate = '[quarter_start]' AND IsDeleted = false
),
snap_today AS (
  SELECT Id, Stages__c, Account__c
  FROM main.sfdc_bronze.usecase__c
  WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND IsDeleted = false
),
progressions AS (
  SELECT t.Id, t.Account__c
  FROM snap_today t JOIN snap_start f ON t.Id = f.Id
  JOIN stage_order so_new ON t.Stages__c = so_new.stage
  JOIN stage_order so_old ON f.Stages__c = so_old.stage
  WHERE so_new.ord > so_old.ord
)
SELECT u.Name AS sa_name, COUNT(DISTINCT p.Id) AS progressed_ucos_qtd
FROM progressions p
JOIN main.sfdc_bronze.accountteammember atm ON p.Account__c = atm.AccountId
  AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
  AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
  AND atm.UserId IN (<sa_ids>)
JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
GROUP BY u.Name ORDER BY progressed_ucos_qtd DESC
```
If `[quarter_start]` has no snapshot, use the first `processDate >= [quarter_start]` available in `usecase__c`.

### 1h. U2 Velocity per SA (avg days in U2 stage)

```sql
SELECT u.Name AS sa_name,
  ROUND(AVG(uvd.days_in_scoping), 0) AS avg_u2_age_days
FROM main.gtm_gold.use_case_velocity_details uvd
JOIN main.sfdc_bronze.usecase__c uc ON uvd.use_case_id = uc.Id
  AND uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
  AND uc.IsDeleted = false
JOIN main.sfdc_bronze.accountteammember atm ON uc.Account__c = atm.AccountId
  AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
  AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
  AND atm.UserId IN (<sa_ids>)
JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
GROUP BY u.Name
```

### 1i. Top Progressed UCOs by MRR $DBUs (U1/U2/U3 only, QTD)

Returns the top 3 U1/U2/U3 use cases (by current MRR $DBUs) that moved forward at least one stage QTD.

```sql
WITH stage_order AS (
  SELECT 'U1' AS stage, 1 AS ord UNION ALL SELECT 'U2', 2 UNION ALL
  SELECT 'U3', 3 UNION ALL SELECT 'U4', 4 UNION ALL SELECT 'U5', 5 UNION ALL
  SELECT 'U6', 6 UNION ALL SELECT 'Live', 6
),
snap_start AS (
  SELECT Id, Stages__c
  FROM main.sfdc_bronze.usecase__c
  WHERE processDate = '[quarter_start]' AND IsDeleted = false
),
snap_today AS (
  SELECT Id, Stages__c, Account__c, Name AS uco_name,
    COALESCE(MonthlyTotalDollarDBUs__c, QtrlyPipeGenDollarDBU__c / 3) AS mrr_dbu
  FROM main.sfdc_bronze.usecase__c
  WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND IsDeleted = false AND Stages__c IN ('U1','U2','U3')
),
progressed AS (
  SELECT t.Id, t.uco_name, t.Account__c, t.Stages__c AS cur_stage, t.mrr_dbu
  FROM snap_today t JOIN snap_start f ON t.Id = f.Id
  JOIN stage_order so_new ON t.Stages__c = so_new.stage
  JOIN stage_order so_old ON f.Stages__c = so_old.stage
  WHERE so_new.ord > so_old.ord
)
-- ROW_NUMBER ensures each UCO appears once even if multiple team SAs share its account.
-- The SA shown is the first alphabetically among those on the account.
SELECT uco_name, account_name, cur_stage, mrr_dbu, sa_name
FROM (
  SELECT p.uco_name, a.Name AS account_name, p.cur_stage,
    ROUND(p.mrr_dbu, 0) AS mrr_dbu, u.Name AS sa_name,
    ROW_NUMBER() OVER (PARTITION BY p.Id ORDER BY u.Name) AS rn
  FROM progressed p
  JOIN main.sfdc_bronze.account a ON p.Account__c = a.Id
    AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
  JOIN main.sfdc_bronze.accountteammember atm ON p.Account__c = atm.AccountId
    AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
    AND atm.IsDeleted = false AND atm.TeamMemberRole LIKE '%Solution Architect%'
    AND atm.UserId IN (<sa_ids>)
  JOIN main.sfdc_bronze.user u ON atm.UserId = u.Id
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
) WHERE rn = 1
ORDER BY mrr_dbu DESC NULLS LAST
LIMIT 3
```
If `MonthlyTotalDollarDBUs__c` is NULL, use `QtrlyPipeGenDollarDBU__c / 3` as MRR proxy (already in COALESCE above).

---

## Phase 2: Analysis and Formatting

### 2a. Build Scorecard Table

**Columns:** `SA | T3M | MoM | U2d | U3 | ASQ | SSA | STS`

**SA name format:** Always use the person's **first name** (e.g. `Anton`, `Chi-Ju`, `Oleksandr`), never the `F. Lastname` initials pattern. If the first name alone fits in ≤13 chars, use it as-is; if longer, truncate to 13. This makes the table friendlier and easier to read at a glance.

- `T3M` = `$XXXk` (T3M DBU$) or `$X.XM`
- `MoM` = `+X.X%▲` (growing) / `-X.X%▼` (declining) / `±0%` (flat). Threshold: ±2% = flat. Use `▲`/`▼` unicode arrows (monospace-safe, single-width)
- `U2d` = avg days in U2 stage (from 1g). Format: `XXd` right-aligned. `n/a` if no U2 UCOs.
- `U3` = avg days in U3 stage (from 1c). Format: `XXd ~` (60–90d watch) / `XXd !` (>90d stall) / `XXd `. `n/a` if no U3 UCOs.
- `ASQ` = count of QTD owned ASQ requests. `N✓` if ≥1, `–` if 0. QTD = since `ctx["quarter_start"]` (derived dynamically).
- `SSA` = count of Specialist SA requests **filed** by the SA FY YTD (from 1e). `N✓` if ≥1, `–` if 0.
- `STS` = count of Scaled Tech Specialist requests **filed** by the SA FY YTD (from 1i). `N✓` if ≥1, `–` if 0.

> **Wtd$ removed** — it's already visible in the pipeline table below; avoid duplication.

**Legend** (in a `context` block *outside* the code block — not inside it):
```
▲▼ MoM direction  ·  U2d avg days in U2  ·  U3: ! stall >90d  ~ watch >60d
ASQ ✓ = Scaled SA request owned QTD  ·  SSA/STS ✓ = specialist request filed FY YTD
```

**Separator:** Use `─` (U+2500 box-drawing) instead of `-` for table dividers — cleaner in Slack.

**Color signal context block below table:**
- 🟢 `Growing: [names with MoM >+5%]`
- 🔴 `Declining: [names with MoM <-5%]`
- ⚡ `Velocity (U2→U3): [top 2 fastest names]`
- ⚠️ `U3 stalls: [names with U3 >90d]`

### 2b. Build Quarterly Pipeline Table

Columns: `SA | Q1 | Q2 | Q3 | Q4 | Total` (all in `$XXk` format).

**Add a TEAM totals row** at the bottom, preceded by a separator line:
```
─────────────────────────────────────────────────────
TEAM            $396K   $347K   $234K   $315K   $1.4M
(FY27 Q1=Feb–Apr  Q2=May–Jul  Q3=Aug–Oct  Q4=Nov–Jan)
```

> **TEAM row MUST use the deduplicated totals from query 1b Part B** — never sum the SA-level rows, as shared accounts would be double-counted. The SA rows above it are intentionally higher in aggregate because each SA gets full credit.

Footer context note: highlight heaviest quarter, flag any SA with $0 in Q4.

### 2c. Build Leaderboard (Monospace Block)

**Four sections (growth, velocity, progressions, top UCOs), each limited to top 3, with underlined headers:**

```
  📈 Consumption Growth (MoM  [month] vs [month])
  ──────────────────────────────────────────────
    1. [SA Name]   +X.X%
    2. [SA Name]   +X.X%
    3. [SA Name]   +X.X%
    (only SAs with positive growth; skip if none)

  ⚡ Pipeline Velocity (U2→U3, avg days)
  ─────────────────────────────────────
    1. [SA Name]   Xd
    2. [SA Name]   Xd
    3. [SA Name]   Xd

  🏆 UCO Stage Progressions QTD (since [quarter_start])
  ─────────────────────────────────────────────────────
    1. [SA Name]   X UCOs
    2. [SA Name]   X UCOs
    3. [SA Name]   X UCOs

  💰 Highest-Value Progressed UCOs (QTD)
  ─────────────────────────────────────
    1. [UCO Name truncated 20c]  [Stage]  $XXk — [SA Name]
    2. ...
    3. ...

```

Rules:
- **Consumption Growth:** positive MoM only. If 0 SAs are positive, write `(no positive growth this period)`.
- **All sections:** top 3 only (not top 5 or 6).
- Section headers use underline `─` matching header width.
- Keep each line ≤87 chars — truncate UCO names to ~20 chars.

### 2d. Team-Level Summary (mrkdwn bullets)

> Use **deduplicated team totals** (from query 1a Part B and 1b Part B) for the T3M and pipeline figures in the bullets below — not the sum of SA rows.

```
• *T3M DBU:* $X.XM — top earner [SA] ($XXXk). Growing (MoM >+5%): [names]. Declining: [names].
• *Active pipeline:* $X.XM weighted (FY[YY]) — [SA] leads ($XXXk). [Q_heaviest] is heaviest at $XXXk.
• *U3 bottleneck:* avg team U3 age Xd. Stalls (>90d): [names].
• *Pipeline velocity (U2→U3):* fastest [SA] at Xd; slowest [SA] at Xd.
• *Support filed FY[YY] YTD (SSA + STS):* X SSA, X STS — top filers: [SA (SSA:N STS:N), ...].
• *UCO progressions QTD:* X total — [SA] leads with X UCOs.
```

**Do not include a T3M breakdown for SSA or STS** — FY YTD totals only are sufficient.

---

## Phase 3: Slack Output

**Delivery:** DM to manager's Slack handle (from vibe profile) or channel if specified. Look up user ID via `slack_read_api_call` `users.lookupByEmail` if only email is known.

**Message structure (Slack Block Kit):**

```
[Header]  [Manager Name]'s SA Team | KPI Summary
[Context] Manager: [Name]  ·  [Date]  ·  N SAs  ·  T3M: [Month1] – [Month3]

[Divider]
[Section] *:clipboard: Team Scorecard*
[Context] <column description line>
[Code block] <monospace table from 2a>
[Context] <legend line>
[Context] 🟢 Growing  🔴 Declining  ⚡ Velocity  ⚠️ Stalls

[Divider]
[Section] *:bar_chart: FY[YY] Weighted Pipeline by Quarter*
[Code block] <monospace table from 2b, with TEAM totals row>
[Context] <pipeline distribution signals>

[Divider]
[Section] *:trophy: Leaderboard Highlights — [FY Quarter] QTD*
[Code block] <leaderboard from 2c>

[Divider]
[Section] *:memo: Team-Level Summary*
[mrkdwn bullets from 2d]
```

**Slack formatting rules:**
- Monospace blocks: wrap in triple backticks. Max 87 chars per line.
- Do NOT put emojis inside monospace blocks — they break column alignment.
- Use `▲`/`▼` for MoM (single-width, safe in monospace). Never `^`/`v`.
- Use `─` (U+2500) for table separator lines, not `-`.
- Keep dollar amounts short: `$86K` not `$86,400` inside tables.
- Header block does not support markdown; use `plain_text`.
- `context` blocks for legends, signals, footnotes; `section` + `mrkdwn` for summaries and tables.
- Send via `slack_write_api_call` MCP with `endpoint: chat.postMessage`, `channel` = Slack user ID, `text` = plain fallback, `blocks` = Block Kit JSON array.

---

## Data Sources Reference

| Data | Source |
|------|--------|
| SA team membership | `main.sfdc_bronze.user` (ManagerId filter) |
| SA account attribution | `main.sfdc_bronze.accountteammember` — `TeamMemberRole LIKE '%Solution Architect%'` |
| Monthly consumption | `main.gtm_gold.account_consumption_monthly` — `account_id`, `calendar_year_month` (string `'YYYY-MM'`), `dbu_dollars` |
| UCO pipeline | `main.sfdc_bronze.usecase__c` — `Stages__c`, `QtrlyPipeGenDollarDBU__c`, `Full_Production_Date__c` |
| U3/U2 velocity | `main.gtm_gold.use_case_velocity_details` — `days_in_evaluating` (U3), `days_in_scoping` (U2) |
| ASQ (owned by SA) | `main.sfdc_bronze.approvalrequest__c` — `Request_Type__c = 'Scaled SAs Support Request'`, filter `OwnerId IN (<sa_ids>)`, QTD window |
| SSA (filed by SA) | `main.sfdc_bronze.approvalrequest__c` — `Request_Type__c = 'Specialist SA (SSA) Request'`, filter `CreatedById IN (<sa_ids>)`, FY YTD window |
| STS (filed by SA) | `main.sfdc_bronze.approvalrequest__c` — `Request_Type__c = 'Shared Technical Services'` (verified 2026-03-03 for Logfood org; re-verify if deploying elsewhere — see query 1f note), filter `CreatedById IN (<sa_ids>)`, FY YTD window |
| Stage snapshots (QTD) | `main.sfdc_bronze.usecase__c` — filter `processDate = ctx["quarter_start"]` for start snapshot |
| UCO MRR $DBUs | `main.sfdc_bronze.usecase__c` — `MonthlyTotalDollarDBUs__c`; fallback: `QtrlyPipeGenDollarDBU__c / 3` |
| Fiscal calendar context | `../../resources/fiscal_calendar.py` — run via subprocess in Phase 0, provides `quarter_start`, `fy_start_date`, etc. |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoded date strings like `'2026-02-01'` pasted into queries | Always substitute from `ctx = get_fiscal_context()` — use `ctx["quarter_start"]`, `ctx["fy_start_date"]`, etc. Never paste a literal date. |
| `account_consumption_monthly.total_arr_usd` not found | Column is `dbu_dollars`; date key is `calendar_year_month` (string `'YYYY-MM'`), not a date `calendar_month` |
| Q4 pipeline shows $0 in current FY | Month 11/12 offset must be `-1999` (same as Q1–Q3); month 1 must be `-2000`. Using `-1998` for Q4 shifts all UCOs forward one FY. |
| SSA query returns 0 rows | SA is the **creator** (`CreatedById`) of SSA requests, not the owner. Always filter `CreatedById IN (<sa_ids>)` for SSA. |
| STS query returns 0 rows | Same as SSA — filter `CreatedById IN (<sa_ids>)`. Verified `Request_Type__c = 'Shared Technical Services'` for Logfood org (see query 1f note); re-verify if deploying in a different org. |
| ASQ query returns 0 rows | SA must **own** (`OwnerId`) the Scaled SA request. If QTD is 0 at start of quarter, that is correct — show "none yet" rather than widening the window. |
| `Weight__c` is NULL/0 | Always apply hardcoded weights: U2=20%, U3=40%, U4=60%, U5=80% |
| `GROUP_CONCAT` not found | Use `COLLECT_LIST` in Databricks SQL |
| `quarter_start` snapshot missing | Use first `processDate >= quarter_start` available in `usecase__c` |
| `use_case_velocity_details` timeout | Fall back to `DATEDIFF(CURRENT_DATE(), Last_Stage_Modified_Date__c)` on `usecase__c` WHERE `Stages__c = 'U2'` or `'U3'` |
| Emojis break table alignment | Put emojis only in `context` blocks below code blocks, never inside ``` blocks |
| Wide Slack table scrolls horizontally | Use SA first names (≤13 chars); use `$XXk` format; max 87 chars per line |
| SA name shown as `F. Lastname` initials | Always use first name (e.g. `Anton`, `Salih`) — never the `F. Lastname` pattern |
| Showing negative growth in leaderboard | Growth section shows only SAs with **positive** MoM; declining SAs go in the color-signal context block instead |
| Pipeline TEAM totals row missing | Always add a `─` separator + `TEAM  $Q1  $Q2  $Q3  $Q4  $Total` row at the bottom of the pipeline table |
| Team total inflated due to shared accounts | Never sum SA-level rows for TEAM figures — use query 1a Part B (deduplicated consumption) and 1b Part B (deduplicated pipeline) for all TEAM row and summary bullet values |
| Top UCO appears twice for different SAs | Query 1h uses `ROW_NUMBER() OVER (PARTITION BY p.Id ORDER BY u.Name)` — always filter `WHERE rn = 1` so each UCO appears once |

---

## Checklist (per run)

- [ ] Manager identity resolved from vibe profile or explicit input; SA team IDs loaded
- [ ] `ctx = get_fiscal_context()` called at Phase 0 start; `ctx["quarter_start"]` and `ctx["fy_start_date"]` substituted into ALL queries — zero hardcoded date strings
- [ ] All 9 queries (1a–1i) run in parallel; NULL results noted (SA may have 0 for that metric, not an error)
- [ ] 1a uses `dbu_dollars` and `calendar_year_month` (not `total_arr_usd` / `calendar_month`)
- [ ] 1d (ASQ) uses `(CreatedDate >= quarter_start OR LastModifiedDate >= quarter_start)` AND `OwnerId IN (<sa_ids>)`; captures both new + carryover requests active in Q1
- [ ] 1e (SSA) and 1f (STS) both filter by `CreatedById` FY YTD — never `OwnerId`; STS `Request_Type__c = 'Shared Technical Services'` verified for Logfood org (see query 1f note; re-verify for other orgs)
- [ ] Pipeline weights applied (U2=20%…); Q4 offsets use -1999 (months 11/12) and -2000 (month 1)
- [ ] Scorecard uses columns: `SA | T3M | MoM | U2d | U3 | ASQ | SSA | STS` — `Wtd$` omitted (shown in pipeline table); SSA and STS are FY YTD filed counts, shown as separate columns
- [ ] SA names in all tables use first name only (e.g. `Anton`, `Salih`) — never `F. Lastname` initials
- [ ] Monospace tables use `─` separators and `▲`/`▼` arrows; line widths ≤87 chars
- [ ] Pipeline table includes TEAM totals row; TEAM row values come from deduplicated query 1b Part B (not sum of SA rows)
- [ ] Scorecard TEAM T3M row uses deduplicated query 1a Part B; all team-level summary bullets use same deduplicated totals
- [ ] Leaderboard: top 3 per section; Growth section positive MoM only; Support Filed section shows SSA+STS combined total with per-type breakdown
- [ ] Team-Level Summary: ASQ says "QTD owned"; SSA says "FY YTD filed" with no T3M line
- [ ] Slack message sent to manager via Block Kit; no emojis inside code blocks
