---
name: account-sync
description: Sync account overview documents with recent activity from Calendar, Gmail, Slack, Salesforce, Google Drive, and GitHub. Use when updating account folders, refreshing engagement timelines, or checking for new artifacts.
user-invocable: true
---

# Account Sync

Orchestrate a comprehensive account activity sync by pulling recent data from multiple sources and updating the account-overview.md in each account folder.

## Capabilities

- Pull recent meetings from Google Calendar matching the account name or key contacts
- Search Gmail for emails related to the account (by name, domain, or contact emails)
- Search Slack for messages mentioning the account in relevant channels
- Query Salesforce for UCO status, stage updates, contacts, and account team info
- Scan Google Drive for new artifacts (slides, docs, demand plans, demos) in the account folder
- Update the Engagement Timeline, Existing Artifacts, and Databricks Engagement sections incrementally
- Create a new account-overview.md from template for accounts that do not have one yet

## Arguments

- `/account-sync <account-name>` — Sync a single account (e.g., `/account-sync halton-healthcare`)
- `/account-sync --all` — Sync all account folders in the working directory

## Workflow

### Step 0: Verify Authentication

Before querying any data sources, verify that authentication is active. Run these checks:

1. **Google Auth** — Invoke the `google-auth` skill to verify Google authentication is active (needed for Calendar, Gmail, Drive, Docs)
2. **Salesforce Auth** — Invoke the `salesforce-authentication` skill to verify Salesforce CLI authentication

If either auth is expired, prompt the user to re-authenticate before continuing.

### Step 1: Resolve Target Accounts

Parse the user's arguments:

- If a specific account name is given (e.g., `halton-healthcare`), target only that folder
- If `--all` is specified, scan the working directory for subdirectories, **excluding**: `.obsidian`, `.claude`, `.claude-plugin`, and any hidden directories (starting with `.`)

For each target account folder:
1. Read the existing `account-overview.md` if it exists
2. Extract the **display name** (from the `# heading`), **key contacts** (names and emails from the contacts table), **UCO name** (from Databricks Engagement table), and **existing timeline entries** (dates already logged) and **existing artifacts** (documents already linked)
3. If no `account-overview.md` exists, note this account needs a new one created from the template at `${CLAUDE_SKILL_DIR}/references/account-overview-template.md`

Build a context object for each account:
- `folder_name`: directory name (e.g., `halton-healthcare`)
- `display_name`: human-readable name (e.g., `Halton Healthcare`)
- `contacts`: list of names and emails from the overview
- `existing_timeline_dates`: set of dates already in the timeline
- `existing_artifact_names`: set of document names already linked
- `has_overview`: boolean
- `last_synced`: the date from the `> Last synced:` line at the bottom of the overview (if present). Use this to narrow searches — on subsequent syncs, only query for activity **since the last sync date** instead of the full 30-day window. If no `last_synced` date exists, fall back to the default 30-day window.

### Step 2: Gather Activity (Parallel Agents)

For **each account**, launch up to 5 Agent sub-agents **in parallel** in a single message. Each agent gets the account context and instructions for one data source.

**IMPORTANT**: Launch all agents for a single account in ONE message to maximize parallelism.

**Date range**: If `last_synced` is set, search from that date to today. Otherwise, search the last 30 days. Pass the computed `since_date` (YYYY-MM-DD) to each agent prompt.

#### Agent 1: Google Calendar
Prompt the agent:
> Search Google Calendar for meetings in the last 30 days that mention "{display_name}" or any of these contacts: {contacts list}. For each meeting found, return: date (YYYY-MM-DD), event title, attendees, and any meeting notes or description. Use the `google-calendar` skill. Format results as a markdown table with columns: Date, Event, Notes.

#### Agent 2: Gmail
Prompt the agent:
> Search Gmail for emails from the last 30 days matching: "{display_name}" OR "{folder_name}" OR any of these email domains/addresses: {contact emails}. For each relevant email, return: date, subject, from, summary of content. Use the `gmail` skill. Focus on emails that indicate engagement activity (meetings scheduled, follow-ups, proposals sent, questions asked). Format results as a markdown table with columns: Date, Event, Notes.

#### Agent 3: Slack
Prompt the agent:
> Search Slack for messages from the last 30 days mentioning "{display_name}" or "{folder_name}". Search in channels likely used for account discussions (team channels, deal channels, general SA channels). Use the Slack MCP tools (`mcp__slack__slack_read_api_call` with endpoint `search.messages`). For each relevant thread, return: date, channel, summary of discussion. Format results as a markdown table with columns: Date, Event, Notes.

