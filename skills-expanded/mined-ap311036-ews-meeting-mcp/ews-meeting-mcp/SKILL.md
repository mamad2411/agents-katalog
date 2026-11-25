---
name: ews-meeting-mcp
description: Use when reading company Outlook mail, sending self-only Jira reports, or scheduling and safely updating/cancelling meetings through the local EWS Meeting Agent MCP server, including checking Exchange/EWS availability, searching and reading the inbox, suggesting overlapping free slots, previewing lifecycle changes, and acting only after the relevant safety gate.
---

# EWS Meeting Agent

Use the `ews-meeting-mcp` MCP tools to read company Outlook mail, send self-only Jira reports, and schedule meetings through an on-prem Exchange/EWS calendar.

## Workflow

1. For company Outlook mail, call `ews_setup_check`, then `ews_search_emails` with the narrowest known filters. Present the returned metadata, use the exact selected `id` and optional `changekey` with `ews_read_email`, and summarize the returned message. These tools are read-only: they do not mark messages as read, move messages, delete messages, or change labels.
2. At the start of a scheduling session, call `ews_setup_check`. If it returns `ready: false`, show its `user_message` as-is, or show `setup_command` verbatim in a fenced `bash` block, and stop. Do not ask the user to paste a password into chat or MCP config; do not ask for attendee emails or continue with EWS tools until the user says they fixed setup. Then call `ews_setup_check` again before continuing.
   If the user asks how to set up an Outlook-style meeting signature, call `ews_signature_setup_guide` and show the returned `sample_html`, `recommended_path`, and `setup_command`; this helper does not require EWS credentials.
3. For the Thursday Jira weekly-report automation, after it assembles the previous and current report, call `ews_send_email_to_self` with `subject`, `body`, `body_format`, and a stable, non-secret `idempotency_key`. It has no recipient, `to`, `cc`, or `bcc` argument; it sends only to the configured `EWS_EMAIL` through EWS `CreateItem` followed by `SendItem`. Never substitute Gmail or `to: me`. Reuse the same idempotency key for retries; treat `duplicate_confirmation`, `confirmation_in_progress`, and unknown delivery as stop conditions until Sent Items and the audit log are inspected.
4. Parse the user's request into attendees, candidate rooms, date range, duration, subject, body, location, and optional `show_as`. For a personal appointment with exact times and no invitees/room, use `attendees: []` and `rooms: []`, skip attendee/room discovery and slot selection, and proceed to preview.
   For Taiwan/local office scheduling, pass datetime arguments with an explicit local offset such as `+08:00`. `Z` is accepted by the tool but means UTC, not local time.
5. If any attendee is not a complete email address, call `ews_resolve_attendees` first. Do not ask the user to provide full attendee email addresses before trying company directory resolution.
6. Use exactly resolved emails for scheduling. If a name has zero matches or multiple matches, ask the user to clarify or choose from the returned candidates before continuing. Prefer the host's interactive multiple-choice UI or clickable choice controls when available; otherwise show a short numbered list of candidates. For ambiguous matches, show candidate names and emails as choices; do not ask the user to type the full email manually.
7. If the user did not mention rooms, call `ews_list_rooms` with the attendee count if known, then ask whether a meeting room is needed using the returned `options`. Prefer the host's interactive multiple-choice UI or clickable choice controls when available; include "no meeting room" and "auto-pick any room with enough capacity" choices. The default `source: "auto"` tries Exchange room-list discovery and falls back to configured policy rooms; offer the user a choice among the returned room `value`s or "no specific room"; do not rely on a hand-written room list.
8. If the user wants a room but does not choose a specific room, call `ews_suggest_slots` with `require_room: true` and no `rooms`; the tool uses dynamic Exchange rooms when available, then falls back to configured rooms, and filters rooms with known `capacity` below the attendee count. `P` means persons.
9. If the user chooses specific rooms, pass the selected room `value`s or emails in `rooms` when calling `ews_suggest_slots`.
10. Show suggested slots with their `available_rooms`. When asking the user to pick a slot or room, prefer the host's interactive multiple-choice UI or clickable choice controls when available; otherwise show a short numbered list. Omit `workday_start`, `workday_end`, and `avoid` to use local policy defaults.
11. When the user picks a slot and room, call `ews_create_meeting_preview` with the selected room in `rooms`.
12. For recurring meeting requests, pass a structured `recurrence` object to preview and confirmed create calls. Weekly Monday/Wednesday uses `{"type":"weekly","interval":1,"weekdays":["MO","WE"],"range":{"type":"numbered","count":10}}`. Every business day until 2026-07-26 uses `{"type":"weekly","interval":1,"weekdays":["MO","TU","WE","TH","FR"],"range":{"type":"end_date","end_date":"2026-07-26"}}`. Business days mean Monday through Friday only. If the user gives weekdays but no end date, occurrence count, or explicit no-end choice, ask for one before previewing.
13. Show the exact preview: attendees, rooms, start/end with timezone offsets, `show_as`, `confirmed_will_send_invites`, subject, body, location, `signature` status, recurrence if present, and `confirmation_id`.
14. Only after the user explicitly confirms, call `ews_create_meeting_confirmed` with `confirm: true` and the exact `confirmation_id` returned by preview.
15. After a successful confirmed create, call `ews_verify_meeting` with the returned item `id` and `changekey` when available, then report the organizer item status and room `response_status`. Treat `unknown` room response as pending/unknown, not as failure.

