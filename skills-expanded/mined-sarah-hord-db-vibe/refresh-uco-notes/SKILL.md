---
name: refresh-uco-notes
description: Refresh stale UCO onboarding notes for any account. Use when asked to update onboarding notes, refresh UCO notes, check stale UCOs, or run onboarding refresh. Triggers on "onboarding refresh", "update onboarding notes", "stale UCOs", "refresh notes", "uco-onboarding-refresh".
---

# UCO Onboarding Notes Refresh

Automatically identify stale UCO onboarding notes, gather context from multiple sources, and draft updates following the SA's personal writing pattern.

This skill is **fully parameterized** — each SA configures their own initials, account, template, and preferences via a YAML config file.

## Capabilities

- Load SA-specific configuration from `~/.vibe/uco-onboarding-config.yaml`
- Query Logfood to find active UCOs and detect stale onboarding notes
- Gather context in parallel from Gmail, Google Calendar, Slack, and Salesforce partner notes
- Draft updated notes using the SA's custom template and style examples
- Present updates for review and write approved changes to Salesforce

## Workflow

1. **Load Config** — Read `~/.vibe/uco-onboarding-config.yaml` (prompt to create if missing)
2. **Identify Stale UCOs** — Query Logfood for UCOs matching the SA's account and markers, flag those not updated within the staleness threshold
3. **Gather Context** — For each stale UCO, search Gmail, Calendar, Slack, and Salesforce in parallel for recent activity
4. **Draft Updates** — Generate updated notes following the SA's template and style, appending new milestones
5. **Review & Apply** — Present drafts for user approval, then write approved updates to Salesforce

## Prerequisites

- `gmail` skill (for email context)
- `google-calendar` skill (for meeting context)
- Slack MCP tools (for channel context)
- `field-data-analyst` agent (for Logfood queries)
- Salesforce CLI (`sf`) authenticated

## Phase 0: Load Configuration

1. Read the SA's config file at `~/.vibe/uco-onboarding-config.yaml`
2. If the file does not exist, prompt the user to create one using the template from `references/config-template.yaml`
3. Parse all config values. The config has these fields:

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `sa_initials` | Yes | — | SA's initials for the notes header (e.g., "SS", "JD") |
| `account_name` | Yes | — | Account name to filter UCOs (partial match) |
| `partner_initials` | No | — | Co-SA initials who also writes updates |
| `notes_field` | No | `Implementation_Notes__c` | Salesforce field for onboarding notes |
| `partner_notes_field` | No | `Demand_Plan_Next_Steps__c` | Salesforce field for partner status |
| `date_format` | No | `DD/MM/YYYY` | Date format for the notes header |
| `staleness_days` | No | `14` | Days before notes are stale |
| `stages` | No | `[U3, U4, U5, U6]` | UCO stages to include |
| `slack_channels` | No | `[]` | Slack channels to search |
| `notes_template` | No | (see default) | Custom notes template with placeholders |
| `style_examples` | No | `[]` | Array of example notes for style matching |

4. Validate required fields (`sa_initials`, `account_name`). Error if missing.

## Phase 1: Identify Stale UCOs

1. Use the `field-data-analyst` agent to query Logfood. Build the query dynamically from config:

```sql
SELECT uc.Id, uc.Name, uc.Stages__c,
       uc.{notes_field} AS onboarding_notes,
       uc.{partner_notes_field} AS partner_notes
FROM main.sfdc_bronze.usecase__c uc
JOIN main.sfdc_bronze.account a ON uc.Account__c = a.Id
WHERE uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
AND a.Name LIKE '%{account_name}%'
AND uc.Stages__c IN ({stages_csv})
AND (
  uc.{notes_field} LIKE '%{sa_initials} %'
  {partner_clause}
)
```

Where:
- `{notes_field}` = config `notes_field` (default: `Implementation_Notes__c`)
- `{partner_notes_field}` = config `partner_notes_field` (default: `Demand_Plan_Next_Steps__c`)
- `{account_name}` = config `account_name`
- `{stages_csv}` = config `stages` joined as `'U3', 'U4', 'U5', 'U6'`
- `{partner_clause}` = if `partner_initials` is set: `OR uc.{partner_notes_field} LIKE '%{partner_initials}%'`, otherwise omit

2. Parse the SA date header from the `onboarding_notes` column. Look for the pattern: `{sa_initials} <date>` on the first line. Parse the date using `{date_format}`.

