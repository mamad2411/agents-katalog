---
name: uco-analyzer-tofu
description: >
  Generate a TOFU (Top of Funnel) territory analysis for any SA or AE. Analyzes U1, U2, and U3 UCOs
  with AI-powered stage recommendations via FMAPI — identifies UCOs that should be promoted, are blocked
  by product/engineering issues (with Aha links), need review (with downstage suggestions), or are
  correctly staged. Includes pipe gen metrics. Use this skill when someone says "TOFU analysis",
  "TOFU report", "territory report", "pipe gen report", "funnel report", "stage analysis", or
  "UCO stage analysis".
user-invocable: true
default-model: sonnet
---

# TOFU Territory Analysis — Pipe Gen & UCO Stage Analysis

Generate a self-serve TOFU (Top of Funnel) analysis for any SA, AE, or leader.
This report analyzes **every U1, U2, and U3 UCO** in a territory, classifies each using the
Databricks Foundation Model API (Llama 3.3 70B), and recommends stage promotions, flags
blocked UCOs with Aha idea links, or flags UCOs that need review with downstage suggestions.
Only **promote**, **blocked**, and **review** UCOs appear in the report tables.

**Output:** HTML report saved to `~/myvibe/weeklyplanning/` and emailed to the invoker (+ optional recipients).

**Resources:**
- `resources/classify_ucos.py` — LLM-based UCO classification via FMAPI
- `resources/build_html.py` — HTML report generator

## Report Structure

1. **Filter Bar** — AE and Account dropdowns that dynamically update ALL sections below
2. **Pipe Gen Summary** — 8-KPI banner: This Week, This Week UCOs, WoW Change, QTD UCOs, Pro-rata Att., QTD Total, QTD Target, QTD Attainment (with quarter elapsed %)
3. **U2 Stage Analysis** — Summary banner + table of promote/blocked/review UCOs only
4. **U3 Stage Analysis** — Summary banner + table of promote/blocked/review UCOs only
5. **U1 Stage Analysis** — Summary banner + table of promote/blocked/review UCOs only

Correctly staged UCOs are counted in the summary banner but **excluded from the table** to keep the report actionable.

**Interactive Filters:**
- **AE filter** — filters all tables, all summary banners, AND pipe gen KPIs. When an AE is selected, QTD Target and attainment switch to that AE's individual target (from `materialized__view_data_individual_obt`).
- **Account filter** — filters tables and summary banners by account. Pipe gen KPIs recalculate from filtered detail rows (target stays at territory level unless an AE is also selected).
- **Clear button** — resets all filters to show full territory view.

**Pipe Gen KPIs update dynamically:**
- This Week, WoW, QTD Total, QTD UCOs are recalculated from embedded `pg_detail` rows.
- QTD Target switches to the selected AE's individual target when an AE filter is applied.
- Pro-rata Att. = QTD Attainment / quarter elapsed fraction.
- QTD Attainment shows quarter elapsed % (e.g., "41.8% (43.8% elapsed)").

**Row Colors:**
- **Green** — promote: UCO should be in a higher stage
- **Red** — blocked: active product/engineering blocker (type='Blocked', NOT 'Friction'), with Aha idea links
- **Amber** — review: stalled, on hold, or at risk, with downstage suggestion (e.g., U3→U2, U2→U1)

## Phase 0: Setup & Identity

### Step 1: Load Dependencies

Load the following skills before proceeding:

```
Skill: databricks-authentication
Skill: logfood-querier
Skill: databricks-warehouse-selector
```

### Step 2: Compute Fiscal Context

Run the shared fiscal calendar to get dynamic quarter boundaries. NEVER hardcode dates.

```bash
python3 $(find ~/.claude/plugins/cache/fe-vibe/fe-shared-resources -name fiscal_calendar.py 2>/dev/null || find ~/.vibe/marketplace/plugins/fe-shared-resources -name fiscal_calendar.py 2>/dev/null)
```

