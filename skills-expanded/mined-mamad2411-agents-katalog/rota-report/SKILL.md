---
name: rota-report
description: Generate ROTA activity reports by cross-referencing FinancialForce timecards with Google Calendar events. Resolves fiscal quarters, queries SF timecards, fetches calendar events for logged days, and categorizes activities into ROTA categories (interview prep, conducting interviews, grading, CV review, project scoping). Use when the user wants a ROTA report, ROTA activity summary, or timecard-calendar cross-reference.
user-invocable: true
---

# ROTA Activity Report Generator

This skill produces formatted ROTA activity reports by cross-referencing FinancialForce timecard data with Google Calendar events.

## Accepted Inputs

| Input Type | Example | How It's Used |
|------------|---------|---------------|
| Fiscal quarter + assignment name | `Q1 FY27 SEMEA ROTA` | Resolve dates + fuzzy search assignment |
| Fiscal quarter + SF ID | `Q2 FY27 a0DXXXXXXXXXXXXXXX` | Resolve dates + direct lookup |
| Date range + assignment | `2026-02-01 2026-04-30 ROTA` | Explicit dates + fuzzy search |

## Example Invocations

```
/rota-report Q1 FY27 SEMEA ROTA
/rota-report Q2 FY27 a0DXXXXXXXXXXXXXXX
/rota-report 2026-02-01 2026-04-30 ROTA
```

---

## Activity Categories

Use the following keyword-based mapping to categorize calendar events. Match is case-insensitive. If an event matches multiple categories, use the first match in this table order.

