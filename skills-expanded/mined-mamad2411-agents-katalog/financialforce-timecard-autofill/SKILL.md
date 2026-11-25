---
name: financialforce-timecard-autofill
description: Fill out weekly FinancialForce PSA timecards automatically from scheduled hours and auto-populate notes from work activity. Use when the user says "fill timesheet", "fill out my timecard", "submit my time", "timesheet", or asks to log weekly hours.
---

# Fill Timesheet

Automate weekly FinancialForce PSA timecard creation with scheduled hours and activity-based notes.

**Requires:** `fe-salesforce-tools` (for `salesforce-authentication`) and `fe-google-tools` (for `google-calendar`, `google-auth`, and `gmail`).

**Preview before writing:** Always show the user a complete preview of hours and notes before creating or updating any timecards (Step 6). Only proceed after explicit confirmation.

## Workflow

### Step 1: Auth + Identity + Target Week

Invoke the `salesforce-authentication` skill, then extract the active org:

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
```

- User email = `$SF_TARGET_ORG` (the username IS the email)
- Target week: default **current week** (Sunday–Saturday). User can pass a date to override.
- Always use `--target-org "$SF_TARGET_ORG"` on every `sf` command

### Step 2: Discover Assignments + Check Target Week

Query assignments:

```bash
sf data query --query "SELECT Id, Name, pse__Project__c, pse__Project__r.Name, pse__Resource__c, pse__Schedule__c, pse__End_Date__c FROM pse__Assignment__c WHERE pse__Resource__r.pse__Salesforce_User__r.Email = '<email>' AND pse__End_Date__c >= <target_week_start>" --target-org "$SF_TARGET_ORG"
```

Check if target week timecards already exist:

```bash
sf data query --query "SELECT Id, pse__Start_Date__c, pse__Status__c, pse__Assignment__c, pse__Assignment__r.Name, pse__Project__c, pse__Project__r.Name, pse__Total_Hours__c FROM pse__Timecard_Header__c WHERE pse__Resource__r.pse__Salesforce_User__r.Email = '<email>' AND pse__Start_Date__c = <target_week_sunday>" --target-org "$SF_TARGET_ORG"
```

If timecards exist, list each with its status (Saved/Submitted/Approved).

- **Approved timecards: NEVER modify.** Do not unlock, update notes, change hours, or re-lock Approved timecards. Unlocking can create lock states that prevent future edits and risks corrupting approval history. Simply display them in the summary as-is and skip them.
- **Saved timecards:** Can be updated directly.
- **Submitted timecards:** Can be recalled, updated, and resubmitted (see Step 6).

### Step 3: Get Scheduled Hours

Get schedule exceptions covering the target week:

```bash
sf data query --query "SELECT pse__Schedule__c, pse__Date__c, pse__End_Date__c, pse__Monday_Hours__c, pse__Tuesday_Hours__c, pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c FROM pse__Schedule_Exception__c WHERE pse__Schedule__c IN ('<sched1>','<sched2>',...) AND pse__Date__c <= <target_week_end> AND pse__End_Date__c >= <target_week_start>" --target-org "$SF_TARGET_ORG"
```

For assignments without a matching exception, fall back to the default schedule:

```bash
sf data query --query "SELECT Id, pse__Monday_Hours__c, pse__Tuesday_Hours__c, pse__Wednesday_Hours__c, pse__Thursday_Hours__c, pse__Friday_Hours__c FROM pse__Schedule__c WHERE Id IN ('<sched_ids>')" --target-org "$SF_TARGET_ORG"
```

Priority: schedule exception > default schedule.

### Step 4: Auto-Fill Shortfall to PS - Admin

Default target: **40 hours/week**. User can override (part-time, PTO). On holiday weeks, verify the target with the user first.

If total scheduled hours < target, add the shortfall:
1. Find the admin assignment (project name containing "PS - Admin", "PSA Admin", or similar). If no match or multiple matches, ask the user.
2. Distribute shortfall hours only across days where the user has scheduled hours > 0. If the schedule shows 0 hours on a day (PTO, holiday), skip that day and divide among the remaining working days.

The shortfall is included in the preview shown in Step 6 — the user confirms the full picture before anything is written.

### Step 5: Gather Work Activity for Notes

Use the **Agent tool** to run 5a–5f **in parallel**, then process with 5g–5h:

#### 5a: Google Calendar
Use `google-calendar` skill to list events for Monday–Friday of target week.

#### 5b: Slack Messages
```
slack_read_api_call("search.messages", {"query": "from:me after:<target_monday> before:<target_saturday>", "sort": "timestamp", "count": 100})
```
`from:me` resolves to the Slack MCP authenticated user, which may differ from the Salesforce user.

#### 5c: Git Commits
```bash
for dir in ~/code ~/repos ~/projects ~/workspace ~/src; do
  [ -d "$dir" ] && find "$dir" -maxdepth 3 -name .git -type d -exec dirname {} \; 2>/dev/null | while read repo; do
    git -C "$repo" log --author="<email>" --after="<target_monday>" --before="<target_next_sunday>" --format="%ad %s [$repo]" --date=short 2>/dev/null
  done