Store the result as `ctx`. You will use `ctx.quarter_start`, `ctx.quarter_end`, and `ctx.fiscal_year_quarter_str` throughout.

### Step 3: Identify the Target User

Check `~/.vibe/profile` for the user's name and email.

**If the user specified a name/email**, use that directly.
**If not specified**, default to whoever ran the skill (use their profile email).

To resolve a name to email when only a name is provided, query:
```sql
SELECT Email, Name FROM main.sfdc_bronze.user
WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  AND LOWER(Name) LIKE LOWER('%{name}%')
  AND IsActive = true
```

Store:
- `target_email` — the SA/AE email (e.g., `ryan.bogden@databricks.com`)
- `target_name` — display name (e.g., `Ryan Bogden`)

Then look up the territory/role name:
```sql
SELECT u.Name, ur.Name AS role_name
FROM main.sfdc_bronze.user u
LEFT JOIN main.sfdc_bronze.userrole ur
  ON u.UserRoleId = ur.Id
  AND ur.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.userrole)
WHERE u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  AND LOWER(u.Email) = LOWER('{target_email}')
```

Store `role_name` as `territory_label`. If null or empty, default to `target_name`.

### Step 4: Verify Territory Scope

The `concatenated_emails` field in `main.gtm_silver.use_case_detail` contains the **full management hierarchy chain** — from assigned SA all the way up through FLM, Director, RVP, SVP. The `main.gtm_gold.email_exists()` UDF checks if a given email appears anywhere in that chain. This means UCO queries work for **any level** — SAs, AEs, Directors, RVPs — without needing `accountteammember` lookups.

Count how many UCOs the target user can see:

```sql
SELECT COUNT(*) AS total_ucos,
       COUNT(CASE WHEN stage_number IN (1,2,3) THEN 1 END) AS u1_u2_u3_count,
       COUNT(DISTINCT account_id) AS num_accounts
FROM main.gtm_silver.use_case_detail
WHERE main.gtm_gold.email_exists(concatenated_emails, '{target_email}')
```

Store `num_accounts` and `u1_u2_u3_count`. If 0, inform the user and stop.

**Optional:** The user may override the territory label (e.g., "Real-Money Gaming"). If not provided, use `territory_label` from Step 3.

## Phase 1: Data Collection

Run queries using the `field-data-analyst` subagent with profile `logfood`.

**CRITICAL:** Use `MAX(date)` from the consumption table as TODAY, NOT `CURRENT_DATE()`. Data lags 1-2 days.

**PARALLEL EXECUTION:** After 1a (report date), run 1b, 1c, 1d, and 1g **in parallel** — they are independent. Then run 1c2 (needs AE names from 1d). This reduces ~8 serial queries to 3 serial rounds.

### 1a: Get Report Date

```sql
SELECT MAX(date) AS d FROM main.fin_live_gold.paid_usage_metering
```

Store as `TODAY`. Compute: `L7D_START`, `PREV_L7_START`, `PREV_L7_END`, `QTD_START = ctx.quarter_start`.

### 1b: Pipe Gen — QTD Detail

```sql
SELECT p.usecase_id AS uco_id, p.account_name, p.usecase_name AS uco_name,
       p.stage, ROUND(p.usecase_pipe_gen_amount, 0) AS dbus,
       p.usecase_pipe_gen_date AS u3_date, p.target_live_date AS go_live_date,
       d.account_executive AS ae
FROM main.gtm_gold.usecase_pipe_gen_amount p
LEFT JOIN main.gtm_silver.use_case_detail d ON p.usecase_id = d.usecase_id
WHERE main.gtm_gold.email_exists(p.concatenated_emails, '{target_email}')
  AND p.usecase_pipe_gen_fiscal_year = now_fiscal_year
  AND p.usecase_pipe_gen_fiscal_quarter = now_fiscal_quarter
ORDER BY p.usecase_pipe_gen_amount DESC
```

