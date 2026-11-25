---
name: dsa-weekly-report
description: Generate a comprehensive weekly activity report for a DSA covering hours, deliverables, UCO progress, consumption changes, and upcoming milestones. Use when a DSA says weekly report, activity report, DSA report, weekly summary, week in review.
user-invocable: true
---

# DSA Weekly Report

Generate a comprehensive weekly activity report for a DSA covering hours, deliverables, UCO progress, consumption changes, and upcoming milestones. This report provides a structured week-in-review suitable for sharing with managers or stakeholders.

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** -- Run `/salesforce-authentication`
2. **Logfood** -- Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`

## Query Reference

All SQL and SOQL templates used by this skill are documented in:
- `fe-dsa:dsa-account-prep` skill -> `resources/DSA_QUERIES.md`

The output template is documented in:
- `resources/WEEKLY_REPORT_TEMPLATE.md`

---

## Fiscal Calendar Awareness

Databricks fiscal year starts **February 1**:

| Quarter | Months | Example (FY27) |
|---------|--------|----------------|
| Q1 | Feb - Apr | Feb 2026 - Apr 2026 |
| Q2 | May - Jul | May 2026 - Jul 2026 |
| Q3 | Aug - Oct | Aug 2026 - Oct 2026 |
| Q4 | Nov - Jan | Nov 2026 - Jan 2027 |

When generating the report, always include the current fiscal quarter in the header. Use the format `FY<YY>-Q<N>` (e.g., FY27-Q1 for February 2026).

---

## Step 0: Discover DSA Identity

**This step runs automatically when the skill is invoked.**

**IMPORTANT: Always use `--target-org` on every `sf` CLI command.**

### 0A: Resolve Salesforce Org and User

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
USER_EMAIL="$SF_TARGET_ORG"
```

### 0B: Get Salesforce User ID and Name

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Email FROM User WHERE Email = '${USER_EMAIL}'" --json
```

### 0C: Get All Assigned Accounts and Assignments

Run in parallel:

1. **AccountTeamMember query** (Salesforce) -- all accounts with DSA role
2. **DSA Assignment query** (Logfood) -- from `main.field_dsa.dsa_project_assignment_outcomes`
3. **DSA Bandwidth query** (Logfood) -- from `main.field_dsa.dsa_bandwidth_table`

---

## Step 1: Gather Weekly Data

For the reporting period (default: last 7 days), gather data across all assigned accounts.

### 1A: UCO Pipeline Snapshot (Logfood)

Query `main.gtm_gold.rpt_use_case_pipeline_monthly` for all assigned accounts (see DSA_QUERIES.md Section 4).

Collect per UCO:
- Current stage and health
- Days in stage
- Estimated quarterly DBUs
- Number of blockers
- Target live date
- Last modified date

### 1B: UCO Changes via projection_month_end_date Diff (Logfood)

To detect changes over the week, compare the latest `projection_month_end_date` snapshot against the snapshot from 7 days ago using ROW_NUMBER windowing. This reveals:

- **Stage changes** -- UCOs that moved stages (e.g., U3 -> U4)
- **Health changes** -- UCOs whose health status changed
- **New UCOs** -- UCOs that appeared in the current snapshot but not the prior one
- **Completed UCOs** -- UCOs that moved to U6 or were marked Lost/Disqualified

```sql
-- Current snapshot
WITH current_ucos AS (
  SELECT
    usecase_id, usecase_name, account_name, stage_name_ui,
    CAST(stage_number AS INT) AS stage_number,
    implementation_status, CAST(estimated_quarterly_dollar_dbus AS DOUBLE) AS est_dbus,
    CAST(num_of_blockers AS INT) AS blockers,
    ROW_NUMBER() OVER (PARTITION BY usecase_id ORDER BY projection_month_end_date DESC) AS rn
  FROM main.gtm_gold.rpt_use_case_pipeline_monthly
  WHERE LOWER(dsa) LIKE '%<DSA_NAME>%'
    AND estimated_quarterly_dollar_dbus >= 0
),
-- Prior snapshot (7 days ago)
prior_ucos AS (
  SELECT
    usecase_id, stage_name_ui AS prev_stage,
    CAST(stage_number AS INT) AS prev_stage_number,
    implementation_status AS prev_health,
    CAST(estimated_quarterly_dollar_dbus AS DOUBLE) AS prev_est_dbus,
    ROW_NUMBER() OVER (PARTITION BY usecase_id ORDER BY projection_month_end_date DESC) AS rn
  FROM main.gtm_gold.rpt_use_case_pipeline_monthly
  WHERE LOWER(dsa) LIKE '%<DSA_NAME>%'
    AND estimated_quarterly_dollar_dbus >= 0
    AND projection_month_end_date <= DATE_ADD(CURRENT_DATE(), -7)
)
SELECT
  c.usecase_id, c.usecase_name, c.account_name,
  c.stage_name_ui AS current_stage, c.stage_number,
  p.prev_stage, p.prev_stage_number,
  c.implementation_status AS current_health,
  p.prev_health,
  c.est_dbus, p.prev_est_dbus,
  c.blockers,
  CASE
    WHEN p.usecase_id IS NULL THEN 'NEW'
    WHEN c.stage_number != p.prev_stage_number THEN 'STAGE_CHANGE'
    WHEN c.implementation_status != p.prev_health THEN 'HEALTH_CHANGE'
    WHEN c.est_dbus != p.prev_est_dbus THEN 'DBUS_CHANGE'
    ELSE 'NO_CHANGE'
  END AS change_type
