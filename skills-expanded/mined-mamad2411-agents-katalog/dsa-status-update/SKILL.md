---
name: dsa-status-update
description: Generate a weekly DSA status update covering all assigned accounts, UCO health, bandwidth utilization, and deliverables. Automates the weekly review workflow. Use when a DSA says DSA status, weekly status, status update, weekly review, DSA check-in.
user-invocable: true
---

# DSA Status Update

Generate a weekly DSA status update covering all assigned accounts, UCO health, bandwidth utilization, and deliverables. This skill automates the weekly review workflow that every DSA must complete.

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** -- Run `/salesforce-authentication`
2. **Logfood** -- Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`

## Query Reference

All SQL and SOQL templates used by this skill are documented in:
- `fe-dsa:dsa-account-prep` skill -> `resources/DSA_QUERIES.md`

The output template is documented in:
- `resources/STATUS_UPDATE_TEMPLATE.md`

---

## Step 0: Discover DSA Identity and All Assigned Accounts

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

Store `User.Id` as `DSA_USER_ID` and `User.Name` as `DSA_NAME`.

### 0C: Find ALL Accounts Where User is DSA

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Account.Name, Account.Id, AccountId, TeamMemberRole \
   FROM AccountTeamMember \
   WHERE UserId = '<DSA_USER_ID>' \
   AND TeamMemberRole = 'DSA'" --json
```

Store the full list of accounts. If no results, fall back to querying UCOs where `DSA__r.Email = '${USER_EMAIL}'` and extract unique account names.

### 0D: Get All DSA Assignments from Logfood

Load the `logfood-querier` skill, then query assignments:

```sql
-- See DSA_QUERIES.md Section 2: DSA Project Assignments
-- Filter: WHERE LOWER(pa.assignment_resource_user_name) LIKE '%<DSA_NAME>%'
--   AND pa.assignment_status_custom IN ('CURRENT ASSIGNED', 'UPCOMING')
```

This gives you the authoritative list of active accounts with assignment details (hours, FTE, engagement type, dates).

---

## Step 1: Per-Account Data Collection

For EACH assigned account, gather data using the `field-data-analyst` subagent or `account-researcher` agent. Execute queries in parallel across accounts where possible.

### 1A: UCO Health per Account (Logfood)

Query `main.gtm_gold.rpt_use_case_pipeline_monthly` for each account (see DSA_QUERIES.md Section 4). Collect:

- UCO count by stage (U1-U6)
- UCO count by health (Red/Yellow/Green/null)
- Total estimated_quarterly_dbus
- Days in stage per UCO
- Blockers count per UCO

### 1B: Consumption Delta per Account (Logfood)

Query `main.fin_live_gold.paid_usage_metering` with date range filter (see DSA_QUERIES.md Section 7: Historical Diff). Compare:

- Current 30-day consumption vs prior 30-day consumption
- Identify significant changes (>10% delta)

### 1C: DSA Bandwidth (Logfood)

```sql
-- See DSA_QUERIES.md Section 3: DSA Bandwidth
-- Filter: WHERE LOWER(dsa) LIKE '%<DSA_NAME>%'
```

---

## Step 2: Bandwidth Context

Calculate overall DSA utilization:

| Metric | Calculation |
|--------|------------|
| Total Assigned FTE | SUM of fte_req across all active assignments |
| Total Weekly Hours | SUM of subscription_hours_weekly across all assignments |
| Capacity Flag | From dsa_bandwidth_table |
| Utilization % | (assigned_bandwidth / 1.0) * 100 |

### DSA Tier per Account

For each account, classify:
- **Platinum**: subscription_hours_weekly >= 32 (1.0 FTE)
- **Gold**: subscription_hours_weekly >= 16 (0.5 FTE)
- **Silver**: subscription_hours_weekly < 16 (0.25 FTE)

---

## Step 3: Identify Action Items

Scan all gathered data for items requiring attention. Flag each with a severity.

### Automatic Flags