Compute: `pg_qtd_total`, `pg_l7d_total`, `pg_l7d_count`, `pg_prev_total`, `pg_wow_pct`.

**IMPORTANT:** Save the full pipe gen detail rows (with `account_name`, `ae`, `dbus`, `u3_date`) as `pg_detail` in the metrics JSON. The HTML report uses this for dynamic filter recalculation.

### 1c: Pipe Gen — Territory Target & Attainment

```sql
SELECT ROUND(target_use_case_pipe_gen_dollars, 0) AS target,
       ROUND(use_case_pipe_gen_projection_attainment * 100, 1) AS prorata_att,
       ROUND(use_case_pipe_gen_attainment * 100, 1) AS attainment
FROM main.gtm_gold.materialized__view_data_individual_obt
WHERE user_email = '{target_email}'
  AND fiscal_year_quarter = CONCAT("FY'", RIGHT(CAST(YEAR(DATE '{QTD_START}') + 1 AS STRING), 2), ' Q{ctx.fiscal_quarter}')
```

### 1c2: Pipe Gen — Per-AE Targets & Attainment

Fetch individual targets for each AE in the territory. These power the AE-level target/attainment when the AE filter is applied.

```sql
SELECT u.Name AS ae_name,
       u.Email AS ae_email,
       ROUND(o.target_use_case_pipe_gen_dollars, 0) AS target,
       ROUND(o.use_case_pipe_gen_projection_attainment * 100, 1) AS prorata_att,
       ROUND(o.use_case_pipe_gen_attainment * 100, 1) AS attainment
FROM main.gtm_gold.materialized__view_data_individual_obt o
JOIN main.sfdc_bronze.user u
  ON LOWER(u.Email) = LOWER(o.user_email)
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
WHERE u.Name IN ({comma_separated_ae_names_from_1d_1e_1f})
  AND o.fiscal_year_quarter = CONCAT("FY'", RIGHT(CAST(YEAR(DATE '{QTD_START}') + 1 AS STRING), 2), ' Q{ctx.fiscal_quarter}')
```

Save as `ae_targets` dict in metrics JSON: `{ae_name: {target, prorata_att, attainment}}`.

**Include the target user themselves** in the AE list (e.g., if the target is a Director, include their name too so the territory-level target is also in `ae_targets`).

### 1d: All U1/U2/U3 UCOs — Single Query (no limit — fetch ALL)

Uses `use_case_detail` + `email_exists()` so it works for SAs, AEs, Directors, and RVPs — anyone in the management chain. Fetches all three stages in one query and includes `CreatedDate` to avoid a separate query later.

```sql
SELECT d.usecase_id AS uco_id, d.account_name, d.usecase_name AS uco_name,
       CONCAT('U', d.stage_number) AS stage,
       d.stage_number,
       ROUND(d.estimated_quarterly_dollar_dbus, 0) AS dbus,
       ROUND(CAST(u.CurrentStageDaysCount__c AS DOUBLE), 0) AS days,
       CAST(u.Full_Production_Date__c AS STRING) AS go_live_date,
       u.Demand_Plan_Next_Steps__c AS next_step,
       d.account_executive AS ae,
       CAST(u.CreatedDate AS STRING) AS created_date
FROM main.gtm_silver.use_case_detail d
JOIN main.sfdc_bronze.usecase__c u
  ON d.usecase_id = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
WHERE main.gtm_gold.email_exists(d.concatenated_emails, '{target_email}')
  AND d.stage_number IN (1, 2, 3)
ORDER BY d.stage_number, d.estimated_quarterly_dollar_dbus DESC
```

**Split client-side** into three lists by `stage_number` (1→U1, 2→U2, 3→U3) before saving. Trim `created_date` to first 10 chars (date only).

**IMPORTANT:** Do NOT truncate `next_step`. Do NOT limit results.

