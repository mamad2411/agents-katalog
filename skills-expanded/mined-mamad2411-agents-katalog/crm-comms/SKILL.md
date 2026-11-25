---
name: crm-comms
description: Communication surfaces in the CRM (Twenty) — draft and send email, read synced message threads, campaigns, call recordings, and blocklists. Use for outreach, replying from CRM context, reviewing email history with a contact, or campaign work.
---

# CRM Comms

Read the `crm` skill first.

## Email

- **Draft Email** composes without sending — this is the default. Show the
  user the draft.
- **Send Email** actually sends from the connected mailbox. **Never send
  without explicit user approval of the final recipient list, subject, and
  body in this conversation.** Sending is irreversible.
- Ground outreach in CRM data: pull the person's record, recent notes, open
  deals, and last thread before drafting, and reference them naturally.

## Synced message threads

Email sync lands as messages/threads:

- `Search messages` / `Search message threads` filtered by participant to get
  history with a contact; `Search message participants` maps who was on what.
  `Find message` fetches one message's body.
- Message channel/folder association tools (`Create/Update/Delete message
  channel message association [message folder]`) manage how synced mail maps
  to channels and folders — touch these only for sync-repair tasks the user
  explicitly asks for.
- Deleting messages/threads removes synced copies from the CRM, not the
  mailbox; still confirm first.

## Campaigns

Campaigns are a custom object here: full
Find/Search/Group/Create/Update/Upsert/Delete family. Check
`Get Object Metadata` for its fields (status, dates, metrics). Typical flow:
create the campaign, build a list of targets (`crm-records` lists), and track
membership/results via list members and group calls.

## Call recordings and meeting notes

`Search call recordings` / `Find call recording` retrieve call records and
their transcripts/summaries when present; granola connection objects tie
external meeting-notes sources to the workspace. Use recordings as source
material for notes and follow-ups (`crm-productivity`).

## Blocklists

`Create blocklist` entries (email or domain) exclude addresses from sync.
`Search blocklists` to check why someone's mail is missing. Confirm before
adding or deleting entries — they change what the whole workspace syncs.
