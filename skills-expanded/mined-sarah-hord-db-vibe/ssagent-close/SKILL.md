---
name: ssagent-close
description: Closes out a Salesforce SSA specialist request (ASQ). Use when an SSA engagement or ASQ is complete. Accepts AR-XXXXXXXXX Salesforce identifiers. Reviews engagement notes, emails, calendar, and work product, drafts a closure summary and final Salesforce status note, identifies reusable assets, and marks the ASQ as Complete in Salesforce. Do not use for Asana or generic project management tasks.
argument-hint: "AR-XXXXXXXXX"
user-invocable: true
model: sonnet
---

# ASQ Close

Close out a Salesforce ASQ with a structured summary and learnings.

**Usage:** `/ssagent-close AR-XXXXXXXXX`

---

## Prerequisites

Load the profile using `load_profile.py` from `ssagent-sfdc` (returns all keys with defaults applied). Extract `sf_org` and `initials`. If either is `None`, fall back to `fe-salesforce-tools:salesforce-authentication` and the User query pattern from `ssagent-sfdc` Reusable Query Patterns.

Substitute the resolved `sf_org` value as a **literal** into every `<SF_ORG_USERNAME>` placeholder below.

Invoke `fe-google-tools:google-auth` to confirm Google credentials are valid.

---

## Step 1 — Resolve ASQ

Parse `$ARGUMENTS`:
- If it starts with `AR-` → direct fetch by AR number
- Otherwise → fuzzy match against open ASQs by customer name fragment; show the match and confirm with the user before proceeding

Run the following queries **in parallel**:

**Fetch ASQ record:**
```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Account__c, Status__c, Support_Type__c, AssignmentDate__c, End_Date__c, Request_Description__c, Request_Status_Notes__c, Additional_Notes_or_Doc_Links__c FROM ApprovalRequest__c WHERE Name = '<AR-XXXXXXXXX>'" --target-org <SF_ORG_USERNAME> --json
```

**Fetch linked UCOs:**
```bash
sf data query --query "SELECT Name, Stages__c, Amount__c, MonthlyTotalDollarDBUs__c, Business_Value_Description__c, POCStatus__c FROM UseCase__c WHERE Id IN (SELECT Use_Case__c FROM Approved_UseCase__c WHERE Approval_Request__c = '<SFDC_ID>')" --target-org <SF_ORG_USERNAME> --json
```

Note: `AssignmentDate__c` (engagement start), `Account_Name__c`, `SFDC_ID`, and `<INITIALS>` (from profile or Prerequisites fallback).

---

## Step 2 — Gather Engagement Evidence (Parallel)

Run all in parallel to reconstruct what happened during the engagement:

**A. Google Calendar** — invoke `fe-google-tools:google-calendar` to find all meetings with `[ACCOUNT_NAME]` between `AssignmentDate__c` and today. Extract: meeting count, key topics discussed, decisions made.

**B. Gmail** — invoke `fe-google-tools:gmail` to find emails mentioning `[ACCOUNT_NAME]` over the same period. Extract: key threads, outcomes, action items resolved.

**C. Google Drive** — invoke `fe-google-tools:google-docs` to search Drive for documents related to `[ACCOUNT_NAME]` or the AR number. Focus on files created or modified since `AssignmentDate__c`. List titles and URLs — these are candidate reusable assets.

**D. Slack (fallback only)** — only invoke `fe-workflows:slack-discovery-agent` if Calendar and Gmail returned sparse context.

---

## Step 3 — Draft Closure Materials

Using the ASQ history and evidence from Step 2, produce all four sections and present them to the user before writing anything to Salesforce:

**A. Closure summary** (2–4 sentences):
What was the engagement about, what was done, what was the outcome. Be specific: include outcomes, metrics, and decisions made.

**B. Reusable assets** (if any):
List specific Drive docs, notebooks, or architectures found in Step 2C that could benefit other SSAs. If none found, say so explicitly.

**C. Final status note** using profile `note_format.prefix` (default: `<INITIALS> YYYY-MM-DD`):
```
<prefix>: Closing. <1-sentence outcome summary>.
```

If `custom_instructions` is set in the profile, apply it to the closure summary and final note.

**D. Long-term learnings** (optional, 1–3 bullet points):
Patterns, gotchas, or approaches useful for future similar engagements.

**E. Actual Effort in Days** (`Actual_Effort_in_Days__c`):
Estimate from the evidence gathered in Step 2. Count calendar meetings as ~0.5 day each, add estimated prep/follow-up time based on email threads and Drive artifacts. Present the estimate and let the user adjust.