### 1g: Active Blockers (optional but recommended)

Fetch active blockers (type='Blocked' only, NOT 'Friction') for all UCOs in the territory. Uses the enriched `gtm_silver.blocker_detail` table which includes Aha idea data.

```sql
SELECT
  bd.usecase_id,
  bd.blocker_name,
  bd.blocker_status,
  bd.type,
  bd.category,
  bd.dbu_dollars_blocked,
  bd.comment,
  bd.aha
FROM main.gtm_silver.blocker_detail bd
WHERE bd.usecase_id IN (
  SELECT d.usecase_id FROM main.gtm_silver.use_case_detail d
  WHERE main.gtm_gold.email_exists(d.concatenated_emails, '{target_email}')
    AND d.stage_number IN (1, 2, 3)
)
  AND bd.blocker_status = 'Open'
  AND bd.type = 'Blocked'
```

**Notes:**
- The `aha` column is `ARRAY<STRUCT>` with fields: `aha_idea_id`, `aha_name`, `aha_link`, `aha_status`, `aha_owner`, `aha_reference`, `aha_last_modified_date`
- Only fetch type='Blocked' — 'Friction' is not a true blocker
- Save to `/tmp/{name_sanitized}_blockers.json`

### Save Intermediate Data

Split the single UCO query result by `stage_number` and save to temporary files:
- U1 UCOs (stage_number=1) → `/tmp/{name_sanitized}_u1_ucos.json`
- U2 UCOs (stage_number=2) → `/tmp/{name_sanitized}_u2_ucos.json`
- U3 UCOs (stage_number=3) → `/tmp/{name_sanitized}_u3_ucos.json`
- Blockers → `/tmp/{name_sanitized}_blockers.json`

Each UCO already has `created_date` from the merged query — no separate created dates query needed.
- Metrics → `/tmp/{name_sanitized}_metrics.json` containing:
  - Date context: `TODAY`, `L7D_START`, `PREV_L7_START`, `PREV_L7_END`, `QTD_START`
  - Territory: `num_accounts`
  - Pipe gen aggregates: `pg_qtd_total`, `pg_l7d_total`, `pg_l7d_count`, `pg_prev_total`, `pg_wow_pct`, `pg_qtd_count`
  - Pipe gen targets: `pg_target`, `pg_attainment`, `pg_prorata_attainment`
  - Pipe gen detail: `pg_detail` (list of `{account_name, ae, dbus, u3_date}` for each QTD pipe gen UCO)
  - Per-AE targets: `ae_targets` (dict of `{ae_name: {target, prorata_att, attainment}}`)

## Phase 2: AI Stage Classification

Run the classification script. This calls Databricks FMAPI (Llama 3.3 70B) to classify each UCO.

```bash
python3 {skill_resources_dir}/classify_ucos.py \
  --u2-file /tmp/{name_sanitized}_u2_ucos.json \
  --u3-file /tmp/{name_sanitized}_u3_ucos.json \
  --u1-file /tmp/{name_sanitized}_u1_ucos.json \
  --blockers-file /tmp/{name_sanitized}_blockers.json \
  --output /tmp/{name_sanitized}_classified.json \
  --profile logfood
```

The script:
- Classifies U2, U3, and U1 stages **in parallel** using a shared thread pool (6 workers)
- Sends UCOs in batches of 20 to FMAPI
- Classifies each as `promote`, `blocked`, `review`, or `correct`
- For `promote`: suggests a target stage (U2, U3, U4, or U5) with an actionable reason
- For `blocked`: identifies active product/engineering blockers with Aha idea references
- For `review`: suggests a downstage (U3→U2/U1, U2→U1) or closure with a reason
- Uses temperature=0 for consistent results
- Handles 429 rate limiting with aggressive exponential backoff
- Saves classified data (with `_blockers` field for Aha links) to the output JSON

### Classification Framework