| Flag | Condition | Severity |
|------|-----------|----------|
| Stale UCO | UCO with `days_in_stage > 30` and no recent Next Steps (>7 days) | HIGH |
| Red Health | UCO with `implementation_status = 'Red'` | HIGH |
| Yellow Health | UCO with `implementation_status = 'Yellow'` | MEDIUM |
| Past-Due Target | UCO where `target_live_date < TODAY` | HIGH |
| Approaching Target | UCO where `target_live_date` is within 14 days | MEDIUM |
| Declining Consumption | Account with >10% MoM consumption decrease | MEDIUM |
| No Health Set | Active U2+ UCO with null implementation_status | LOW |
| Ending Assignment | Assignment end date within 30 days | MEDIUM |
| Over Capacity | capacity_flag = 'Red' | HIGH |
| Unresolved Blockers | UCO with num_of_blockers > 0 | HIGH |

### Priority Ordering

Present action items in this order:
1. HIGH severity items (Red UCOs, past-due, over capacity)
2. MEDIUM severity items (Yellow UCOs, declining consumption, approaching dates)
3. LOW severity items (missing health, minor updates needed)

---

## Step 4: Generate Status Summary

Build the status update using the template in `resources/STATUS_UPDATE_TEMPLATE.md`.

### Summary Metrics (Top of Report)

| Metric | Value |
|--------|-------|
| Report Date | <TODAY> |
| Fiscal Quarter | <CURRENT_FQ> (FY starts Feb 1) |
| Total Accounts | <COUNT> |
| Total Active UCOs | <COUNT> |
| UCO Health | <RED_COUNT> Red / <YELLOW_COUNT> Yellow / <GREEN_COUNT> Green |
| Total Pipeline ARR | $<SUM(estimated_quarterly_dbus * 4)> for U1-U4 |
| Bandwidth Utilization | <ASSIGNED_FTE> FTE / <CAPACITY_FLAG> |
| Action Items | <HIGH_COUNT> High / <MEDIUM_COUNT> Medium / <LOW_COUNT> Low |

### Per-Account Blocks

For each account, include:
- Account name and DSA tier
- Assignment details (hours, FTE, dates)
- UCO summary (count by stage, health breakdown)
- Consumption trend (up/down/flat with percentage)
- Top action items for this account

---

## Step 5: Optional UCO Updates

After presenting the status update, offer to update UCOs:

> "I found <N> UCOs that may need updates. Would you like me to run `/uco-updates` to review and update them?"

If the user consents:
1. Load the `uco-updates` skill
2. Present the list of UCOs needing updates (Red health, stale, missing Next Steps)
3. For each UCO, help the user draft and apply updates

**Important:** Never auto-update UCOs without explicit user consent. The status update is read-only by default.

---

## Step 6: Output

### Console Output (Default)

Render the status update directly in the terminal using the template format. Use markdown tables, clear section headers, and color indicators.

### Google Doc Output (Optional)

If the user requests a Google Doc:

1. Save the markdown to a temp file:
```bash
cat > /tmp/dsa_status_update.md << 'CONTENT'
[Status update markdown content]
CONTENT
```

2. Convert to Google Doc:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/dsa_status_update.md \
  --title "DSA Status Update - <DSA_NAME> - <DATE>"
```

3. Post-process for status colors (Green/Yellow/Red).

Return the Google Doc URL to the user.

---

## Example Invocations

| Prompt | What Happens |
|--------|-------------|
| "DSA status update" | Full status across all assigned accounts |
| "Weekly status" | Same as above |
| "Status update, output as Google Doc" | Status saved to Google Doc |
| "DSA check-in" | Status with emphasis on action items |
| "Weekly review for my accounts" | Full status with optional UCO updates |

---

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/dsa-account-prep` | Deep-dive into a single account before a meeting |
| `/dsa-weekly-report` | Comprehensive weekly activity report with change detection |
| `/uco-updates` | Update UCO fields (Next Steps, health, stage, dates) |
| `/dsa-handoff` | Transitioning an account to a new DSA |
| `/logfood-querier` | Ad-hoc Logfood queries |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| No accounts found | Check AccountTeamMember role is 'DSA'; verify SF user email matches |
| Empty assignment data | Logfood DSA tables use display names; ensure name matches exactly |
| Consumption data stale | This table uses `date` ranges, not snapshots; verify `date` filter covers the expected period and check logfood auth |
| Bandwidth shows 0 | The dsa_bandwidth_table regex extracts from HTML; verify DSA name match |