## Existing Meeting Lifecycle

1. For a request to change or cancel an existing meeting, call `ews_find_calendar_events` with the narrowest known `start`/`end` window and filters such as `subject_contains`, `location_contains`, `organizer_email`, or `attendee_email`.
2. Use only the exact `id` and `changekey` returned by `ews_find_calendar_events`. If there is more than one plausible candidate, ask the user to choose one before previewing changes. Prefer the host's interactive multiple-choice UI or clickable choice controls when available; otherwise show a short numbered list.
3. For updates, call `ews_update_meeting_preview` with the exact `id`, `changekey`, and only supported fields: `subject`, `start`, `end`, `location`, `body`, and `show_as`. Do not attempt attendee or room replacement.
4. For cancellations, call `ews_cancel_meeting_preview` with the exact `id` and `changekey`.
5. Show the returned `current_event` plus `proposed_event`, or the `cancellation_target`, along with `warnings` and `confirmation_id`.
6. Only after the user explicitly confirms the exact action, call the matching confirmed tool with `confirm: true` and the exact `confirmation_id` returned by preview.

## Safety

- Never call `ews_create_meeting_confirmed`, `ews_update_meeting_confirmed`, or `ews_cancel_meeting_confirmed` without explicit user confirmation.
- Never invent or reuse stale lifecycle metadata. Confirmed create/update/cancel calls must use the exact matching `confirmation_id` from the preview; update/cancel also require the latest exact `id` and `changekey`.
- If a confirmed tool returns `error_code: "duplicate_confirmation"`, treat the action as already handled, inspect `prior_result`, and do not retry blindly.
- If a confirmed tool returns `error_code: "confirmation_in_progress"`, wait or inspect the calendar/audit log; do not issue another confirmed call with the same `confirmation_id`.
- Confirmed cancellation is limited to non-recurring organizer meetings when Exchange exposes those fields. If a tool reports recurrence or organizer limitations, ask the user to handle it in Outlook.
- `ews_send_email_to_self` is the only mail-write tool. It accepts no recipient, `to`, `cc`, or `bcc` value and sends only to configured `EWS_EMAIL` after validating a stable idempotency key.
- Never put email addresses, passwords, tokens, or raw credential values in prompts, tool arguments, audit entries, or logs. The self-only send tool does not record its recipient, subject, or body.
- Do not put EWS passwords in prompts or messages. The MCP server reads credentials from `.env`, environment variables, or macOS Keychain.
- Do not add the organizer as an attendee unless the user explicitly asks; Exchange creates the organizer's calendar item automatically.
- If Outlook does not show a newly created meeting immediately, ask the user to sync or restart Outlook before assuming the event is missing.

## Tool Notes

- Calendar Show As is optional on all four create/update preview/confirmed tools: `free`, `tentative`, `busy`, or `out_of_office` (EWS `OOF`). This changes calendar status, not email automatic replies. Omission keeps the Busy default on create and preserves the stored status on update. Personal appointments always use `SendToNone`; show the effective no-invitation flag before confirmation. Pass the same `show_as` in preview and confirmed calls. Weekly recurring creation also accepts it; recurrence editing scope is unchanged. After saving, use `ews_verify_meeting` and check stored `show_as: "out_of_office"` plus raw `legacy_free_busy_status: "OOF"`. Unknown/missing stored statuses return `show_as: null`; do not infer success from the subject or preview.

