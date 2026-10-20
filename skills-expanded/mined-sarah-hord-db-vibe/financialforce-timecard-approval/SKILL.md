---
name: financialforce-timecard-approval
description: View and approve/reject FinancialForce/Certinia timecards (pse__Timecard_Header__c) as a manager. Use when the user asks to approve timecards, review submitted time, check pending approvals, reject a timecard, or manage timecard approvals in FinancialForce. Shows a weekly grid of submitted timecards grouped by resource and project with financial context.
---

# FinancialForce Timecard Approval

View, approve, and reject submitted timecards (`pse__Timecard_Header__c`) as a manager/approver in Salesforce/FinancialForce. Includes financial context (budget, bookings, billings, scheduled hours) to support approval decisions.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.

## Week Boundaries

FinancialForce uses **Sunday–Saturday** weeks. To determine the current week:

1. Find today's day of week
2. **Week start** = most recent Sunday (or today if Sunday)
3. **Week end** = week start + 6 days (Saturday)
4. Use `YYYY-MM-DD` format for all SOQL date filters

The user may say "this week", "last week", or give a specific date. Always resolve to the correct Sunday–Saturday range.

## Timecard Statuses

| Status | Meaning |
|--------|---------|
| `Saved` | Draft, not yet submitted (not visible to approvers) |
| `Submitted` | Awaiting manager approval |
| `Pending Approval` | In an approval workflow |
| `Approved` | Manager has approved |
| `Rejected` | Manager has rejected, returned to resource |

## Workflow

### Step 1 — Identify the Approver

Look up the current user's Salesforce User ID:

```bash
sf data query \
  --query "SELECT Id, Name, Email FROM User WHERE Email = '<user_email>'" \
  --target-org <alias>
```

The `pse__Approver__c` field on timecards stores the User ID of the designated approver.

### Step 2 — Query Timecards with Financial Fields

Query timecards including the fields needed for financial context:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Resource__r.Name, pse__Project__r.Name, pse__Project__c, \
      pse__Status__c, pse__Start_Date__c, \
      pse__Sunday_Hours__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, \
      pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c, \
      pse__Saturday_Hours__c, pse__Total_Hours__c, \
      pse__Total_Billable_Amount__c, pse__Total_Cost__c, \
      pse__Bill_Rate__c, pse__Cost_Rate_Amount__c, pse__Billable__c, \
      pse__Assignment__r.pse__Schedule__c \
    FROM pse__Timecard_Header__c \
    WHERE pse__Approver__c = '<approver_user_id>' \
      AND pse__Status__c IN ('Submitted', 'Approved') \
      AND pse__Start_Date__c = <week_start> \
    ORDER BY pse__Status__c DESC, pse__Resource__r.Name, pse__Project__r.Name" \
  --target-org <alias>
```

### Step 3 — Query Scheduled Hours

Get schedule exceptions for comparison. Collect all unique `pse__Schedule__c` IDs from the timecards, then:

```bash
sf data query \
  --query "SELECT Id, pse__Schedule__c, pse__Date__c, \
      pse__Sunday_Hours__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, \
      pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c, \
      pse__Saturday_Hours__c \
    FROM pse__Schedule_Exception__c \
    WHERE pse__Schedule__c IN ('<schedule_id_1>','<schedule_id_2>',...) \
      AND pse__Date__c >= <week_start_minus_7> \
      AND pse__Date__c <= <week_end> \
    ORDER BY pse__Schedule__c, pse__Date__c DESC" \
  --target-org <alias>
```

For each schedule, use the most recent exception on or before the week end. Sum the daily hours to get weekly scheduled hours.

### Step 4 — Query Project Financials

Collect unique project IDs from the timecards, then query project-level data:

#### Project Bookings & Billings

```bash
sf data query \
  --query "SELECT Id, Name, pse__Bookings__c, pse__Billings__c, pse__Billing_Type__c \
    FROM pse__Proj__c \
    WHERE Id IN ('<project_id_1>','<project_id_2>',...)" \
  --target-org <alias>
```

#### Project Budgets

```bash
sf data query \
  --query "SELECT pse__Project__c, SUM(pse__Amount__c) budget \
    FROM pse__Budget__c \
    WHERE pse__Project__c IN ('<project_id_1>','<project_id_2>',...) \
      AND pse__Status__c = 'Approved' \
    GROUP BY pse__Project__c" \
  --target-org <alias>