Present all five sections:
```
Closure materials for AR-XXXXXXXXX — [ACCOUNT_NAME]:

A. Summary:
  [2–4 sentences]

B. Reusable assets:
  - [title] — [URL] — suggested: [where to share]
  (or: None found)

C. Final note:
  [INITIALS YYYY-MM-DD: Closing. ...]

D. Learnings:
  - [bullet]

E. Actual Effort: [N] days
  (based on [X meetings] + [estimated prep/follow-up])

```

Then use `AskUserQuestion` with options:
- "Approve all" (Recommended) — proceed to Step 4
- "Edit" — let user modify the materials before writing
- "Skip" — do not write to Salesforce

---

## Step 4 — Write to Salesforce and Chatter

Load `sf_update_channel` from the profile (default: `dual`).

**If `sf_update_channel` is `notes` or `dual`:**
On user approval, use `sf_update.py close` from `ssagent-sfdc` to update the ASQ with status `Complete`, the closure note, combined status notes, today's date as `Actual_Completion_Date__c`, and the approved effort value as `Actual_Effort_in_Days__c`. Pass `--separator` based on the profile's `note_format.separator` (default `single`).

**If `sf_update_channel` is `chatter` or `dual`:**
Post the closure summary to Chatter so it appears in the ASQ's right sidebar:
```bash
python3 "$SF_UPDATE" chatter \
  --record-id "<SFDC_ID>" \
  --text "<FINAL NOTE + CLOSURE SUMMARY>" \
  --org "<SF_ORG_USERNAME>"
```

**Note:** When `sf_update_channel` is `chatter` (Chatter-only), the `sf_update.py close` command is still used for status, date, and effort fields — only the `Request_Status_Notes__c` prepend and `Request_Closure_Note__c` writes are skipped. Instead, post the closure note and final status note to Chatter only.

If any update fails: show the error and ask the user whether to retry or skip.

---

## Step 5 — Closure Report & Assets

### 5a. Closure Report

Check the profile value `closure_doc`:
- `always` → create the report
- `ask` (default) → use `AskUserQuestion`: "Create a closure report in the shared SSA Drive folder?" with options: "Yes, create report" (Recommended), "No, skip"
- `never` → skip to 5b

If creating the report:

1. Build a markdown file (`/tmp/ssagent-closure-XXXXXX.md`) from Steps 1–3 using this structure:

```markdown
# ASQ Closure Report: <AR-XXXXXXXXX> — <ACCOUNT_NAME>

*Generated by SSAgent on <YYYY-MM-DD>*

**ASQ:** [<AR-XXXXXXXXX>](https://databricks--c.vf.force.com/apex/ASQ?id=<SFDC_ID>)
**Account:** <ACCOUNT_NAME>
**Support Type:** <Support_Type__c>  |  **Engagement:** <AssignmentDate__c> → <TODAY>
**Effort:** <N> days  |  **SSA:** <sf_org>

## Closure Summary
<Section A — 2–4 sentences>

## Outcome & Learnings
<Section D — bullet points>

## Reusable Assets
<Section B — list of title + URL, or "None identified">

## Engagement Timeline
- <meeting count> meetings, <email thread count> email threads
- Key topics: <list from Step 2 evidence>

## Linked Use Cases
| UCO | Stage | Monthly $DBU | Business Value |
|-----|-------|-------------|----------------|
<One row per UCO from Step 1, or "No linked UCOs">
```

2. Create the Google Doc using `markdown_to_gdocs.py` from `fe-google-tools:google-docs` with `--title "ASQ Closure: <AR-XXXXXXXXX> — <ACCOUNT_NAME>"`. Capture the returned document URL.

3. Move the doc to the shared closure folder (`closure_folder_id` from profile) using `fe-google-tools:google-docs` — add the folder as parent, remove `root`.

4. Prepend `"Closure Report: <GOOGLE_DOC_URL>"` to `Additional_Notes_or_Doc_Links__c` using `sf_update.py prepend` from `ssagent-sfdc`.

### 5b. Reusable Assets

If reusable assets were identified in Step 3B, present each one and ask whether to share more broadly (Glean, field enablement, Confluence).

### 5c. Summary

Tell the user:
- Salesforce: ASQ marked Complete with closure note and effort
- Closure report: [Google Doc URL] (in shared SSA folder) — or "skipped"
- Doc link: prepended to `Additional_Notes_or_Doc_Links__c` — or "n/a"
- Assets: [list any shared or flagged]