- Use `ews_search_emails` for company Outlook inbox questions. Filter by `subject_contains`, `sender_email`, `after`, `before`, or `unread_only`; omit filters to list recent inbox messages. Then use the exact returned `id` with `ews_read_email` to retrieve the body and attachment metadata.
- Mail reads do not mark messages as read. Do not claim that a read tool sent, forwarded, moved, deleted, or labeled a message. Use only `ews_send_email_to_self` for the Thursday report self-send.
- For `ews_send_email_to_self`, call `ews_setup_check` first, then pass `subject`, `body`, optional `body_format` (`text` by default), and a stable `idempotency_key`. Reuse the same key on retry; never pass or invent a recipient.
- Use `ews_resolve_attendees` whenever the user gives names, aliases, or mixed name/email attendee lists. Never ask for full attendee emails as the first step; try directory resolution first.
- Use `ews_setup_check` before the first EWS operation in a session. It never returns the password. If `ready` is false, follow `next_action` or `required_action`, show the setup instructions, and stop.
- Use `ews_keychain_status` only when you specifically need the password source diagnostic.
- Use `ews_get_audit_log` when you need to inspect recent preview, confirmed, sent, duplicate, in-progress, or structured error outcomes. It reads a local JSONL audit log and never returns EWS passwords or self-send content.
- If any EWS tool returns `error_code: "credentials_missing"` or `required_action: "show_setup_command"`, show the returned `setup_command` verbatim and do not ask the user for attendee email addresses as a workaround.
- If any live EWS tool returns `error_code: "authentication_failed"` or `error_code: "authentication_retry_blocked"`, stop immediately. Do not retry or call another live EWS tool; fix the shared Keychain item and restart the MCP process first.
- Use `ews_list_rooms` to present structured meeting-room choices before asking the user to choose a room. `source: "auto"` discovers dynamic Exchange rooms when credentials are available and falls back to configured rooms; `source: "static"` is credential-free; `source: "exchange"` requires EWS credentials.
- Scheduling and meeting tools also auto-resolve non-email attendees; if they report ambiguity or not found, ask the user to choose or provide the exact email.
- Use multiple attendee emails and candidate room aliases in one `ews_suggest_slots` call.
- Use `require_room: true` when the user wants a room but does not specify which room.
- To schedule with a room, pass the selected room in `rooms` to both preview and confirmed meeting tools. The room is sent as an Exchange resource, not as a required attendee.
- To schedule a recurring meeting, use `recurrence.type: "weekly"` with weekday codes `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU`. Use `range.type: "end_date"`, `"numbered"`, or `"no_end"`; do not preview a recurrence until the range is explicit.
- Meeting body defaults to `body_format: "html"`. You may turn a user-provided agenda into concise HTML, including clickable PRD/Wiki links. Plain text bodies are also accepted and are safely converted to HTML with line breaks and URL anchors.
- New meeting bodies append the configured HTML signature by default when `body_format: "html"`. Use `include_signature: false` only when the user explicitly asks to omit the signature for that meeting. If no signature file is configured, scheduling still works and the preview includes `signature.configured: false`.
- Use `ews_signature_setup_guide` whenever the user needs help creating or editing the signature file. The tool returns a copyable HTML starter with name, email link, logo image, and disclaimer sections.
- Use `ews_get_free_busy` for diagnostics when slot suggestions look surprising.
- Use `ews_list_calendar` to verify whether an event exists on the server calendar.
- Use `ews_find_calendar_events` before update or cancel because it returns stable item metadata (`id`, `changekey`, `uid`, attendees, resources, organizer, meeting/cancelled/recurrence flags) needed for safe lifecycle tools.
- Use `ews_verify_meeting` after successful create/update when the user needs confirmation that the organizer calendar item exists or wants room/resource response status.
- Preview tools never save, move, delete, or send Exchange notifications. They exist to produce the exact payload the user should confirm.
- Confirmed tools record completed `confirmation_id`s in a local ledger. Self-only sends record a one-way idempotency key hash in the local ledger. Lifecycle preview/confirmed/sent/duplicate/in-progress/error outcomes are also written to a local audit log. The ledger and audit log store operation metadata, not recipient addresses, mail content, or EWS passwords.
- If a confirmed create, update, or cancel returns `error_code: "confirmation_mismatch"`, call the matching preview tool again, show the new preview, and ask for confirmation again.
