---
name: prospect-files
description: The markdown file schema for sales prospects in the [YOUR_FIRM] outbound harness. One file per lead at PROSPECT_DIR (OneDrive). Source of truth for state, dossier, drafts, conversation, and audit log. Read and written by Prospector, Composer, and Cadence skills. Use when researching a lead, drafting outbound, processing replies, or auditing a sales prospect's history.
cowork:
  category: automation
  icon: DocumentText
---

# Prospect Files

One markdown file per lead. The file is the prospect.

## Location

All prospect files live at `PROSPECT_DIR` on OneDrive. Per `sales-harness-config.md`:

- UI path: `OneDrive - [YOUR_TENANT] / sales-harness / prospects`
- Drive ID: `[YOUR_DRIVE_ID]`
- Folder item ID: `[YOUR_FOLDER_ITEM_ID]`

Access via the SharePoint/OneDrive MCP tools (`GetDriveChildren`, `GetDriveItem`, `ReadFileContent`, and Graph PUT for uploads).

> To find these IDs: open the prospects folder in OneDrive on the web, then call `mcp__sharepoint_onedrive__GetDefaultDrive` (no args) to retrieve the drive ID, and `mcp__sharepoint_onedrive__GetDriveChildren` with that drive ID to get the folder item ID of `sales-harness/prospects`.

## File naming

`<firstname>-<lastname>.md`, all lowercase, hyphenated, ASCII only. Slugs collide on common names → append a short company suffix: `jane-smith-acme.md`.

## The schema

```markdown
---
# Identity
name: Jane Smith
email: jane@acme.com
company: Acme
title: VP of Revenue Operations
linkedin_url: https://www.linkedin.com/in/janesmithacme
domain: acme.com
timezone: America/New_York

# State machine
state: new
state_updated_at: 2026-05-25T14:30:00Z
last_agent: null

# Campaign membership
campaign: outbound-email-v1
lawful_basis: legitimate-interest  # or: consent, contract

# Cadence runtime
touch_count: 0
next_step_at: null
thread_id: null
sent_at: null
cadence_template_id: null

# Compliance flags
do_not_contact: false
email_invalid: false

# Outcomes (filled in over time)
icp_score: null
disqualify_reason: null
hold_reason: null
re_engage_at: null
---

# Jane Smith — VP RevOps, Acme

## Dossier
(filled by Prospector)

## Signals
(filled by Prospector)

## ICP Fit
(filled by Prospector)

## Hook
(filled by Prospector)

## Prior Touches
(filled by Prospector)

## Notes
(filled by any agent)

## Draft (pending approval)
(filled by Composer when state transitions to draft_pending_approval;
removed or moved to ## Conversation when the lead transitions to sent)

## Conversation
(filled by Cadence as sends and replies happen; chronological)

## Audit
(append-only log of every state transition and tool call)
```

## State machine (v1)

```
new → researched → draft_pending_approval → sent → awaiting_reply
                                                          │
                                                          ├→ replied → composer drafts a reply
                                                          ├→ cadence_step_due → cadence queues the next templated step as a draft (state goes back to draft_pending_approval)
                                                          ├→ dormant
                                                          └→ meeting_booked
disqualified is terminal. needs_review is the error state.
```

The human's "click Send in Outlook" IS the approval. Cadence detects the send and transitions `draft_pending_approval → sent` directly. There is no separate `approved`/`rejected` state in v1.

## State transition rules

Each transition writes:

- `state:` → new value
- `state_updated_at:` → ISO 8601 timestamp
- `last_agent:` → the agent that made the transition
- An entry in `## Audit` like:
  `2026-05-25T14:32:01Z [prospector] state: new → researched (icp_score: 8)`

Agents may only write the transitions named in their definition:

- Prospector: `new → researched | disqualified`
- Composer: `researched | replied → draft_pending_approval`
- Cadence: everything else

## Reading the file

When an agent reads a file:

1. Use `ReadFileContent` (or `GetDriveItem` + `ReadFileContent`) to fetch the markdown.
2. Parse the YAML frontmatter.
3. Check `do_not_contact` first; if true, skip.
4. Check `state` matches the agent's input states; if not, skip.
5. Read the body sections relevant to the agent's job (Prospector reads only frontmatter to decide whether to research; Composer reads Dossier + Hook + Signals to draft; Cadence reads Conversation + Audit to decide next move).

## Writing the file

OneDrive files are written via Graph API. The pattern:

1. Download the existing file to a workspace temp path with `ReadFileContent`.
2. Edit locally with the `Edit` tool (preserve any operator manual edits — never blind-overwrite).
3. Upload back via Graph PUT to the file's content endpoint.

When writing a new section (e.g. Composer adding a `## Draft (pending approval)`), insert it in the canonical order shown in the schema. Sections never duplicate — if `## Draft (pending approval)` already exists, update it in place rather than adding a second one.

## PII and persistence

Prospect files contain PII (names, emails, dossier intel). They live only in the OneDrive sales-harness folder. Reference files (`_schema.md`, `_template.md`, `_example-jane-smith.md`) document the format and live in the same folder for convenience.