The FMAPI system prompt is grounded in two official Databricks frameworks:

**1. UCO Stage Definitions & Exit Criteria:**
- U1 (Validating, 0%) → U2 (Scoping, 10%) → U3 (Evaluating, 50%) → U4 (Confirming) → U5 (Onboarding) → U6 (Live)
- Each stage has tier-based exit criteria (All UCOs, M+ ≥$2k MRR, XL+ ≥$10k MRR) that the LLM checks against next steps
- Jobs to be Done per stage (e.g., U1→U2: confirm customer acknowledges a pain point; U2→U3: secure eval kickoff)

**2. MEDDPICC Methodology:**
- **M**etrics, **E**conomic Buyer, **D**ecision Criteria, **D**ecision Process, **P**ath to Production, **I**dentified Pain, **C**ompetition, **C**hampion
- Classification reasons reference MEDDPICC elements (e.g., "Kickoff POC meeting and confirm Decision Criteria")

**Classification Rules by Stage:**
- **U2 UCOs:** Promote to U3 if next steps mention eval kickoff, POC setup, or technical validation. Champions is Optional at U2→U3. Partner logged if applicable. Review/downstage if no updates >90 days, deprioritized, or no clear customer engagement.
- **U3 UCOs:** Promote to U4 if next steps mention successful POC completion, results review, or decision timeline. For M+: requires Onboarding Month/Strategy/Plan. For XL+: also requires Metrics, EvalPath, Tech Decision Maker. Review/downstage if stalled >120 days, customer unresponsive, or competitor risk.
- **U1 UCOs:** Promote to U2 if next steps show confirmed pain, scheduled meetings, or scoping activity. Review if no updates or unclear customer interest.

**Exit Criteria Note:** Rigidity around exit criteria has been dropped — strict enforcement now only applies to XL+ (≥$10k MRR). For smaller UCOs, criteria are guidelines not gates.

**Close/Regress Guidance (stage-specific):**
- U1 Close: "New Demand not Validated", "Customer Unresponsive"
- U2 Close: "New Demand not Validated", "Not Qualified". Regress to U1: "Not Ready for SA Review", "Readiness Criteria Not Met"
- U3+ Close: "Lost after Pipe-gen", "Customer Unresponsive". Regress: "Go-live Not Ready", "Stuck/Legacy"
- Reasons are 10-20 words long and actionable (e.g., "Schedule eval kickoff with SA" not just "ready for U3")

**Acceleration Mechanisms:**
- The LLM suggests acceleration mechanisms when appropriate: PS (RSA/Advisory/Implementation), Partner/SI (Brickbuilder Accelerators), Funding/Credits (POC/Consumption), Technical Programs (Immersion Day, Solution Accelerator, Hackathon), Champion Development
- Only one acceleration mechanism suggested per UCO — the most impactful one

**Expected runtime:** ~40-60 seconds for 500+ UCOs (parallel classification across stages).

## Phase 3: Generate HTML Report

Run the HTML builder script:

```bash
python3 {skill_resources_dir}/build_html.py \
  --classified /tmp/{name_sanitized}_classified.json \
  --metrics /tmp/{name_sanitized}_metrics.json \
  --output ~/myvibe/weeklyplanning/{Name}\ TOFU\ Analysis\ Report.html \
  --name "{target_name}" \
  --territory "{territory_label}"
```

