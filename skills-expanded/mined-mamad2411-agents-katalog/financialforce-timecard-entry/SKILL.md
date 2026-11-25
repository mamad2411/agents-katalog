---
name: financialforce-timecard-entry
description: View, fill, and manage FinancialForce/Certinia timecards (pse__Timecard_Header__c). Use when the user asks to view their timecard, log hours, fill time, check time entry, submit timecards, or manage weekly time in FinancialForce. Supports viewing scheduled vs actual hours, creating new timecards, updating existing ones, and submitting for approval.
---

# FinancialForce Time Entry

View, create, update, and submit weekly timecards (`pse__Timecard_Header__c`) in Salesforce/FinancialForce. Mimics the FinancialForce Time Entry UI with a grid of assignments × days.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.

## Week Boundaries

FinancialForce uses **Sunday–Saturday** weeks. To determine the current week:

1. Find today's day of week
2. **Week start** = most recent Sunday (or today if Sunday)
3. **Week end** = week start + 6 days (Saturday)
4. Use `YYYY-MM-DD` format for all SOQL date filters

The user may say "this week", "last week", "next week", or give a specific date. Always resolve to the correct Sunday–Saturday range.

## Workflow

### Step 1 — Identify the Resource

The user is typically entering time for themselves. Look up the resource by name on the **Contact** object (FinancialForce resources are Contacts, not Users):

```bash
sf data query \
  --query "SELECT Id, Name FROM Contact WHERE Name = '<full_name>'" \
  --target-org <alias>
```

If the user's name isn't known, search by email on the User object first, then match to Contact:
```bash
sf data query \
  --query "SELECT Id, Name, Email FROM User WHERE Email = '<email>'" \
  --target-org <alias>
```

### Step 2 — Get Active Assignments

Query assignments that are active for the target week. Filter by date range to exclude stale/future assignments:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Resource__r.Name, pse__Project__r.Name, pse__Project__c, pse__Schedule__c, pse__Start_Date__c, pse__End_Date__c \
    FROM pse__Assignment__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__End_Date__c >= <week_start> \
      AND pse__Start_Date__c <= <week_end> \
      AND pse__Closed_for_Time_Entry__c = false \
    ORDER BY pse__Project__r.Name" \
  --target-org <alias>
```

### Step 3 — Get Scheduled Hours (REQUIRED)

**You MUST always query scheduled hours before displaying the grid.** Do NOT skip this step. Scheduled hours come from `pse__Schedule_Exception__c` records linked to each assignment's `pse__Schedule__c`. Query for exceptions that cover the target week:

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

For each schedule, use the **most recent** exception whose `pse__Date__c` is on or before the week end. The day-of-week fields (`pse__Monday_Hours__c`, etc.) give the scheduled hours per day.

If no exception exists, fall back to the base `pse__Schedule__c` record's day fields (often all zeros for non-scheduled time).

### Step 4 — Get Existing Timecards

Query existing timecard headers for the week:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Project__r.Name, pse__Assignment__r.Name, pse__Assignment__c, \
      pse__Status__c, pse__Sunday_Hours__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, \
      pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c, \
      pse__Saturday_Hours__c, pse__Total_Hours__c \
    FROM pse__Timecard_Header__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__Start_Date__c = <week_start> \
    ORDER BY pse__Project__r.Name" \
  --target-org <alias>
```

### Step 5 — Display the Time Entry Grid

**CRITICAL: You MUST always show BOTH the *Sched* row AND the **Actual** row for every project. Never omit the Sched row, even if scheduled hours are all zeros.** The two-row format is the core UI of this skill.

Present a two-row-per-project grid with *scheduled* hours in italics and **actual** hours in bold:

```
**Time Entry — <Resource Name>**
**Week: Sun <M/D> – Sat <M/D/YYYY>**

| # | Project | | Sun | Mon | Tue | Wed | Thu | Fri | Sat | Total | Status |
|---|---------|--|-----|-----|-----|-----|-----|-----|-----|-------|--------|
| 1 | <Project Name> | *Sched* | *0* | *1* | *1* | *1* | *1* | *1* | *0* | *5* | |
| | | **Actual** | **0** | **1** | **1** | **1** | **1** | **1** | **0** | **5** | Approved |
| 2 | <Project Name> | *Sched* | *0* | *0* | *8* | *8* | *8* | *0* | *0* | *24* | |
| | | **Actual** | **—** | **—** | **—** | **—** | **—** | **—** | **—** | **0** | *No timecard* |

*Scheduled: XX hrs* | **Actual: XX hrs** | **Remaining: XX hrs**
```