```

### Step 5 — Display the Approval Grid

Present two tables: the timecard detail grid, then the project financial summary.

```
**Timecard Approvals — <Approver Name>**
**Week: Sun <M/D> – Sat <M/D/YYYY>**

**Pending Approval (<count>)**

| # | Resource | Project | Total | Sched | Diff | Billable $ | Cost $ | Rec |
|---|----------|---------|-------|-------|------|------------|--------|-----|
| 1 | <Name> | <Project> | 40 | 40 | **0** | $7,040 | $0 | **Approve** |
| 2 | <Name> | <Project> | 36 | 32 | +4 | $3,802 | $0 | Hours ≠ Schedule |
| 3 | <Name> | <Project> | 8 | — | — | $0 | $1,760 | Approve |

**Total pending: XX hrs across N timecards | Billable: $XX | Cost: $XX**

---

**Already Approved (<count>)**

| # | Resource | Project | Total | Sched | Diff | Billable $ | Cost $ |
|---|----------|---------|-------|-------|------|------------|--------|
| 1 | <Name> | <Project> | 5 | 5 | **0** | $880 | $0 |

**Total approved: XX hrs | Billable: $XX**

---

**Project Financial Summary**

| Project | Budget | Bookings | Billings | Billing Type | If Approved |
|---------|--------|----------|----------|-------------|-------------|
| <Project> | $16,896 | $16,896 | $3,520 | 100% Paid Upfront | $4,400 |
| <Project> | $601,973 | $601,973 | $175,059 | Ratable | $175,059 |
```

#### Display Rules

- Group by **Pending Approval** first, then **Already Approved**
- Number rows sequentially within each group for easy reference
- Sort by resource name, then project name
- **Sched** = weekly scheduled hours from `pse__Schedule_Exception__c` (show `—` if no schedule data)
- **Diff** = Total - Sched (bold **0** when matching, show `+N` or `-N` when different)
- **Billable $** = `pse__Total_Billable_Amount__c` from timecard (or `pse__Bill_Rate__c × total_hours`)
- **Cost $** = `pse__Total_Cost__c` from timecard (or `pse__Cost_Rate_Amount__c × total_hours`)
- **If Approved** = current `pse__Billings__c` + sum of `pse__Total_Billable_Amount__c` for all pending timecards on that project
- When showing all weeks, add a **Week** column before Resource

#### Recommendation Logic

| Condition | Recommendation |
|-----------|---------------|
| Hours match schedule (diff = 0 or within 10%) | **Approve** |
| Hours differ from schedule by > 10% | **Hours ≠ Schedule** |
| No schedule data, non-billable internal project | Approve |
| No schedule data, billable or high cost | Review |

### Step 6 — Prompt for Action

After displaying the grid, prompt the approver:

> *"You have N timecards pending approval (XX total hours, $XX billable). Would you like to:*
> 1. *Approve all pending timecards for this week*
> 2. *Approve all for a specific resource (e.g., "approve all for Akshay")*
> 3. *Approve specific entries by number (e.g., "approve #1, #3, #5")*
> 4. *Reject specific entries (e.g., "reject #2 — reason: hours exceed schedule")*"

## Approving Timecards

To approve a single timecard:

```bash
sf data update record \
  --sobject pse__Timecard_Header__c \
  --record-id <header_id> \
  --values "pse__Status__c='Approved' pse__Approved__c=true" \
  --target-org <alias>
```

### Batch Approval

To approve multiple timecards, run the update command for each one sequentially. After all updates, re-query to verify.

**Always confirm before batch approving.** Example confirmation:

> *"I'll approve 5 timecards for Akshay Sharma (weeks of 2/1 through 3/1, totaling 45 hours, $7,920 billable). Proceed?"*

### Approve All for a Week

When the user says "approve all":
1. Query all Submitted timecards for the week where `pse__Approver__c` matches
2. Show a summary: N timecards, total hours, total billable, resources affected
3. Confirm with the user
4. Execute updates one at a time
5. Show final status

### Approve All for a Resource

When the user says "approve all for [name]":
1. Query all Submitted timecards for that resource where `pse__Approver__c` matches
2. Optionally filter to a specific week if mentioned
3. Confirm and execute

## Rejecting Timecards

To reject a timecard:

```bash
sf data update record \
  --sobject pse__Timecard_Header__c \
  --record-id <header_id> \
  --values "pse__Status__c='Rejected'" \
  --target-org <alias>