The script:
- Only includes `promote`, `blocked`, and `review` UCOs in the HTML tables
- Green rows = promote, Red rows = blocked (with Aha links), Amber rows = review (with downstage)
- `correct` UCOs are counted in the summary banner but excluded from tables
- 4-column summary banner per stage: Potentially Higher Stage | Blocked | Needs Review | Correctly Staged
- AE and Account filter dropdowns that dynamically update ALL sections (tables, banners, pipe gen KPIs)
- Pipe gen KPIs: 8 metrics with per-AE target resolution (switches to AE's individual target when filtered)
- QTD Attainment displays quarter elapsed % (e.g., "41.8% (43.8% elapsed)")
- Pro-rata Att. = attainment / quarter elapsed fraction, recalculated on filter change
- Per-AE targets embedded as JS data (`aeTargets`) from `ae_targets` in metrics
- Pipe gen detail embedded as JS data (`pgDetail`) from `pg_detail` in metrics for client-side recalculation
- Target live dates formatted as "Mon YYYY" (e.g., "Mar 2026")
- Timestamp in AMER ET format in report header

## Phase 4: Save & Open

1. **Open** in the browser: `open ~/myvibe/weeklyplanning/{Name}\ TOFU\ Analysis\ Report.html`
2. **Tell the user** a summary:
   - Pipe Gen QTD: ${total} / ${target} ({attainment}%), Pro-rata: {prorata}%
   - This Week: ${l7d_total} ({l7d_count} UCOs), WoW: {wow}%
   - U2 Analysis: {promote} promote, {blocked} blocked, {review} review, {correct} correctly staged
   - U3 Analysis: {promote} promote, {blocked} blocked, {review} review, {correct} correctly staged
   - U1 Analysis: {promote} promote, {blocked} blocked, {review} review, {correct} correctly staged

## Phase 5: Email Delivery

Send the report via email using the `gmail` skill.

### Determine Recipients

- **Default recipient:** The person who invoked the skill (read their email from `~/.vibe/profile`).
- **Additional recipients:** If the user provided extra email addresses, include them as well.

### Send the Email

Use the `gmail` skill to send:

- **To:** All recipients (comma-separated)
- **Subject:** `TOFU Analysis — {target_name} ({territory_label}) · {TODAY_FORMATTED}` where `TODAY_FORMATTED` is Month DD, YYYY (e.g., `March 12, 2026`)
- **Body:** The full HTML report content (send as HTML email, not as an attachment)

### Confirm to the User

After sending, tell the user: email sent to {recipients}, subject line used.

## Quick Reference

| Metric | Source Table | Key Field |
|--------|-------------|-----------|
| Pipe Gen | `main.gtm_gold.usecase_pipe_gen_amount` | `usecase_pipe_gen_amount` |
| Pipe Gen Target (territory) | `main.gtm_gold.materialized__view_data_individual_obt` | `target_use_case_pipe_gen_dollars` |
| Pipe Gen Target (per-AE) | `main.gtm_gold.materialized__view_data_individual_obt` | Same table, queried for each AE |
| UCO Detail | `main.gtm_silver.use_case_detail` | `usecase_id`, `concatenated_emails`, `stage_number`, `account_executive` |
| UCO Raw | `main.sfdc_bronze.usecase__c` | `CurrentStageDaysCount__c`, `Demand_Plan_Next_Steps__c` |
| Hierarchy UDF | `main.gtm_gold.email_exists()` | Checks if email is in `concatenated_emails` chain |
| Blockers | `main.gtm_silver.blocker_detail` | `usecase_id`, `type`, `aha` (ARRAY<STRUCT>) |
| Consumption | `main.fin_live_gold.paid_usage_metering` | `date` (for MAX date only) |

## Troubleshooting

- **"No UCOs found"**: The email may not appear in any `concatenated_emails` chain. Try the full email (e.g., `jimmy.aveningo@databricks.com` not `james.aveningo@databricks.com`). The `concatenated_emails` field uses the Salesforce email which may differ from the display name.
- **Empty pipe gen**: The SA may not have any UCOs that reached U3 this quarter. Normal early in quarter.
- **Stale data**: Logfood data lags 1-2 days. Report date reflects latest available data.
- **Classification timeout**: For very large territories (1000+ UCOs), classification may take 3-5 minutes. This is expected.
- **FMAPI errors**: If the serving endpoint is rate-limited, the script retries with exponential backoff (up to 2 retries per batch).