Display rules:
- **ALWAYS show two rows per project**: the `*Sched*` row (italics) and the `**Actual**` row (bold). Never collapse to a single row.
- If the schedule query returned no exceptions, show `*0*` for all days in the Sched row — do NOT omit the row.
- Use `**—**` for days with no timecard (vs `**0**` when a timecard exists with zero hours)
- Show status from the timecard header: Saved, Submitted, Approved
- Show `*No timecard*` in italics when no header exists for that assignment
- Always show the totals summary line at the bottom

## Creating a Timecard

When the user wants to log hours on a project that has no existing timecard for the week:

```bash
sf data create record \
  --sobject pse__Timecard_Header__c \
  --values "pse__Resource__c='<contact_id>' \
    pse__Assignment__c='<assignment_id>' \
    pse__Project__c='<project_id>' \
    pse__Start_Date__c='<week_start>' \
    pse__End_Date__c='<week_end>' \
    pse__Sunday_Hours__c=<hrs> \
    pse__Monday_Hours__c=<hrs> \
    pse__Tuesday_Hours__c=<hrs> \
    pse__Wednesday_Hours__c=<hrs> \
    pse__Thursday_Hours__c=<hrs> \
    pse__Friday_Hours__c=<hrs> \
    pse__Saturday_Hours__c=<hrs> \
    pse__Status__c='Saved'" \
  --target-org <alias>
```

Key behaviors:
- Setting daily hours on the header at creation time works — the detail record (`pse__Timecard__c`) is **auto-generated** and inherits the hours
- `pse__Total_Hours__c` is auto-calculated on both header and detail
- No separate update to the detail record is needed after creation
- `pse__Start_Date__c` must be the **Sunday** and `pse__End_Date__c` must be the **Saturday**

## Updating a Timecard

When modifying hours on an existing timecard:

```bash
sf data update record \
  --sobject pse__Timecard_Header__c \
  --record-id <header_id> \
  --values "pse__<Day>_Hours__c=<new_hours>" \
  --target-org <alias>
```

Only update the specific day fields that changed. The total recalculates automatically.

**Important:** Only timecards in `Saved` status can be updated. If status is `Submitted` or `Approved`, inform the user it must be recalled first.

## Deleting a Timecard

When removing a timecard entirely, delete the **detail first**, then the header:

```bash
# 1. Find the detail record
sf data query \
  --query "SELECT Id FROM pse__Timecard__c WHERE pse__Timecard_Header__c = '<header_id>'" \
  --target-org <alias>

# 2. Delete detail
sf data delete record \
  --sobject pse__Timecard__c \
  --record-id <detail_id> \
  --target-org <alias>

# 3. Delete header
sf data delete record \
  --sobject pse__Timecard_Header__c \
  --record-id <header_id> \
  --target-org <alias>
```

## Submitting Timecards

**Do NOT submit timecards programmatically.** Direct field updates (`pse__Status__c='Submitted'`) and `Approval.ProcessSubmitRequest` both fail to trigger the FinancialForce PSA submission workflow correctly. Direct field updates bypass the `ProcessInstance` approval chain, which means `pse__Include_In_Financials__c` never gets set to `true` on approval — and **hours won't count toward revenue**.

Instead, after creating or updating timecards, instruct the user:

> "Your timecards are saved. Please submit them through the FinancialForce Time Entry UI to ensure they enter the proper approval workflow. This is the only safe submission path that guarantees hours count toward revenue."

Provide a direct link: `https://databricks.lightning.force.com/lightning/n/pse__Timecard_Entry`

## After Displaying the Grid

After showing the timecard grid, offer the user navigation and help options:

> *"You can:*
> - *Change the week — "show last week", "show week of 3/2", "show next week"*
> - *Log time — "log 8 hours Mon-Fri on Admin", "fill to schedule"*
> - *Need help? — "where should I log my time?", "what projects can I use?"*
> - *Submit — "submit my timecard" (will direct you to the FinancialForce UI)*"