```

**Always ask for a rejection reason.** The reason should be communicated to the resource (via Slack, email, or as a note).

After rejection, the resource's timecard returns to an editable state so they can correct and resubmit.

## Common User Requests

| Request | Action |
|---------|--------|
| "Show my pending approvals" | Query Submitted timecards for this approver |
| "Show approvals for this week" | Filter by current week, show Submitted + Approved with financials |
| "Approve all" | Batch approve all Submitted timecards for the specified week |
| "Approve all for [name]" | Approve all timecards for a specific resource |
| "Approve #1, #3" | Approve specific numbered entries from the grid |
| "Reject #2" | Reject a specific timecard, ask for reason |
| "Show all outstanding" | Query all Submitted timecards across all weeks |
| "How many timecards are pending?" | Count query grouped by resource |

## Salesforce Objects Reference

| Object | API Name | Purpose |
|--------|----------|---------|
| Timecard Header | `pse__Timecard_Header__c` | Weekly timecard per assignment |
| Contact | `Contact` | Resource record (FinancialForce resources are Contacts) |
| User | `User` | Approver record |
| Project | `pse__Proj__c` | Project with bookings/billings/billing type |
| Budget | `pse__Budget__c` | Project budget (amount in hours or dollars) |
| Schedule Exception | `pse__Schedule_Exception__c` | Weekly scheduled hours per assignment |

## Key Fields

### Timecard Header (`pse__Timecard_Header__c`)

| Field | API Name | Notes |
|-------|----------|-------|
| Status | `pse__Status__c` | Submitted → Approved or Rejected |
| Approved | `pse__Approved__c` | Set to `true` when approving |
| Approver | `pse__Approver__c` | User ID of designated approver |
| Resource | `pse__Resource__r.Name` | Person who logged time |
| Project | `pse__Project__r.Name` | Project time was logged against |
| Project ID | `pse__Project__c` | For joining to project/budget data |
| Week Start | `pse__Start_Date__c` | Always a Sunday |
| Daily Hours | `pse__Sunday_Hours__c` – `pse__Saturday_Hours__c` | Hours per day |
| Total Hours | `pse__Total_Hours__c` | Auto-calculated weekly total |
| Bill Rate | `pse__Bill_Rate__c` | Per-hour bill rate |
| Cost Rate | `pse__Cost_Rate_Amount__c` | Per-hour cost rate |
| Billable Amount | `pse__Total_Billable_Amount__c` | Total billable for this timecard |
| Cost Amount | `pse__Total_Cost__c` | Total cost for this timecard |
| Billable | `pse__Billable__c` | Whether timecard is billable |
| Schedule | `pse__Assignment__r.pse__Schedule__c` | Schedule ID for exception lookup |

### Project (`pse__Proj__c`)

| Field | API Name | Notes |
|-------|----------|-------|
| Bookings | `pse__Bookings__c` | Total project bookings |
| Billings | `pse__Billings__c` | Total project billings to date |
| Billing Type | `pse__Billing_Type__c` | Ratable, Carve, 100% Paid Upfront, Time and Materials |

### Budget (`pse__Budget__c`)

| Field | API Name | Notes |
|-------|----------|-------|
| Amount | `pse__Amount__c` | Budget amount (hours or dollars) |
| Status | `pse__Status__c` | Filter to Approved budgets |
| Project | `pse__Project__c` | Link to parent project |

## Important Notes

- **Do not** use `--use-tooling-api` flag.
- **Only the designated approver** should approve timecards — the `pse__Approver__c` field determines who can approve.
- **Always confirm before approving or rejecting** — show the grid with financial context and get explicit confirmation.
- **Rejection requires a reason** — always ask the user why they're rejecting so the resource knows what to fix.
- **Week boundaries are Sunday–Saturday** — the `pse__Start_Date__c` on timecards is always a Sunday.
- **"If Approved" billings** = current `pse__Billings__c` + sum of `pse__Total_Billable_Amount__c` for pending timecards on that project.
- Record IDs are 18-character Salesforce IDs.
- The Salesforce link format is: `https://databricks.lightning.force.com/lightning/r/pse__Timecard_Header__c/<id>/view`
