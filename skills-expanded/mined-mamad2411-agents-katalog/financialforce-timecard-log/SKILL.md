---
name: financialforce-timecard-log
description: Log weekly timecards in Salesforce PSA. Use when the user wants to log time, check available timecodes, create timecards, or fill in their weekly timesheet.
---

# Salesforce Timecard Skill

Guides the user through logging weekly time in Salesforce PSA
(pse__Timecard_Header__c). Discovers available timecodes from recent history,
collects hours, creates saved (not submitted) timecards.

## Key Facts

- Timecards live on `pse__Timecard_Header__c` — one record per project per week
- Weekly hours are stored as day fields directly on the header
  (`pse__Monday_Hours__c` ... `pse__Friday_Hours__c`)
- Weeks **must** run Sunday -> Saturday or Salesforce rejects/deletes the record
- Status `Saved` = draft; Status `Submitted` = submitted for approval
- Each timecard needs: OwnerId, pse__Resource__c, pse__Project__c,
  pse__Assignment__c
- **Never pipe `sf data query --json` to `jq` without a null guard.** Use
  `.result.records // [] | .[]` not `.result.records[]` — if sf returns an
  error or empty result, `.result.records` is `null` and `null[]` throws.
- For display/verify steps, prefer plain `sf data query` (no `--json`) — the
  CLI renders a clean table natively with no parsing needed.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.

## Workflow

### Phase 1: Authenticate

Run `sf org display` and check `Connected Status`. If not Connected, run:
```bash
sf org login web --instance-url=https://databricks.my.salesforce.com/ --set-default
```

**IMPORTANT: Always use `--target-org` on every `sf` CLI command.** Resolve the org username once at session start and reuse:

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
```

Append `--target-org "$SF_TARGET_ORG"` to every `sf` command.

### Phase 2: Resolve the Current User

Look up the current user's Salesforce User ID using the username from `sf org display`:

```bash
sf data query --query "SELECT Id FROM User WHERE Username = '<username>'" --target-org "$SF_TARGET_ORG"
```

Then get the Resource ID from the most recent timecard header:
```bash
sf data query --query "SELECT pse__Resource__c FROM pse__Timecard_Header__c WHERE OwnerId = '<user-id>' ORDER BY pse__Start_Date__c DESC LIMIT 1" --target-org "$SF_TARGET_ORG"
```

Use plain `sf data query` output (no `--json`) — the CLI renders a readable table natively.

### Phase 3: Discover Available Timecodes

Pull distinct projects + assignments from the user's last ~8 weeks of approved
timecards. Deduplicate by `pse__Project__c` and present as a numbered list.

```bash
sf data query --query "SELECT pse__Project__r.Name, pse__Project__c, pse__Assignment__r.Name, pse__Assignment__c FROM pse__Timecard_Header__c WHERE OwnerId = '<user-id>' AND pse__Status__c = 'Approved' ORDER BY pse__Start_Date__c DESC LIMIT 20" --target-org "$SF_TARGET_ORG"
```

Present to the user like:
```
Available timecodes:
1. Optiver - RSA (Trading) Extension - RSA/Con/PM
2. PS - Internal Enablement
3. PS - Admin (Brickster Only)
```

### Phase 4: Collect Hours from User

Ask the user:
1. **Which week?** Default to the current week.
2. **For each timecode:** which days and how many hours?

Compute the correct Sun-Sat boundaries. The start date must be a Sunday and
end date a Saturday. Given any date in the week, derive Sunday as:
```python
from datetime import date, timedelta
d = date.today()
sunday = d - timedelta(days=(d.weekday() + 1) % 7)
saturday = sunday + timedelta(days=6)
```

### Phase 5: Create Timecard Headers

Create one `pse__Timecard_Header__c` per distinct project. Pass `0` for days
with no hours (not blank).

```bash
sf data create record --sobject pse__Timecard_Header__c --values \
  "pse__Start_Date__c=<YYYY-MM-DD> \
   pse__End_Date__c=<YYYY-MM-DD> \
   pse__Status__c=Saved \
   OwnerId=<user-id> \
   pse__Resource__c=<resource-id> \
   pse__Project__c=<project-id> \
   pse__Assignment__c=<assignment-id> \
   pse__Monday_Hours__c=0 \
   pse__Tuesday_Hours__c=<h> \
   pse__Wednesday_Hours__c=<h> \
   pse__Thursday_Hours__c=<h> \
   pse__Friday_Hours__c=<h>" \
  --target-org "$SF_TARGET_ORG"