## Helping Users Find the Right Project

### "Where should I log my time?" / "What projects can I use?"

When the user asks for help finding the right time code, show their active assignments with full context:

```bash
sf data query \
  --query "SELECT Id, pse__Project__r.Name, pse__Project__r.pse__Project_Type__c, \
      pse__Project__r.pse__Billing_Type__c, pse__Project__r.pse__Stage__c, \
      pse__Project__r.Description, pse__Project__r.pse__Account__r.Name, \
      pse__Start_Date__c, pse__End_Date__c \
    FROM pse__Assignment__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__End_Date__c >= <week_start> \
      AND pse__Start_Date__c <= <week_end> \
      AND pse__Closed_for_Time_Entry__c = false \
    ORDER BY pse__Project__r.pse__Project_Type__c, pse__Project__r.Name" \
  --target-org <alias>
```

Display as a categorized list:

```
**Your Active Assignments — Week of <M/D>**

**Internal Projects**
| # | Project | Type | Description |
|---|---------|------|-------------|
| 1 | PS - Admin (Brickster Only) | Admin | General admin, meetings, email, internal work |
| 2 | PS - Time Off | PTO | Vacation, sick leave, personal days |
| 3 | PS - Project Manager (Brickster Only) | PM | PM-specific internal work |

**Customer Projects**
| # | Project | Account | Billing Type | Stage |
|---|---------|---------|-------------|-------|
| 4 | Amgen - PS&T CDH RSA | Amgen | 100% Paid Upfront | In Progress |
| 5 | CareSource Archival - Drawdown | CareSource | 100% Paid Upfront | In Progress |

*Say a number or project name to log time, e.g. "log 8 hours to #4 on Monday"*
```

### Fuzzy Project Matching

When the user gives a partial or vague project name (e.g., "log time to admin", "put hours on Amgen"), search their assignments using `LIKE`:

```bash
sf data query \
  --query "SELECT Id, pse__Project__r.Name, pse__Project__c, pse__Project__r.pse__Project_Type__c \
    FROM pse__Assignment__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__Project__r.Name LIKE '%<keyword>%' \
      AND pse__End_Date__c >= <week_start> \
      AND pse__Start_Date__c <= <week_end> \
      AND pse__Closed_for_Time_Entry__c = false" \
  --target-org <alias>
```

- If **one match** → proceed with that project
- If **multiple matches** → show them and ask which one
- If **no matches** → try broader search, then fall back to the recent history or "no assignment" flow

### Smart Suggestions from Recent History

When the user is unsure where to log time, query their last 4 weeks of timecards to show what they've been using:

```bash
sf data query \
  --query "SELECT pse__Project__r.Name, pse__Project__r.pse__Project_Type__c, \
      SUM(pse__Total_Hours__c) total_hours, COUNT(Id) weeks_used \
    FROM pse__Timecard_Header__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__Start_Date__c >= <four_weeks_ago_sunday> \
      AND pse__Start_Date__c <= <current_week_start> \
    GROUP BY pse__Project__r.Name, pse__Project__r.pse__Project_Type__c \
    ORDER BY COUNT(Id) DESC, SUM(pse__Total_Hours__c) DESC" \
  --target-org <alias>
```

Display as:

```
**Your Recent Time Entry (last 4 weeks)**

| Project | Type | Weeks Used | Total Hours |
|---------|------|------------|-------------|
| PS - Admin (Brickster Only) | Internal | 4/4 | 10 hrs |
| Amgen - PS&T CDH RSA | Customer | 4/4 | 128 hrs |
| CareSource Archival | Customer | 2/4 | 48 hrs |
| PS - Time Off | Internal | 1/4 | 8 hrs |

*"You've been logging most of your time to Amgen and Admin. Is that still accurate this week?"*
```

### Common Internal Time Codes

When the user asks about internal projects or standard time codes, provide this reference. These are role-specific — each person's assignments will vary, but common ones include:

| Time Code Pattern | Used For |
|-------------------|----------|
| **PS - Admin** | General admin: email, internal meetings, 1:1s, team calls |
| **PS - Time Off** | PTO, vacation, sick days, personal time |
| **PS - Holiday** | Company holidays |
| **PS - Project Manager** | PM-specific internal work (PM role only) |
| **PS - Training** | Formal training, certifications, learning |
| **PS - Enablement** | Internal enablement activities |
| **PS - Presales** | Pre-sales support, scoping, technical validation |
| **[Region] - Management Call** | Regional management meetings |

