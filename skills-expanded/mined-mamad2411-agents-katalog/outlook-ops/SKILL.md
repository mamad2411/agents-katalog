---
name: outlook-ops
description: How the [YOUR_FIRM] sales harness reads from and writes to Outlook via the Copilot MCP. Composer uses it to save drafts. Cadence uses it to detect sends, detect replies, and queue templated follow-ups. Use when the harness needs to draft a new email, draft a threaded reply, search sent items for a send, scan inbox for a reply, or propose meeting times.
cowork:
  category: automation
  icon: Mail
---

# Outlook Ops

In Copilot, Outlook is a native MCP. The harness uses these tools directly — no helper scripts, no markdown-to-Outlook sync bridge needed.

## What's available

### Read

| Operation | Tool |
|---|---|
| Search any mailbox content | `SearchM365` with `sources=["email"]` |
| List messages with filters | `ListMessages` (folder, from, date, unread, flagged) |
| Get a specific message | `GetMessage` |
| List mail folders | `ListMailFolders` |
| List calendar events | `ListCalendarView` / `ListEvents` |
| Find free/busy slots | `FindMeetingTimes` |
| Search SharePoint/OneDrive | `SearchM365` with `sources=["files"]` or `SearchDrive` |

### Write

| Operation | Tool |
|---|---|
| Draft a new email (NOT send) | `CreateDraftMessage` |
| Draft a threaded reply (NOT send) | `CreateReplyDraft` |
| Draft a reply-all (NOT send) | `CreateReplyAllDraft` |
| Update an existing draft | `UpdateDraft` |
| Send a draft | `SendDraftMessage` |
| Add file attachment to a draft | `AddDraftAttachments` |

In v1, the harness uses `CreateDraftMessage` / `CreateReplyDraft` only. It never calls `SendDraftMessage`. The human clicks Send in Outlook — that click is the approval.

## Tenant configuration

From `sales-harness-config.md` in OneDrive:

- `OUTLOOK_FROM`: `[YOUR_OUTLOOK_EMAIL]`
- Drafts folder ID: `[YOUR_DRAFTS_FOLDER_ID]` (well-known name `drafts` works in most calls)
- Sent Items folder ID: `[YOUR_SENT_FOLDER_ID]` (well-known name `sentitems` works in most calls)
- Inbox folder ID: `[YOUR_INBOX_FOLDER_ID]` (well-known name `inbox` works in most calls)

> Most ListMessages calls accept the well-known names directly, so you don't actually need to look up the IDs unless you want stable references. To get IDs, call `mcp__outlook__ListMailFolders` once and copy them into your config.

## Composer flow — saving a first-touch draft

When the Composer finishes a draft and the lead's state is `researched` → `draft_pending_approval`:

1. Write the draft text to the prospect MD file's `## Draft (pending approval)` section (for audit + human review in OneDrive).
2. Call `CreateDraftMessage`:
   - `to=[<prospect email>]`
   - `subject=<draft subject>`
   - `body=<draft body, HTML or plain text>`
3. Capture the returned draft `id` and store it in the prospect frontmatter as `draft_message_id`.
4. Set `state: draft_pending_approval`. Append to `## Audit`.

## Composer flow — saving a reply draft

When the Composer is drafting a reply to a prospect's reply:

1. Get the inbound message ID (from Cadence's reply detection — stored in the lead's `## Conversation` section).
2. Call `CreateReplyDraft(message_id=<inbound>, comment=<draft body>)`.
3. Update the MD file and capture `draft_message_id`.

## Cadence flow — queueing a templated step

When `next_step_at` is due for a lead in `awaiting_reply`:

1. Load the cadence template (e.g. `cadence-rules/templates/outbound-email-v1.md`).
2. Render the next step using lead variables.
3. Run compliance checks (`compliance/SKILL.md`).
4. Call `CreateReplyDraft(message_id=<original thread root>, comment=<rendered body>)` — follow-ups are always threaded.
5. Increment `touch_count`. Set `state: draft_pending_approval`. Append to `## Audit`.

## Cadence flow — detecting a send

Periodically scan for sends that have completed:

1. `ListMessages(folder_id="sentitems", received_after=<draft created time>)` — or `SearchM365` with `sources=["email"]`, `from_user=<OUTLOOK_FROM>`, query=`<subject>`.
2. Match on subject + recipient + send time after the draft creation.
3. If exactly one match → transition lead `draft_pending_approval → sent`, set `sent_at`, capture `thread_id` from the message's `conversationId`, clear `draft_message_id`.
4. If zero matches and the draft is older than 7 days → set `hold_reason: draft never sent`, do not transition.
5. If multiple matches → take the most recent, log a warning in `## Notes`.

## Cadence flow — detecting a reply

Periodically scan for replies on threads we're awaiting:

1. For each lead in `awaiting_reply` with a `thread_id`, call `ListMessages(folder_id="inbox", received_after=<sent_at>)` and filter by `conversationId` matching `thread_id` and sender matching the prospect's domain. Or `SearchM365` with `sources=["email"]`, `from_user=<prospect email>`, `after=<sent_at>`.
2. If a match → transition to `state: replied`, copy the reply body and message ID into the lead's `## Conversation` section, hand off to Composer for reply drafting.

## Authentication

All Graph access is delegated using the operator's M365 sign-in (`[YOUR_OUTLOOK_EMAIL]`). The harness never holds a service-principal token. If a tool call fails with `Unauthorized`, the operator needs to re-authenticate — the harness does not retry blindly.