| Category | Keywords |
|----------|----------|
| Interview prep | prep, rota prep, briefing, live coding test - watch |
| Conducting interviews | interview, panel, SME interview |
| Grading & scorecards | scorecard, score card, grading, take home, coding test grading |
| CV review | CV, resume, DPP, validate CV |
| Project scoping | scoping, workshop, urbanisation, architecture workshop |
| Other ROTA | *(any event during logged hours that doesn't match above)* |

---

## Execution Workflow

Follow these steps in order. Do not skip steps.

---

### Step 1: Parse Inputs

Extract from the user's arguments:
- **Assignment identifier**: either a Salesforce ID (starts with `a0D` or similar) or a name/keyword for fuzzy matching
- **Period**: either a fiscal quarter (e.g. "Q1 FY27") or an explicit date range (YYYY-MM-DD to YYYY-MM-DD)

---

### Step 2: Resolve Fiscal Quarter Dates

Databricks fiscal year starts **February 1**. Map quarters as follows:

| Quarter | Start | End |
|---------|-------|-----|
| Q1 FY{YY} | Feb 1, {YY-1} | Apr 30, {YY-1} |
| Q2 FY{YY} | May 1, {YY-1} | Jul 31, {YY-1} |
| Q3 FY{YY} | Aug 1, {YY-1} | Oct 31, {YY-1} |
| Q4 FY{YY} | Nov 1, {YY-1} | Jan 31, {YY} |

**FY year convention**: FY27 means the fiscal year ending Jan 31, 2027. So:
- Q1 FY27 = Feb 1, 2026 – Apr 30, 2026
- Q2 FY27 = May 1, 2026 – Jul 31, 2026
- Q3 FY27 = Aug 1, 2026 – Oct 31, 2026
- Q4 FY27 = Nov 1, 2026 – Jan 31, 2027

If an explicit date range is provided, use those dates directly.

---

### Step 3: Identify Current User and Target Org

First, resolve the Salesforce org alias. Run `sf org list --json` and look for an alias containing "databricks" or marked as the default. If there is exactly one org, use it. If there are multiple orgs and the correct one is ambiguous, list them and ask the user which to use. Store the chosen alias as `TARGET_ORG` — **all subsequent `sf` calls must include `--target-org <TARGET_ORG>`**.

Then get the current Salesforce user:

```bash
sf org display --target-org <TARGET_ORG> --json
```

Extract the `username` field. Then query Salesforce to get the user's record:

```bash
sf data query --target-org <TARGET_ORG> --query "SELECT Id, Name, Email FROM User WHERE Username = '<username>'" --json
```

Store the user's Name and Email for later use.

---

### Step 4: Find Assignment

**If a Salesforce ID was provided:**
```bash
sf data query --target-org <TARGET_ORG> --query "SELECT Id, Name, pse__Project__r.Name, pse__Resource__r.Name, pse__Start_Date__c, pse__End_Date__c FROM pse__Assignment__c WHERE Id = '<id>'" --json
```

**If a name/keyword was provided:**
```bash
sf data query --target-org <TARGET_ORG> --query "SELECT Id, Name, pse__Project__r.Name, pse__Resource__r.Name, pse__Start_Date__c, pse__End_Date__c FROM pse__Assignment__c WHERE Name LIKE '%<keyword>%' AND pse__Resource__r.Name LIKE '%<user_name_fragment>%'" --json
```

If multiple assignments match, present them to the user and ask which one to use.

Store the assignment `Id` and `Name` for the next step.

---

### Step 5: Query Timecards

Query timecard headers for the assignment within the date range:

```bash
sf data query --target-org <TARGET_ORG> --query "SELECT Id, Name, pse__Start_Date__c, pse__End_Date__c, pse__Status__c, pse__Total_Hours__c, pse__Sunday_Hours__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c, pse__Saturday_Hours__c FROM pse__Timecard_Header__c WHERE pse__Assignment__c = '<assignment_id>' AND pse__Start_Date__c >= <start_date> AND pse__End_Date__c <= <end_date> ORDER BY pse__Start_Date__c" --json
```

Parse the results. For each timecard, determine the week start day from the `pse__Start_Date__c` value by checking what day of the week it falls on (use the actual date's weekday). The day-of-week columns map positionally starting from that day:

- If `pse__Start_Date__c` is a **Sunday**: Sun=+0, Mon=+1, Tue=+2, Wed=+3, Thu=+4, Fri=+5, Sat=+6
- If `pse__Start_Date__c` is a **Monday**: Mon=+0, Tue=+1, Wed=+2, Thu=+3, Fri=+4, Sat=+5, Sun=+6

Always verify by computing the weekday of `pse__Start_Date__c` rather than assuming a fixed start day.

Build a list of **all dates with hours > 0** and their hour values.

---

### Step 6: Get Google Calendar Access

Get the user's timezone and an initial access token:

```bash
# Get access token
TOKEN=$(gcloud auth application-default print-access-token)

# Get user timezone
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/calendar/v3/users/me/settings/timezone" | jq -r '.value'
```

Store the timezone for correct event time display.

**Important:** The access token expires after ~1 hour. Since a full quarter can require ~60 API calls, the token must be refreshed during the loop (see Step 7).

---

### Step 7: Fetch Calendar Events for Logged Days

For each day that has hours > 0, fetch calendar events.

**Token management:** Refresh the access token by re-running `gcloud auth application-default print-access-token` at the start of each weekly batch (i.e., before processing each timecard's days). If any API call returns HTTP 401, refresh the token immediately and retry that call once.

**Rate limiting:** Insert a 100ms pause between consecutive Calendar API calls. If any call returns HTTP 429 (rate limit), wait 5 seconds and retry.

```bash
TOKEN=$(gcloud auth application-default print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=<DATE>T00:00:00<TZ_OFFSET>&timeMax=<DATE>T23:59:59<TZ_OFFSET>&singleEvents=true&orderBy=startTime&maxResults=250" | jq '.items[] | {summary, start: .start.dateTime, end: .end.dateTime}'
```

Where `<DATE>` is the specific date (YYYY-MM-DD) and `<TZ_OFFSET>` is the timezone offset (e.g., `+01:00` for CET).

**Pagination:** If the response contains a `nextPageToken`, make additional requests with `&pageToken=<nextPageToken>` until all events for that day are retrieved.

For each event, extract:
- **summary**: the event title
- **start**: start time
- **end**: end time
- **duration**: calculated from start/end

---

### Step 8: Categorize Activities

For each calendar event on a logged day, match the event summary against the category keywords table (from the Activity Categories section above).

Rules:
1. Match is **case-insensitive**
2. Match against the event **summary** field
3. If an event matches multiple categories, use the **first match** in table order
4. Events that don't match any category keyword but fall on a logged day are categorized as **"Other ROTA"**
5. **Exclude** events matching any of these patterns (case-insensitive): `lunch`, `1:1`, `1-1`, `standup`, `stand-up`, `team sync`, `all-hands`, `all hands`, `office hours`, `OOO`, `out of office`, `focus time`, `blocked`, `commute`, `travel`. These are clearly not ROTA activities.
6. If an event is ambiguous (not matching any category keyword and not in the exclude list), include it as "Other ROTA" and flag it in the report output with a `[?]` marker so the user can review.

---

### Step 9: Generate Report

Produce the report in the following format:

#### Header

```
# ROTA Activity Report
**Assignment**: <assignment_name>
**Period**: <start_date> – <end_date> (<quarter label if applicable>)
**Resource**: <user_name>
**Generated**: <today's date>
```

#### Week-by-Week Detail

For each week (grouped by timecard), output a table:

```
## Week of <start_date> — <total_hours>h logged

| Day | Date | Hours | Activities |
|-----|------|-------|------------|
| Mon | 2026-02-02 | 4.0 | [Interview prep] ROTA prep - John Smith (09:00-10:00, 1h) |
| | | | [Conducting interviews] SME Interview - Jane Doe (14:00-15:30, 1.5h) |
| Tue | 2026-02-03 | 8.0 | [Grading & scorecards] Take home grading - Candidate X (10:00-12:00, 2h) |
| | | | [CV review] DPP review - 3 candidates (14:00-16:00, 2h) |
```

#### Category Summary

```
## Category Summary

| Category | Total Hours | Activity Count | Details |
|----------|-------------|----------------|---------|
| Interview prep | 12.0 | 8 | ROTA prep sessions, briefings |
| Conducting interviews | 24.0 | 16 | Panel interviews, SME interviews |
| Grading & scorecards | 8.0 | 6 | Take home grading, scorecard reviews |
| CV review | 4.0 | 3 | DPP reviews, CV validation |
| Project scoping | 0.0 | 0 | — |
| Other ROTA | 2.0 | 2 | Misc ROTA activities |
| **Total** | **50.0** | **35** | |
```

**Note on hours allocation**: The total hours per day come from the timecard — this is the authoritative total and must not be exceeded.
- When multiple events exist on a day, distribute the logged hours proportionally across events based on their calendar duration.
- If calendar event durations total **more** than logged hours, scale all event hours down proportionally so they sum to the logged total. Add a footnote: `* Calendar events exceeded logged hours; scaled proportionally.`
- If calendar event durations total **less** than logged hours, add the difference to "Other ROTA".

#### Grand Total

```
## Grand Total: <total_hours>h across <num_weeks> weeks
```

---

### Step 10: Present to User

Output the full report in markdown format. Ask the user if they want to:
1. Save it to a Google Doc
2. Adjust any categorizations
3. Re-run for a different period or assignment