> **Note:** Not all users have all time codes. The user must have an active assignment to a project to log time against it. Always verify with their actual assignments before suggesting.

### "I Don't Have an Assignment" Flow

When the user wants to log time but no matching assignment exists:

1. Confirm by searching all their active assignments (not just the current week — widen to ±30 days)
2. If truly no match, guide them:

> *"I can't find an assignment matching that project for you. Here's what to do:*
> - **For customer projects:** Contact your Project Manager or PS Ops to get an assignment created
> - **For internal projects:** Reach out to your manager or PS Ops in **#ps-ops-support**
> - **For presales/budgeted util:** Check if a project exists in **#ps-budgeted-util-request** or ask your manager to submit one
>
> *Would you like me to search for the project to confirm it exists?*"

If they say yes, search the project directly:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Project_Type__c, pse__Stage__c, pse__Is_Active__c, \
      pse__Project_Manager__r.Name \
    FROM pse__Proj__c \
    WHERE Name LIKE '%<keyword>%' \
      AND pse__Is_Active__c = true \
    ORDER BY Name LIMIT 10" \
  --target-org <alias>
```

Show the results with the project manager name so the user knows who to contact.

## Common User Requests

| Request | Action |
|---------|--------|
| "Show my timecard" / "View my time" | Steps 1–5: display the grid, then offer navigation + help |
| "Show last week" / "Show week of 3/2" | Re-run steps 2–5 with the specified week |
| "Log 8 hours Mon-Fri on Admin" | Fuzzy match "Admin" → create or update timecard |
| "Fill my time to match schedule" | Create timecards matching scheduled hours for each assignment |
| "Copy last week" | Query previous week's timecards and replicate hours to current week |
| "Submit my timecard" | Direct user to submit in FinancialForce UI (programmatic submission bypasses PSA workflow) |
| "What's my schedule this week?" | Show only the scheduled hours row |
| "Where should I log my time?" | Show categorized assignments with full context |
| "What projects can I use?" | Same as above — show active assignments |
| "What did I log last week?" | Show recent history with hours breakdown |
| "I don't have a time code for X" | Search assignments, then trigger "no assignment" flow if needed |

### Fill to Schedule

When the user asks to fill their time to match the schedule, iterate through each assignment:
1. If no timecard exists, create one with the scheduled hours
2. If a timecard exists in Saved status, update it to match the schedule
3. Skip assignments with Submitted or Approved timecards

### Copy Last Week

1. Query timecards from the previous week (week start - 7 days)
2. For each timecard found, create a new one for the current week with the same daily hours
3. Set status to Saved on all new timecards

## Salesforce Objects Reference

| Object | API Name | Purpose |
|--------|----------|---------|
| Assignment | `pse__Assignment__c` | Links a resource to a project with date range |
| Timecard Header | `pse__Timecard_Header__c` | Weekly timecard per assignment (one row in the grid) |
| Timecard Detail | `pse__Timecard__c` | Auto-generated child of header |
| Schedule | `pse__Schedule__c` | Base schedule pattern for an assignment |
| Schedule Exception | `pse__Schedule_Exception__c` | Weekly overrides to the base schedule |
| Contact | `Contact` | Resource record (FinancialForce resources are Contacts) |

## Important Notes

- **Do not** use `--use-tooling-api` flag.
- **Week boundaries are Sunday–Saturday** — the `pse__Start_Date__c` on timecards is always a Sunday.
- **Resources are Contacts**, not Users. The `pse__Resource__c` field on assignments and timecards points to Contact.
- **Detail records auto-generate** — when you create a `pse__Timecard_Header__c`, FinancialForce automatically creates a matching `pse__Timecard__c`.
- **Only Saved timecards can be edited** — Submitted and Approved timecards are locked.
- **Always confirm before creating or submitting** — show the user the grid with proposed changes before executing.
- Record IDs are 18-character Salesforce IDs.
- The Salesforce link format is: `https://databricks.lightning.force.com/lightning/r/pse__Timecard_Header__c/<id>/view`