done
```
`--before` is exclusive — use the Sunday after target week. `--author` uses the Salesforce email; if the user's git email differs, they can provide it. If the user has repos outside these directories, they can specify additional paths.

#### 5d: Jira Tickets
```
jira_read_api_call("issues.search", {"jql": "assignee = currentUser() AND updated >= '<target_monday>' AND updated <= '<target_saturday>'", "max_results": 50})
```

#### 5e: Google Drive Documents
Use the `google-auth` skill to authenticate, then search Google Drive for documents the user modified during the target week:

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=modifiedTime+>+'<target_monday>T00:00:00'+and+modifiedTime+<+'<target_saturday>T23:59:59'&fields=files(name,modifiedTime,webViewLink)&pageSize=50&corpora=allDrives&includeItemsFromAllDrives=true&supportsAllDrives=true"
```

This returns both owned and shared files the user modified. The `corpora=allDrives` parameter includes shared drives.

#### 5f: Gmail Sent Emails
Use the `gmail` skill to search for emails sent by the user during the target week:

```
gmail search: from:me after:<target_monday> before:<target_saturday>
```

This captures customer communications, internal follow-ups, meeting recaps, and action item threads. For each email, extract: date, subject line, recipients (to/cc), and a brief snippet. Emails to external domains are strong signals for mapping to customer assignments.

#### 5g: Match Activities to Projects

| Signal | Maps To |
|--------|---------|
| Account/project name in title, channel, doc, or email subject | That assignment |
| External recipient domains in sent emails | Customer assignment |
| External attendee domains | Customer assignment |
| Internal meetings, admin, 1:1s | PS - Admin |
| POD/team meetings, standups | POD Management |
| Unmatched activity | PS - Admin (default) |

**Known limitation:** Matching relies on keyword overlap between activity titles and project/account names. When multiple projects share similar keywords or account names are ambiguous, activities may be mapped to the wrong project. Notes can be manually corrected after the preview.

#### 5h: Generate Notes

Per assignment, per day: concise note (max 255 chars). Generate `pse__Timecard_Notes__c` as a weekly summary. No activity for a day → "Ongoing project support".

### Step 6: Preview + Write Timecards

**Before any writes, show the user a complete preview** of all timecards that will be created or updated — including hours per day, shortfall distribution, and generated notes. Only proceed after the user confirms.

All writes use Apex via `sf apex run --file /dev/stdin --target-org "$SF_TARGET_ORG"`. Apex handles apostrophes and special characters without shell escaping issues.

**IMPORTANT: All timecards created or updated in this step MUST be left in `Saved` status.** Never set `pse__Status__c` to anything other than `'Saved'` and never set `pse__Submitted__c = true` during creation or update. Submission is a separate, optional step handled in Step 7 only after the user explicitly confirms.

#### New timecards:

