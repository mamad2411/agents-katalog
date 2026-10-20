---
name: dsa-capacity-planning
description: FTE allocation analysis for DSA team leads. Shows team bandwidth utilization, identifies over/under-allocated DSAs, flags expiring assignments, and recommends rebalancing. Use when someone says capacity planning, FTE planning, bandwidth analysis, team allocation, DSA capacity, rebalancing.
user-invocable: true
---

# DSA Capacity Planning

FTE allocation analysis for DSA team leads. This skill provides a comprehensive view of team bandwidth utilization, identifies over- and under-allocated DSAs, flags expiring assignments, surfaces upcoming starts, and generates rebalancing recommendations.

**This skill is read-only. It never writes to any data source.**

## When to Use This Skill

Use this skill when you need to:
- Review current FTE allocation across the team
- Identify over-allocated or under-leveraged DSAs
- Plan for upcoming assignment expirations
- Prepare for capacity planning discussions with leadership
- Evaluate whether the team can absorb new work
- Generate a rebalancing recommendation

## Prerequisites

Before running this skill, ensure:
1. **Databricks** — Run `/databricks-authentication` (for Logfood queries)

No Salesforce or Google auth needed unless you want to generate a Google Doc (optional).

## Required Information

The skill needs a **team lead name** or **manager filter**. Provided as: $ARGUMENTS

If not provided, ask the user.

## Reference Files

- **`resources/DSA_LT_QUERIES.md`** (in `dsa-business-overview/resources/`) — SQL query templates
- **`resources/CAPACITY_TEMPLATE.md`** — Output template structure

---

## Step 0: Team Discovery

Identify the team using `main.field_dsa.dsa_roster_curr`:

```sql
SELECT dsa AS name, email, hire_date, dsa_manager
FROM main.field_dsa.dsa_roster_curr
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY dsa
```

Build:
- `dsa_names` list
- `manager_name` pattern

If no results, ask the user for the team lead name or a list of DSA names.

---

## Step 1: Current Allocation

Launch the `fe-dsa-lt:capacity-calculator` agent to query and compute:

### 1a. Bandwidth Data (Source of Truth for FTE Totals)

**CRITICAL: Use `main.field_dsa.dsa_bandwidth_table` for per-DSA FTE totals.** This is the authoritative source — the same table the DSA Operations Dashboard uses. Do NOT sum `fte_req` from `dsa_project_assignment_outcomes` — it has overlapping subscription rows that inflate totals.

```sql
SELECT dsa,
  CAST(regexp_extract(bandwidth_bar_html, 'font-weight:600;">([0-9.]+)<', 1) AS DOUBLE) AS total_fte,
  capacity_flag, account_dsa_accounts_html
FROM main.field_dsa.dsa_bandwidth_table
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY total_fte DESC
```

| DSA | Total FTE | Capacity Flag | Active Accounts |
|-----|-----------|---------------|-----------------|

Count active accounts by parsing `account_dsa_accounts_html` — entries with `ASSIGNMENT` status (green, `color:#137333`) are active.

### 1b. Assignment Detail (for Per-Subscription Detail Only)

From `main.field_dsa.dsa_project_assignment_outcomes` (exploded). Use for subscription detail (tier, hours, dates, engagement type) but NOT for summing FTE totals:

For each DSA, list every active assignment with:
- Account name
- Project name
- Engagement type
- Start/end dates
- Hours/week
- FTE requirement (per-subscription — will NOT match bandwidth table totals)
- Fiscal quarter tags (start_fq, end_fq)
- Cost center
- Business unit

### 1c. Per-DSA Summary

| DSA | Accounts | Total FTE | Capacity Flag | Classification |
|-----|----------|-----------|---------------|----------------|

**Total FTE comes from `dsa_bandwidth_table`** (Step 1a), NOT from summing assignment detail.

---

## Step 2: Bandwidth Analysis

For each DSA, compute utilization metrics:

### Utilization Table

| DSA | Total FTE | Max Capacity | Utilization % | Flag | Classification |
|-----|-----------|-------------|---------------|------|----------------|

**Classification rules**:
- **Over-Allocated** (Red): Total FTE > 1.0 (utilization > 100%)
- **At Capacity** (Yellow): Total FTE 0.9 - 1.0 (utilization 90-100%)
- **Healthy** (Green): Total FTE 0.6 - 0.89 (utilization 60-89%)
- **Under-Allocated** (Blue): Total FTE < 0.6 (utilization < 60%)

### Headroom Analysis

| DSA | Current FTE | Available FTE | Can Absorb |
|-----|-------------|---------------|------------|

`Available FTE = 1.0 - Current FTE` (clamped to 0 if negative)

`Can Absorb` = qualitative assessment:
- "Full assignment (0.5+ FTE)" if headroom >= 0.5
- "Partial engagement (0.25 FTE)" if headroom 0.25-0.49
- "At capacity — no new work" if headroom < 0.25

### Team Aggregate