#### Agent 4: Salesforce
Prompt the agent:
> Look up the Salesforce account for "{display_name}". Use the `salesforce-actions` skill. Return:
> 1. Account team (AE, SA, BDR, Manager)
> 2. All Use Case Objects (UCOs) — for each UCO return: name, stage (U1-U6), health, products, target go-live date, onboarding date (if U5+), next steps, and last modified date
> 3. Any Blocker__c records linked to UCOs
> 4. Key contacts on the account
> 5. Any recent activity logged on the account (last 30 days)
> Format the UCO data as a detailed table and contacts as a separate table.

#### Agent 5: Google Drive
Prompt the agent:
> Search Google Drive for files related to "{display_name}". Use the `google-docs` skill or Google Drive API. Look for:
> 1. Google Docs (meeting notes, proposals, POC documents, demand plans)
> 2. Google Slides (presentations, demos, architecture decks)
> 3. Google Sheets (sizing, planning)
> For each file found, return: file name, file type, last modified date, and the Google Drive/Docs/Slides URL. Format results as a markdown table with columns: Document, Link.

### Step 3: Merge and Deduplicate Results

Once all agents return, combine the results for each account:

1. **Engagement Timeline** — Collect all dated events from Calendar, Gmail, Slack, and Salesforce agents. Sort by date descending. Remove any entries whose date AND event description closely match an existing timeline entry (fuzzy match — same date and similar text means duplicate).

2. **Existing Artifacts** — Collect all documents from Google Drive agent. Remove any whose URL or name matches an already-linked artifact.

3. **Databricks Engagement** — If Salesforce returned updated UCO stage, contacts, or account team info, note the fields that differ from what is currently in the overview.

4. **Key Contacts** — If Salesforce returned contacts not already in the overview, note new contacts to add.

### Step 4: Update the Account Overview

For each account:

#### If `account-overview.md` EXISTS:

Use the **Edit tool** to make surgical updates to the existing file. Do NOT regenerate the entire document. Make these specific edits:

1. **Engagement Timeline table** — Insert new rows at the correct chronological position (most recent at bottom). Each row: `| {date} | {event} | {notes} |`. Do NOT remove or modify existing rows.

2. **Existing Artifacts table** — Append new rows for any newly discovered documents. Each row: `| {document name} | [{link text}]({url}) |`. Do NOT remove existing rows.

3. **Databricks Engagement table** — Update only fields where Salesforce returned newer data (e.g., new AE assigned). Leave fields unchanged if Salesforce data matches. UCO details are now in their own table (see below).

3b. **Use Case Objects (UCOs) table** — This is a separate table under a `### Use Case Objects (UCOs)` heading within the Databricks Engagement section. Update all UCO rows with the latest data from Salesforce. Each row has columns: UCO Name, Stage, Health, Products, Target Go-Live, Onboarding Date, Next Steps. Add new UCOs, update changed fields on existing ones. If a UCO was lost or closed, keep it in the table with its current status.

4. **Key Customer Contacts table** — Append new contacts discovered from Salesforce that are not already listed.

5. Do NOT modify: Organization Profile, Current State, Opportunity Analysis, SA Strategy, or Bottom Line sections. These are manually curated.

6. **Last synced timestamp** — Update (or add) the `> Last synced:` line at the very end of the file with today's date in `YYYY-MM-DD` format. This line must always be the last line of the file:
   ```
   > Last synced: 2026-03-16
   ```

#### If `account-overview.md` DOES NOT EXIST:

1. Read the template from `${CLAUDE_SKILL_DIR}/references/account-overview-template.md`
2. Replace `{{ACCOUNT_DISPLAY_NAME}}` with the display name (convert folder name to title case, e.g., `halton-healthcare` becomes `Halton Healthcare`)
3. Populate the Databricks Engagement table with any Salesforce data found
4. Populate Key Customer Contacts with any contacts found
5. Populate Engagement Timeline with all discovered events
6. Populate Existing Artifacts with all discovered documents
7. Append `> Last synced: {today's date YYYY-MM-DD}` as the last line
8. Write the file to `{account_folder}/account-overview.md`

### Step 5: Report Summary

After all accounts are processed, output a summary to the user:

```
## Account Sync Complete

### {Account Name}
- Timeline: +{N} new entries added
- Artifacts: +{N} new documents linked
- UCO: {stage} (updated/unchanged)
- Contacts: +{N} new contacts added
- Status: Updated / Created from template / No changes

### {Next Account}
...
```

If any agents failed or returned no results, note which data sources had issues so the user can investigate.

## Examples

### Sync a single account
```
/account-sync halton-healthcare
```
Pulls the last 30 days of activity for Halton Healthcare from all sources and updates the existing overview.

### Sync all accounts
```
/account-sync --all
```
Iterates through all account folders (halton-healthcare, arctiq, dova-health, geologic-ai, meridian-credit-union), creates overviews where missing, and updates existing ones.

### After a customer meeting
```
/account-sync arctiq
```
Run after logging a call or sending a follow-up email. The sync will pick up the new calendar event, email, and any Slack discussion, adding them to the timeline.