```apex
pse__Timecard_Header__c tc = new pse__Timecard_Header__c();
tc.pse__Assignment__c = '<assignment_id>';
tc.pse__Project__c = '<project_id>';
tc.pse__Resource__c = '<resource_id>';
tc.pse__Start_Date__c = Date.valueOf('<sunday>');
tc.pse__End_Date__c = Date.valueOf('<saturday>');
tc.pse__Status__c = 'Saved';
tc.pse__Monday_Hours__c = <h>; tc.pse__Tuesday_Hours__c = <h>; tc.pse__Wednesday_Hours__c = <h>;
tc.pse__Thursday_Hours__c = <h>; tc.pse__Friday_Hours__c = <h>;
tc.pse__Monday_Notes__c = '<note>'; tc.pse__Tuesday_Notes__c = '<note>'; tc.pse__Wednesday_Notes__c = '<note>';
tc.pse__Thursday_Notes__c = '<note>'; tc.pse__Friday_Notes__c = '<note>';
tc.pse__Timecard_Notes__c = '<weekly_summary>';
insert tc;
```

Batch multiple inserts using `List<pse__Timecard_Header__c>`.

#### Existing Saved timecards:

```apex
pse__Timecard_Header__c tc = [SELECT Id FROM pse__Timecard_Header__c WHERE Id = '<id>'];
tc.pse__Monday_Notes__c = '<note>'; tc.pse__Tuesday_Notes__c = '<note>'; tc.pse__Wednesday_Notes__c = '<note>';
tc.pse__Thursday_Notes__c = '<note>'; tc.pse__Friday_Notes__c = '<note>';
tc.pse__Timecard_Notes__c = '<weekly_summary>';
update tc;
```

#### Existing Submitted timecards (Recall → Update → Resubmit):

**Confirmation required.** Warn: "These timecards are Submitted and pending approval. Recalling removes them from the approval queue." List each with project name and hours. Only proceed after explicit confirmation.

After recall, the timecard returns to Saved status. Update notes while in Saved status, then **resubmit back to Submitted** to restore the original status. Timecards that were Submitted before must be returned to Submitted after updates.

```apex
// 1. Recall all submitted timecards
List<String> tcIds = new List<String>{'<id1>', '<id2>'};
for (String tcId : tcIds) {
    List<ProcessInstanceWorkitem> workItems = [SELECT Id FROM ProcessInstanceWorkitem WHERE ProcessInstance.TargetObjectId = :tcId];
    if (!workItems.isEmpty()) {
        Approval.ProcessWorkitemRequest req = new Approval.ProcessWorkitemRequest();
        req.setAction('Removed');
        req.setComments('Recalling to update timecard notes');
        req.setWorkitemId(workItems[0].Id);
        Approval.process(req);
    }
}

// 2. Update notes (timecard is now in Saved status after recall)
List<pse__Timecard_Header__c> tcs = [SELECT Id FROM pse__Timecard_Header__c WHERE Id IN ('<id1>','<id2>')];
Map<Id, Map<String, String>> notesMap = new Map<Id, Map<String, String>>();
notesMap.put('<id1>', new Map<String, String>{
    'Mon' => '<note>', 'Tue' => '<note>', 'Wed' => '<note>',
    'Thu' => '<note>', 'Fri' => '<note>', 'Summary' => '<summary>'
});
notesMap.put('<id2>', new Map<String, String>{
    'Mon' => '<note>', 'Tue' => '<note>', 'Wed' => '<note>',
    'Thu' => '<note>', 'Fri' => '<note>', 'Summary' => '<summary>'
});
for (pse__Timecard_Header__c tc : tcs) {
    Map<String, String> notes = notesMap.get(tc.Id);
    tc.pse__Monday_Notes__c = notes.get('Mon');
    tc.pse__Tuesday_Notes__c = notes.get('Tue');
    tc.pse__Wednesday_Notes__c = notes.get('Wed');
    tc.pse__Thursday_Notes__c = notes.get('Thu');
    tc.pse__Friday_Notes__c = notes.get('Fri');
    tc.pse__Timecard_Notes__c = notes.get('Summary');
}
update tcs;

// 3. Resubmit — restore to Submitted status
for (pse__Timecard_Header__c tc : tcs) {
    tc.pse__Submitted__c = true;
    tc.pse__Status__c = 'Submitted';
}
update tcs;
```