| Metric | Value |
|--------|-------|
| Team Size | {count} DSAs |
| Total FTE Allocated | {sum} |
| Total Capacity | {count} * 1.0 = {max} FTE |
| Team Utilization | {utilization}% |
| Over-Allocated | {over_count} DSAs |
| Under-Allocated | {under_count} DSAs |
| Available Headroom | {headroom} FTE |

---

## Step 3: Expiring Assignments

Analyze assignments expiring in the next 30, 60, and 90 days:

### 30-Day Window

| DSA | Account | Project | End Date | FTE | Impact |
|-----|---------|---------|----------|-----|--------|

### 60-Day Window

| DSA | Account | Project | End Date | FTE | Impact |
|-----|---------|---------|----------|-----|--------|

### 90-Day Window

| DSA | Account | Project | End Date | FTE | Impact |
|-----|---------|---------|----------|-----|--------|

### Expiry Timeline Summary

| Window | Assignments Ending | FTE Freeing Up | DSAs Affected |
|--------|-------------------|----------------|---------------|
| Next 30 days | {count} | {fte} | {dsa_list} |
| 31-60 days | {count} | {fte} | {dsa_list} |
| 61-90 days | {count} | {fte} | {dsa_list} |
| **Total** | **{total}** | **{total_fte}** | |

---

## Step 4: Upcoming Assignments

Filter for `assignment_status_custom = 'UPCOMING'`:

| DSA | Account | Project | Start Date | FTE | Engagement Type |
|-----|---------|---------|------------|-----|-----------------|

### Net Capacity Forecast (90 Days)

| DSA | Current FTE | Expiring FTE | Upcoming FTE | Projected FTE | Projected Utilization |
|-----|-------------|-------------|-------------|---------------|----------------------|

---

## Step 5: Rebalancing Recommendations

Based on the analysis, generate specific recommendations:

### Recommendation Categories

1. **Immediate Actions** (this week)
   - DSAs over 100% utilization — identify assignments to redistribute
   - Critical expirations with no renewal

2. **Short-Term** (next 30 days)
   - Redistribute work from over-allocated to under-allocated DSAs
   - Fill coverage gaps at high-value accounts

3. **Medium-Term** (next quarter)
   - Plan for bulk expirations
   - Staff upcoming assignments
   - Address structural imbalances

### Recommendation Format

For each recommendation:

```
**[Priority: High/Medium/Low]** — {Short description}

Current State: {What the data shows}
Recommendation: {Specific action}
Impact: {What changes — FTE, DSA, accounts affected}
```

### Example Recommendations

```
**[Priority: High]** — Redistribute load from Richa Sethi (1.3 FTE, over-allocated)

Current State: Richa is at 130% utilization with 8 accounts. Two assignments
(Account A, Account B) are Silver tier at 0.125 FTE each.
Recommendation: Transfer Account A to Patrick Chan (0.6 FTE, under-allocated,
same region) and Account B to Steve Morgan (0.55 FTE, has capacity).
Impact: Richa drops to 1.05 FTE. Patrick rises to 0.725 FTE. Steve rises to 0.675 FTE.
```

```
**[Priority: Medium]** — Plan for Q2 expiration wave (3 assignments, 0.75 FTE)

Current State: Three assignments end in May-Jun — Account X (0.25 FTE),
Account Y (0.25 FTE), Account Z (0.25 FTE). All assigned to different DSAs.
Recommendation: Begin renewal discussions now. If not renewing, identify
replacement work to maintain utilization. Flag Account X as highest risk
(customer may not renew).
Impact: Without renewals, team utilization drops from 82% to 74%.
```

---

## Step 6: Output

Present results as a formatted summary in the conversation. If the user requests a Google Doc:

1. Write markdown to `/tmp/claude/dsa_capacity_planning.md`
2. Convert with markdown_to_gdocs.py:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/dsa_capacity_planning.md \
  --title "DSA Capacity Planning — {Month Year}"
```

---

## Domain Rules

### Tier Classification
- **Platinum**: >= 32 hours/week = 1.0 FTE
- **Gold**: >= 16 hours/week = 0.5 FTE
- **Silver**: < 16 hours/week = 0.25 FTE

### Databricks Fiscal Year
- FY starts February 1
- Q1: Feb-Apr, Q2: May-Jul, Q3: Aug-Oct, Q4: Nov-Jan

### Assignment Statuses
- `CURRENT ASSIGNED` — Active engagement
- `UPCOMING` — Scheduled, not yet started

### Max Capacity
- Standard DSA max capacity = 1.0 FTE
- Exceeding 1.0 indicates over-allocation

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No roster data | Ask user for team lead name or DSA list |
| Logfood timeout | Retry once after 30s (cold start) |
| No bandwidth data | Fall back to assignment data only (compute FTE from fte_req column) |
| Empty assignments | Report zero allocation — DSA may be new or between assignments |
| Stale data | Note data freshness — Logfood tables refresh on their own schedule |

---

## Related Skills

- `/dsa-business-overview` — Monthly overview doc (uses capacity data as one section)
- `/dsa-assignment-sync` — Validate assignments against Salesforce
- `/logfood-querier` — Direct Logfood SQL queries
