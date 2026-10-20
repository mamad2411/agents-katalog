---
name: inbox-calendar-triage
description: Canonical inbox and calendar triage pack for agenda prep, urgent unread mail, follow-ups, and draft-only response suggestions.
tags: [inbox, calendar, email, gmail, meeting prep, follow-up]
keywords:
  - inbox
  - calendar
  - email
  - gmail
  - meeting prep
  - follow-up
triggers:
  - start the day
  - inbox triage
  - calendar triage
  - meeting prep
context_tags:
  - productivity
  - communication
canonical_pack: true
delivery_modes:
  - manual
  - routine
  - chat-delivery
prerequisite_hints:
  - "`gmail` connector recommended for inbox signal."
  - "`calendar` connector recommended for agenda and meeting prep."
  - "Reply suggestions must remain draft-only; no auto-send."
source_links:
  - plugins/zorai-plugin-gmail-calendar/README.md
mobile_safe: true
approval_behavior: "Draft suggestions are allowed as non-mutating output; sending replies or creating/modifying events requires fresh approval."
---

# Inbox + Calendar Triage

## User story

I want one privacy-safe briefing that combines urgent unread mail with today’s meetings and follow-ups, so I can prepare for the day without context switching across inbox and calendar.

## Pack contract

### Prerequisites and readiness

- Best experience requires both `gmail` and `calendar`
- If one connector is unavailable, continue with the other and mark the missing half as degraded
- If both are unavailable, fail closed with setup guidance

### Inputs and configuration fields

- `focus_window`: today / next 8h / next 24h
- `include_meeting_prep`: boolean
- `include_reply_drafts`: boolean
- `privacy_mode`: `strict` or `standard`

### Outputs and delivery targets

- today’s agenda
- urgent unread / follow-up messages
- meeting prep bullets linked to relevant mail threads when possible
- optional reply-draft suggestions that are explicitly marked as drafts
- mobile-safe bullets with original message/event references

## Manual run recipe

1. Fetch today’s calendar events.
2. Fetch urgent unread / follow-up Gmail messages.
3. Cross-link events with matching senders/subjects when possible.
4. Produce agenda + inbox triage with optional draft suggestions.

## Example routine wiring

`Run the Inbox + Calendar Triage pack before the first meeting and produce privacy-safe mobile output with draft-only suggestions.`

## Example prompt

`Run Inbox + Calendar Triage in strict privacy mode for today. Include urgent unread messages, follow-ups, meeting prep, and draft suggestions, but never send anything.`

## Failure and recovery behavior

- One connector missing -> continue with available source and label omission.
- Draft generation failure -> deliver triage without drafts.
- Any send/create/update request -> stop and require fresh approval.

## Verification checklist

- [ ] Gmail-only proof passes.
- [ ] Calendar-only proof passes.
- [ ] Combined Gmail + Calendar proof passes.
- [ ] Draft suggestions remain draft-only.
- [ ] Output is privacy-safe and source-linked.
