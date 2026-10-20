---
name: slashy-email
description: Search, read, triage, summarize, label, archive, draft, reply to, send, and attach files to email through Slashy MCP. Use for inbox questions, unread or priority sweeps, thread history, follow-ups, email composition, Slashy thread links, attachments from Drive or local files, and any request to manage mail.
---

# Slashy email

Use Slashy tools for account-specific email work. Discover exact tool names and
schemas first; the official server commonly exposes operations equivalent to
`get_user_info`, `list_messages`, `read_thread`, `draft_email`, `send_email`,
and file-upload helpers.

## Search and triage

1. Translate relative time phrases into concrete dates in the user's timezone.
2. Search or list the narrowest useful set of messages.
3. Read full threads only when the answer depends on thread context.
4. Rank by the user's criteria; otherwise prioritize explicit deadlines,
   unanswered direct questions, commitments, and high-value senders.
5. Identify what is evidence from the inbox versus your recommendation.
6. Include a Slashy thread link for each returned thread when identifiers are
   present; follow the link format in the core `slashy` skill.

## Draft, reply, and send

- Default ambiguous composition requests to `draft_email` or the discovered
  draft-equivalent tool. Send only when the user explicitly says "send".
- Read the target thread before drafting a reply so the response preserves
  context, recipients, subject, and threading.
- Match the user's requested tone and constraints. Do not invent commitments,
  dates, prices, or attachments absent from the request or source thread.
- Pass one email address per recipient-array element. Never pass a single
  comma-separated string to `to`, `cc`, or `bcc`.
- If several connected inboxes could send the message, resolve the `from`
  account before acting.
- After saving a draft, return its Slashy link with `?m={draft_id}`. After a
  send, confirm sender, recipients, subject, and whether attachments succeeded.

## Labels, archive, and bulk changes

Treat labels, archive, trash, spam, unsubscribe, and bulk operations as writes.
Require an explicit user request, keep filters narrow, and report the number of
affected threads. For recurring behavior, use `slashy-research` to create an
automation rather than implying a one-time change will continue automatically.

## Attachments

- For a file already in Google Drive, use Slashy's Drive-aware attachment flow
  when the server exposes it; attach the file rather than merely pasting a link
  unless the user requests a link. If several files match, disambiguate by
  filename, type, modified time, or folder instead of guessing.
- For local files smaller than roughly 256 KB, use the discovered inline upload
  operation when its schema permits.
- For larger files, call the server's `request_file_upload` equivalent with the
  filename and MIME type, immediately `PUT` the bytes to the returned presigned
  URL, then pass the returned `file_id` to the draft or send tool.
- Presigned upload URLs expire quickly and must never be shown in the final
  response. Verify the attachment appears in the draft/send result.