3. Flag UCOs where:
   - The SA header date is older than `{staleness_days}` days, OR
   - No SA header exists at all (partner-only UCOs)

4. Present the stale UCO list to the user with: UCO name, current stage, last SA update date (or "never"), and days since last update.

5. Ask the user: proceed with all stale UCOs, select specific ones, or abort?

## Phase 2: Gather Context (Per Stale UCO)

For each stale UCO, gather context from multiple sources **in parallel** using subagents:

1. **Salesforce Partner Notes** — If `partner_initials` is configured, read the latest entries from `{partner_notes_field}` for recent status updates written by the partner
2. **Gmail** — Use the `gmail` skill to search for emails mentioning the UCO name, customer stakeholder names, or workload keywords in the last `{staleness_days}` days (capped at 30 days)
3. **Google Calendar** — Use the `google-calendar` skill to find recent and upcoming meetings with account stakeholders related to the UCO
4. **Slack** — If `slack_channels` is configured, use Slack MCP tools to search those channels. Otherwise, search for messages mentioning the account name + UCO name

Compile all gathered context into a summary per UCO.

## Phase 3: Draft Updated Notes

For each stale UCO, draft an updated `{notes_field}` entry.

### Template Resolution

If the SA provided a `notes_template` in config, use it with these placeholders:
- `{sa_initials}` — SA initials from config
- `{date}` — Today's date in `{date_format}` format
- `{objectives}` — Existing objectives (preserved) or synthesized from context
- `{milestones}` — Existing milestones + new ones appended
- `{stakeholders}` — Existing stakeholders (preserved) or extracted from context
- `{partner}` — Existing partner info (preserved) or "NA"

If no custom template is provided, use the default template from `references/default-template.md`.

### Style Matching

If the SA provided `style_examples` in config (array of example note strings), analyze those examples to match:
- Tone and voice (formal vs informal, technical depth)
- Milestone phrasing style (past tense vs present, level of detail)
- How stakeholders are formatted
- Any unique patterns

### Key Rules

- **ALWAYS update the SA date header to today's date.** The date beside the initials represents "last refreshed" and MUST be today.
- **Preserve ALL existing content** — update the milestones list by appending new entries
- If the UCO already has an SA header, replace ONLY the date on the first line and append new milestones
- If no SA header exists, create one from scratch using gathered context
- Milestones are numbered chronologically
- When appending milestones, continue the numbering from the last existing milestone
- New milestones should include a parenthetical date: `(Month Year)`

### Date Format Handling

Convert the `date_format` config value to the actual date:
- `DD/MM/YYYY` → `11/03/2026` (European)
- `MM/DD/YYYY` → `03/11/2026` (US)
- `YYYY-MM-DD` → `2026-03-11` (ISO)
- Any other strftime-compatible format

## Phase 4: Review and Apply

1. Present all drafted updates to the user in a clear format showing:
   - UCO name and stage
   - Current notes (abbreviated to first 3 lines + milestone count)
   - Proposed updated notes (full)
   - Sources used (which emails/meetings/Slack messages informed the update)
   - Confidence level (high if multiple sources corroborate, medium if single source, low if mostly inferred)

2. Ask the user to **approve**, **edit**, or **skip** each UCO individually.

3. For approved updates, write to Salesforce:
   ```bash
   SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
   sf data update record --sobject UseCase__c --record-id <UCO_ID> --values "{notes_field}='<UPDATED_NOTES>'" --target-org "$SF_TARGET_ORG"
   ```

4. After all updates, show a summary: X updated, Y skipped, Z failed.

## Recurring Usage

This skill supports recurring execution via `/loop`:
```
/loop 1w /uco-onboarding-refresh
```
Adjust interval as needed (e.g., `2w` for biweekly, `3d` for every 3 days).

## Examples

### Example: Full refresh
User says: `/uco-onboarding-refresh`
Result: Reads config, scans all active UCOs for the configured account, identifies stale ones, gathers context, drafts updates, presents for review.

### Example: First-time setup
User says: `/uco-onboarding-refresh`
Config not found → prompts user to fill in their initials, account name, and optionally paste 2-3 example notes for style matching. Creates `~/.vibe/uco-onboarding-config.yaml`.

### Example: Recurring setup
User says: `/loop 1w /uco-onboarding-refresh`
Result: Runs the onboarding refresh automatically every week.