After resubmit, verify the status:

```bash
sf data query --query "SELECT Id, pse__Project__r.Name, pse__Status__c FROM pse__Timecard_Header__c WHERE Id IN ('<id1>','<id2>')" --target-org "$SF_TARGET_ORG"
```

If any timecard did not return to Submitted, warn the user to resubmit manually in FinancialForce: `https://databricks.lightning.force.com/lightning/n/pse__Timecard_Entry`

#### Existing Approved timecards: DO NOT MODIFY

**Never attempt to unlock, update, or re-lock Approved timecards.** `Approval.unlock()` can create lock states that prevent all future edits, and modifying Approved records risks corrupting approval history. If an Approved timecard needs changes, inform the user to handle it manually through FinancialForce or contact their admin.

Skip Approved timecards entirely — display them in the preview/report for the user's reference but do not write to them.

### Step 7: Report + Optional Submission

Display summary table with notes, then confirm the date range:

```
| Project               | Mon | Tue | Wed | Thu | Fri | Total | Status    |
|-----------------------|-----|-----|-----|-----|-----|-------|-----------|
| Albertsons - RSA Gold | 2.0 | 2.0 | 2.0 | 1.0 | 1.0 |     8 | Approved  |
| PVH - RSA Plat Sub    | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |     6 | Submitted |
| POD Management        | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 |     8 | Saved     |
| PS - Admin            | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 |    18 | Saved     |
|                       |     |     |     |     |     |    40 |           |

Timesheet completed: Mar 15–21, 2026 (4 timecards, 40 hours)
```

After displaying the report, ask the user if they would like to submit their timecards. **Only timecards in Saved status are eligible for submission.** If the user confirms, submit them via Apex:

```apex
List<pse__Timecard_Header__c> tcs = [SELECT Id, pse__Project__r.Name, pse__Status__c
    FROM pse__Timecard_Header__c
    WHERE Id IN ('<saved_id1>', '<saved_id2>')
    AND pse__Status__c = 'Saved'];

for (pse__Timecard_Header__c tc : tcs) {
    tc.pse__Submitted__c = true;
    tc.pse__Status__c = 'Submitted';
}
update tcs;
```

After submission, verify the status changed:

```bash
sf data query --query "SELECT Id, pse__Project__r.Name, pse__Status__c, pse__Submitted__c FROM pse__Timecard_Header__c WHERE Id IN ('<saved_id1>','<saved_id2>')" --target-org "$SF_TARGET_ORG"
```

If any timecard did not transition to Submitted, warn the user and provide a direct link to submit manually: `https://databricks.lightning.force.com/lightning/n/pse__Timecard_Entry`

If the user declines submission, remind them they can submit later through FinancialForce.

## Field Reference

| Object | Key Fields |
|--------|-----------|
| `pse__Timecard_Header__c` | `pse__Assignment__c`, `pse__Project__c`, `pse__Resource__c`, `pse__Start_Date__c` (Sunday), `pse__End_Date__c` (Saturday), `pse__Monday_Hours__c`–`pse__Friday_Hours__c`, `pse__Monday_Notes__c`–`pse__Friday_Notes__c` (255 char max), `pse__Timecard_Notes__c`, `pse__Status__c` (Saved/Submitted/Approved), `pse__Submitted__c` |
| `pse__Assignment__c` | `pse__Schedule__c` (lookup), `pse__End_Date__c` |
| `pse__Schedule__c` | `pse__Monday_Hours__c`–`pse__Friday_Hours__c` (default daily hours) |
| `pse__Schedule_Exception__c` | `pse__Schedule__c` (parent), `pse__Date__c` (start), `pse__End_Date__c`, `pse__Monday_Hours__c`–`pse__Friday_Hours__c` (override hours) |