```

### Phase 6: Verify and Display

Query back the created records to confirm. Use plain `sf data query` **without**
`--json` — the CLI renders a table natively and avoids jq null-safety pitfalls:

```bash
sf data query --query "SELECT Name, pse__Project__r.Name, pse__Start_Date__c, pse__End_Date__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c, pse__Total_Hours__c, pse__Status__c FROM pse__Timecard_Header__c WHERE Id IN ('<id1>', '<id2>')" --target-org "$SF_TARGET_ORG"
```

If you must parse JSON output (e.g. to extract a field), always guard the
array: `jq '.result.records // [] | .[] | .FieldName'`

Display format:
```
Week: Sun 1 Mar - Sat 7 Mar 2026

| Timecode                     | Mon | Tue | Wed | Thu | Fri | Total | Status |
|------------------------------|-----|-----|-----|-----|-----|-------|--------|
| Optiver - RSA Trading Ext.   |  -  |  -  |  -  |  -  | 8h  |   8h  | Saved  |
| PS - Internal Enablement     |  -  | 8h  | 8h  | 8h  |  -  |  24h  | Saved  |

Total: 32h - Saved (not submitted)
```

Remind the user to submit in the FinancialForce UI when ready (programmatic submission is not safe — see Phase 7).

### Phase 7: Submit Timecards

**Do NOT submit timecards programmatically.** Direct field updates (`pse__Status__c='Submitted'`) and `Approval.ProcessSubmitRequest` both fail to trigger the FinancialForce PSA submission workflow correctly. Direct field updates bypass the `ProcessInstance` approval chain, which means `pse__Include_In_Financials__c` never gets set to `true` on approval — and **hours won't count toward revenue**.

Instead, after creating timecards, instruct the user:

> "Your timecards are saved. Please submit them through the FinancialForce Time Entry UI to ensure they enter the proper approval workflow. This is the only safe submission path that guarantees hours count toward revenue."

Provide a direct link to the FinancialForce time entry page if possible:
`https://databricks.lightning.force.com/lightning/n/pse__Timecard_Entry`

## Error Handling

- **"must specify a Project"** — `pse__Project__c` is required; always set it.
- **ENTITY_IS_DELETED after create** — week dates were not Sun-Sat. Recheck
  date boundaries and recreate with corrected dates.
- **No timecodes found** — user has no approved timecards in recent history.
  Ask them to provide a project name and search `pse__Project__c` directly.
- **`jq: Cannot iterate over null`** — `sf data query --json` returned an
  error or empty result so `.result.records` is `null`. Fix: use
  `.result.records // [] | .[]` in jq, or drop `--json` and use the plain
  table output instead.

## Important Notes

- **Do not** use `--use-tooling-api` flag.
- **SOQL operators:** Use `!=` or `<>` for not-equal comparisons. **Never** backslash-escape operators (e.g., `\!=` will cause a parse error).
- **No multi-hop relationships:** SOQL on FinancialForce objects does not support chained relationship traversals like `pse__Assignment__r.pse__Project__r.Name`. Query each object separately and join by ID in your logic.
- Timecards are created with `Status = Saved` — they are **not submitted** until the user explicitly asks.
- Record IDs are 18-character Salesforce IDs.
- The Salesforce link format is: `https://databricks.lightning.force.com/lightning/r/pse__Timecard_Header__c/<id>/view`

## Salesforce Objects Reference

| Object | API Name | Purpose |
|--------|----------|---------|
| Timecard Header | `pse__Timecard_Header__c` | Weekly timecard per assignment |
| Contact | `Contact` | Resource record (FinancialForce resources are Contacts) |
| User | `User` | Owner/current user record |
| Project | `pse__Proj__c` | Project time is logged against |
| Assignment | `pse__Assignment__c` | Links resource to project |

## Key Fields (`pse__Timecard_Header__c`)

| Field | API Name | Notes |
|-------|----------|-------|
| Status | `pse__Status__c` | Saved or Submitted |
| Owner | `OwnerId` | Salesforce User ID |
| Resource | `pse__Resource__c` | Contact ID of the resource |
| Project | `pse__Project__c` | Project ID |
| Assignment | `pse__Assignment__c` | Assignment ID |
| Week Start | `pse__Start_Date__c` | Must be a Sunday |
| Week End | `pse__End_Date__c` | Must be a Saturday |
| Monday Hours | `pse__Monday_Hours__c` | Hours for Monday |
| Tuesday Hours | `pse__Tuesday_Hours__c` | Hours for Tuesday |
| Wednesday Hours | `pse__Wednesday_Hours__c` | Hours for Wednesday |
| Thursday Hours | `pse__Thursday_Hours__c` | Hours for Thursday |
| Friday Hours | `pse__Friday_Hours__c` | Hours for Friday |
| Total Hours | `pse__Total_Hours__c` | Auto-calculated weekly total |