FROM current_ucos c
LEFT JOIN prior_ucos p ON c.usecase_id = p.usecase_id AND p.rn = 1
WHERE c.rn = 1
ORDER BY c.account_name, c.stage_number
```

### 1C: Consumption Delta (Logfood)

Query consumption changes using the Historical Diff pattern from DSA_QUERIES.md Section 7. Compare current vs prior month date ranges across all accounts (this table is not snapshot-based — use `date` ranges, not `processDate`).

### 1D: Assignment Changes

Check for any changes in assignments:
- New assignments added this week
- Assignments that ended this week
- FTE or hour changes

---

## Step 2: Detect Changes and Highlights

Process the raw data to identify noteworthy events:

### Change Categories

| Category | Detection Logic |
|----------|----------------|
| **Stage Advancement** | UCO stage_number increased from prior snapshot |
| **Stage Regression** | UCO stage_number decreased (unusual, flag prominently) |
| **Health Improvement** | Red -> Yellow, Yellow -> Green |
| **Health Degradation** | Green -> Yellow, Yellow -> Red |
| **New UCO** | Present in current but not prior snapshot |
| **Completed UCO** | Moved to U6 or Lost/Disqualified |
| **Consumption Spike** | Account consumption up >15% WoW |
| **Consumption Drop** | Account consumption down >10% WoW |
| **New Assignment** | assignment_start_date falls within this week |
| **Ending Assignment** | assignment_end_date falls within next 14 days |
| **Approaching Milestone** | target_live_date within 14 days |
| **Blocker Added** | num_of_blockers increased from prior snapshot |
| **Blocker Resolved** | num_of_blockers decreased from prior snapshot |

### Win Detection

Automatically tag as a **Win**:
- UCO advancing to U5 or U6
- Health improving from Red/Yellow to Green
- Blocker resolved
- Consumption growth >15%

### Risk Detection

Automatically tag as a **Risk**:
- UCO health degrading
- Past-due target date
- Consumption declining >10%
- Assignment ending without extension
- Over-capacity bandwidth

---

## Step 3: Build Weekly Report

Use the template in `resources/WEEKLY_REPORT_TEMPLATE.md` to structure the report.

### Report Sections

1. **Report Period** -- Week of <DATE> to <DATE>, fiscal quarter
2. **Executive Summary** -- 2-3 sentence overview of the week
3. **Bandwidth Summary** -- Total FTE, hours, capacity flag, per-account breakdown
4. **Account-by-Account Detail** -- For each account:
   - UCO changes (stage movements, health changes)
   - Consumption trend
   - Key activities and deliverables
   - Upcoming milestones
5. **Wins** -- Positive outcomes from the week
6. **Risks** -- Items needing attention
7. **Next Week Priorities** -- Top 3-5 items for the coming week

### Auto-Generated Priorities

Based on the detected changes and flags, generate next-week priorities:

1. Any HIGH action items from status flags
2. UCOs approaching target dates
3. Accounts with declining consumption
4. Assignments ending soon
5. UCOs with stale updates

---

## Step 4: Output

### Console Output (Default)

Render the weekly report directly in the terminal using markdown formatting.

### Google Doc Output (Optional)

If the user requests a Google Doc:

1. Save markdown to temp file:
```bash
cat > /tmp/dsa_weekly_report.md << 'CONTENT'
[Weekly report markdown content]
CONTENT
```

2. Convert to Google Doc:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/dsa_weekly_report.md \
  --title "DSA Weekly Report - <DSA_NAME> - Week of <DATE>"
```

3. Post-process for status colors (Green/Yellow/Red).

Return the Google Doc URL to the user.

---

## Example Invocations

| Prompt | What Happens |
|--------|-------------|
| "Weekly report" | Full weekly report across all accounts |
| "DSA weekly summary" | Same as above |
| "Week in review" | Full report with emphasis on changes |
| "Activity report for last week" | Report for the prior 7-day period |
| "Weekly report as Google Doc" | Report saved to Google Doc |

---

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/dsa-account-prep` | Deep-dive prep for a single account meeting |
| `/dsa-status-update` | Quick status check with action items |
| `/uco-updates` | Update UCO fields based on weekly findings |
| `/dsa-handoff` | Account transition document |
| `/logfood-querier` | Ad-hoc Logfood queries for deeper analysis |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| No UCO changes detected | The UCO diff uses `projection_month_end_date` windowing; changes depend on Logfood data refresh cadence and may lag |
| Consumption delta is zero | This table uses `date` ranges (not snapshots); verify the date range covers two distinct periods with data (see DSA_QUERIES.md Section 7) |
| Missing accounts | Cross-reference AccountTeamMember (SF) with assignment_outcomes (Logfood) |
| Fiscal quarter wrong | FY starts Feb 1; FY27-Q1 = Feb-Apr 2026 |
