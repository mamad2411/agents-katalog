---
name: manage-participants
description: Use when the user wants to add people to an EXISTING Boom initiative, check who has replied or a participant's status, stop outreach to someone, or read one participant's conversation. Participants always belong to an initiative — there is no global list and no delete (stopping retains data). To create and launch a brand-new initiative, use launch-initiative.
---

# Manage Participants

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `initiatives_list` | Find the target initiative | read |
| `initiatives_participants_add` | Enroll people in an initiative | **admin** |
| `initiatives_participants_list` | List participants + status, paginated | read |
| `initiatives_participant_get` | One participant's detail | read |
| `initiatives_participants_stop` | Stop outreach to one participant (data retained) | **admin** |
| `initiatives_participant_messages_list` | Full transcript for one participant | read |
| `drafts_list` | Sends waiting for approval, when a participant seems stuck at a send step | read |

## Core rules

- Participants live ONLY under initiatives — there is no global participant list. Always resolve the initiative first.
- **There is no delete.** `initiatives_participants_stop` halts outreach; transcripts and extracted data are retained. If a user asks to "remove" someone, stop them and explain retention. If they ask to *never contact someone again across all initiatives*, that's Do Not Contact — managed in the Boom app, not via MCP.
- `phoneNumber` (E.164) is the only phone field. On an **email** initiative, send `email` instead: a WhatsApp initiative needs `phoneNumber`, an email one needs `email`.

## Workflow: adding participants

1. Confirm the target initiative (`initiatives_list` / user link).
2. Shape rows as `{ "phoneNumber": "+5215512345678", "name": "...", "lastName": "...", ...attributes }` (on an email initiative, `"email": "ana@example.com"` in place of `phoneNumber`) — extra attributes become interview context the agent can use.
3. Call `initiatives_participants_add`. Compare the accepted count to what you sent: DNC-suppressed people (phones and email addresses alike) come back as `contact_suppressed`. **Report the delta; never retry suppressed entries.** A row without the channel's identifier comes back in `errors` as `missing_phone_number` / `missing_email`, and a malformed address as `invalid_email`. It isn't enrolled, but the rest of the batch still is, so fix and resend only those rows.
4. This one needs org admin — on `error.code: "forbidden"`, tell the user their Boom account isn't an admin of the organization, so they need an admin to run it or to do it from the Boom app.

## Workflow: monitoring & stopping

- `initiatives_participants_list` and paginate with `next_cursor`; summarize by status rather than dumping rows.
- Before `initiatives_participants_stop`, confirm with the user — it's not reversible by re-adding mid-conversation.
- To review a conversation, `initiatives_participant_messages_list` returns the flat chronological transcript with direction and author.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `error.code: "forbidden"` | The signed-in user isn't an org admin, and this write sends real messages | An org admin runs it, or do it from the Boom app |
| Person missing after add | DNC suppression | Expected; report, don't retry |
| Participant stuck at a send step, nothing sent | The send node holds sends for approval (`delivery: "draft"`) and their draft is waiting | Check `drafts_list` (filter by `initiativeId`) for a PENDING draft. Approving it sends a real message, so show the user the content first. Drafts don't expire, so the participant waits until someone decides |
| `next_cursor` keeps returning | You're re-sending the first-page call | Pass the *previous response's* cursor each time; stop at `null` |

See [`CONTEXT.md`](../../CONTEXT.md) for the domain model.
